"""main.pyのテスト"""

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from article_hub import __version__
from article_hub.main import app
from article_hub.qiita.models import QiitaItemResponse, QiitaTag


def _make_response(item_id: str = "abc123", title: str = "テスト記事") -> QiitaItemResponse:
    return QiitaItemResponse(
        id=item_id,
        title=title,
        url=f"https://qiita.com/test/items/{item_id}",
        created_at="2026-01-01T00:00:00+09:00",
        updated_at="2026-01-02T00:00:00+09:00",
        tags=[QiitaTag(name="Python")],
        private=False,
    )


class TestCLI:
    """CLIアプリケーションのテスト"""

    def setup_method(self) -> None:
        """テスト用のCLIランナーをセットアップ"""
        self.runner = CliRunner()

    def test_hello_default(self) -> None:
        """デフォルトの挨拶をテスト"""
        result = self.runner.invoke(app, ["hello"])
        assert result.exit_code == 0
        assert "こんにちは、World!" in result.stdout

    def test_hello_with_name(self) -> None:
        """名前を指定した挨拶をテスト"""
        result = self.runner.invoke(app, ["hello", "--name", "テスト"])
        assert result.exit_code == 0
        assert "こんにちは、テスト!" in result.stdout

    def test_version(self) -> None:
        """バージョン表示をテスト"""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout


class TestListCommand:
    """list コマンドのテスト"""

    def setup_method(self) -> None:
        self.runner = CliRunner()

    @patch("article_hub.main._get_token", return_value="test-token")
    @patch("article_hub.main.QiitaClient")
    def test_list_success(self, mock_client_cls, _mock_token) -> None:
        mock_client = MagicMock()
        mock_client.list_items.return_value = [
            _make_response("id1", "記事1"),
            _make_response("id2", "記事2"),
        ]
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = self.runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "記事1" in result.stdout
        assert "記事2" in result.stdout

    @patch("article_hub.main._get_token", return_value="test-token")
    @patch("article_hub.main.QiitaClient")
    def test_list_with_pagination(self, mock_client_cls, _mock_token) -> None:
        mock_client = MagicMock()
        mock_client.list_items.return_value = []
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = self.runner.invoke(app, ["list", "--page", "2", "--per-page", "5"])
        assert result.exit_code == 0
        mock_client.list_items.assert_called_once_with(page=2, per_page=5)

    @patch("article_hub.main._get_token", return_value=None)
    def test_list_no_token(self, _mock_token) -> None:
        result = self.runner.invoke(app, ["list"])
        assert result.exit_code == 1
        assert "QIITA_ACCESS_TOKEN" in result.stdout


class TestPostCommand:
    """post コマンドのテスト"""

    def setup_method(self) -> None:
        self.runner = CliRunner()

    @patch("article_hub.main._get_token", return_value="test-token")
    @patch("article_hub.main.QiitaClient")
    @patch("article_hub.main.parse_markdown_file")
    def test_post_success(self, mock_parse, mock_client_cls, _mock_token) -> None:
        from article_hub.qiita.models import ArticleFrontmatter

        mock_parse.return_value = (
            ArticleFrontmatter(title="新記事", tags=["Python"]),
            "本文テキスト",
        )
        mock_client = MagicMock()
        mock_client.create_item.return_value = _make_response("new1", "新記事")
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = self.runner.invoke(app, ["post", "/tmp/test.md"])
        assert result.exit_code == 0
        assert "new1" in result.stdout

    @patch("article_hub.main._get_token", return_value="test-token")
    @patch("article_hub.main.QiitaClient")
    @patch("article_hub.main.parse_markdown_file")
    def test_post_private(self, mock_parse, mock_client_cls, _mock_token) -> None:
        from article_hub.qiita.models import ArticleFrontmatter

        mock_parse.return_value = (
            ArticleFrontmatter(title="限定記事", tags=["Python"]),
            "本文テキスト",
        )
        mock_client = MagicMock()
        mock_client.create_item.return_value = _make_response("priv1", "限定記事")
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = self.runner.invoke(app, ["post", "/tmp/test.md", "--private"])
        assert result.exit_code == 0
        mock_client.create_item.assert_called_once()
        call_args = mock_client.create_item.call_args[0][0]
        assert call_args.private is True


class TestUpdateCommand:
    """update コマンドのテスト"""

    def setup_method(self) -> None:
        self.runner = CliRunner()

    @patch("article_hub.main._get_token", return_value="test-token")
    @patch("article_hub.main.QiitaClient")
    @patch("article_hub.main.parse_markdown_file")
    def test_update_with_frontmatter_id(self, mock_parse, mock_client_cls, _mock_token) -> None:
        from article_hub.qiita.models import ArticleFrontmatter

        mock_parse.return_value = (
            ArticleFrontmatter(title="更新記事", tags=["Python"], qiita_id="abc123"),
            "更新本文",
        )
        mock_client = MagicMock()
        mock_client.update_item.return_value = _make_response("abc123", "更新記事")
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = self.runner.invoke(app, ["update", "/tmp/test.md"])
        assert result.exit_code == 0
        mock_client.update_item.assert_called_once()
        assert mock_client.update_item.call_args[0][0] == "abc123"

    @patch("article_hub.main._get_token", return_value="test-token")
    @patch("article_hub.main.QiitaClient")
    @patch("article_hub.main.parse_markdown_file")
    def test_update_with_cli_id(self, mock_parse, mock_client_cls, _mock_token) -> None:
        from article_hub.qiita.models import ArticleFrontmatter

        mock_parse.return_value = (
            ArticleFrontmatter(title="更新記事", tags=["Python"]),
            "更新本文",
        )
        mock_client = MagicMock()
        mock_client.update_item.return_value = _make_response("xyz789", "更新記事")
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = self.runner.invoke(app, ["update", "/tmp/test.md", "--id", "xyz789"])
        assert result.exit_code == 0
        mock_client.update_item.assert_called_once()
        assert mock_client.update_item.call_args[0][0] == "xyz789"

    @patch("article_hub.main._get_token", return_value="test-token")
    @patch("article_hub.main.parse_markdown_file")
    def test_update_no_id(self, mock_parse, _mock_token) -> None:
        from article_hub.qiita.models import ArticleFrontmatter

        mock_parse.return_value = (
            ArticleFrontmatter(title="ID なし", tags=["Python"]),
            "本文",
        )
        result = self.runner.invoke(app, ["update", "/tmp/test.md"])
        assert result.exit_code == 1
        assert "qiita_id" in result.stdout
