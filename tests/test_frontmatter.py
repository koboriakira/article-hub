"""Frontmatter パーサーのテスト"""

import pytest

from article_hub.qiita.frontmatter import parse_markdown_file
from article_hub.qiita.models import ArticleFrontmatter


class TestParseMarkdownFile:
    """parse_markdown_file のテスト"""

    def test_parse_basic_frontmatter(self, tmp_path) -> None:
        md = tmp_path / "article.md"
        md.write_text(
            '---\ntitle: "テスト記事"\ntags:\n  - Python\n  - CLI\nprivate: false\n---\n\n# 本文\n\nこれはテストです。\n',
            encoding="utf-8",
        )
        frontmatter, body = parse_markdown_file(md)
        assert isinstance(frontmatter, ArticleFrontmatter)
        assert frontmatter.title == "テスト記事"
        assert frontmatter.tags == ["Python", "CLI"]
        assert frontmatter.private is False
        assert "# 本文" in body
        assert "これはテストです。" in body

    def test_parse_with_qiita_id(self, tmp_path) -> None:
        md = tmp_path / "article.md"
        md.write_text(
            '---\ntitle: "更新記事"\ntags:\n  - Python\nqiita_id: "abc123"\n---\n\n本文\n',
            encoding="utf-8",
        )
        frontmatter, _body = parse_markdown_file(md)
        assert frontmatter.qiita_id == "abc123"

    def test_parse_private_article(self, tmp_path) -> None:
        md = tmp_path / "article.md"
        md.write_text(
            '---\ntitle: "限定記事"\ntags:\n  - Python\nprivate: true\n---\n\n本文\n',
            encoding="utf-8",
        )
        frontmatter, _body = parse_markdown_file(md)
        assert frontmatter.private is True

    def test_file_not_found(self) -> None:
        from pathlib import Path

        with pytest.raises(FileNotFoundError):
            parse_markdown_file(Path("/nonexistent/file.md"))

    def test_no_frontmatter_delimiter(self, tmp_path) -> None:
        md = tmp_path / "article.md"
        md.write_text("# ただのMarkdown\n\n本文です\n", encoding="utf-8")
        with pytest.raises(ValueError, match="frontmatter"):
            parse_markdown_file(md)

    def test_missing_required_field(self, tmp_path) -> None:
        md = tmp_path / "article.md"
        md.write_text('---\ntitle: "タイトルのみ"\n---\n\n本文\n', encoding="utf-8")
        with pytest.raises(ValueError, match="tags"):
            parse_markdown_file(md)

    def test_invalid_yaml(self, tmp_path) -> None:
        md = tmp_path / "article.md"
        md.write_text("---\ntitle: [invalid yaml\n---\n\n本文\n", encoding="utf-8")
        with pytest.raises(ValueError, match="YAML"):
            parse_markdown_file(md)

    def test_body_strips_leading_newlines(self, tmp_path) -> None:
        md = tmp_path / "article.md"
        md.write_text(
            '---\ntitle: "テスト"\ntags:\n  - Python\n---\n\n\n\n本文の開始\n',
            encoding="utf-8",
        )
        _frontmatter, body = parse_markdown_file(md)
        assert body.startswith("本文の開始")
