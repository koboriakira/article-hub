"""Qiita モデルのテスト"""

import pytest
from pydantic import ValidationError

from article_hub.qiita.models import ArticleFrontmatter, QiitaItemRequest, QiitaItemResponse, QiitaTag


class TestQiitaTag:
    """QiitaTag モデルのテスト"""

    def test_tag_with_name_only(self) -> None:
        tag = QiitaTag(name="Python")
        assert tag.name == "Python"
        assert tag.versions == []

    def test_tag_with_versions(self) -> None:
        tag = QiitaTag(name="Python", versions=["3.12", "3.13"])
        assert tag.name == "Python"
        assert tag.versions == ["3.12", "3.13"]

    def test_tag_name_required(self) -> None:
        with pytest.raises(ValidationError):
            QiitaTag()  # type: ignore[call-arg]


class TestQiitaItemRequest:
    """QiitaItemRequest モデルのテスト"""

    def test_minimal_request(self) -> None:
        req = QiitaItemRequest(title="テスト記事", body="本文", tags=[QiitaTag(name="Python")])
        assert req.title == "テスト記事"
        assert req.body == "本文"
        assert req.private is False
        assert len(req.tags) == 1

    def test_private_request(self) -> None:
        req = QiitaItemRequest(title="限定記事", body="本文", tags=[QiitaTag(name="Python")], private=True)
        assert req.private is True

    def test_title_required(self) -> None:
        with pytest.raises(ValidationError):
            QiitaItemRequest(body="本文", tags=[QiitaTag(name="Python")])  # type: ignore[call-arg]

    def test_tags_required(self) -> None:
        with pytest.raises(ValidationError):
            QiitaItemRequest(title="テスト", body="本文")  # type: ignore[call-arg]


class TestQiitaItemResponse:
    """QiitaItemResponse モデルのテスト"""

    def test_parse_response(self) -> None:
        data = {
            "id": "abc123",
            "title": "テスト記事",
            "url": "https://qiita.com/test/items/abc123",
            "created_at": "2026-01-01T00:00:00+09:00",
            "updated_at": "2026-01-02T00:00:00+09:00",
            "tags": [{"name": "Python", "versions": []}],
            "private": False,
        }
        resp = QiitaItemResponse.model_validate(data)
        assert resp.id == "abc123"
        assert resp.title == "テスト記事"
        assert resp.url == "https://qiita.com/test/items/abc123"
        assert resp.private is False
        assert len(resp.tags) == 1

    def test_extra_fields_ignored(self) -> None:
        data = {
            "id": "abc123",
            "title": "テスト",
            "url": "https://qiita.com/test/items/abc123",
            "created_at": "2026-01-01T00:00:00+09:00",
            "updated_at": "2026-01-02T00:00:00+09:00",
            "tags": [],
            "private": False,
            "likes_count": 42,
            "comments_count": 5,
            "page_views_count": 100,
        }
        resp = QiitaItemResponse.model_validate(data)
        assert resp.id == "abc123"


class TestArticleFrontmatter:
    """ArticleFrontmatter モデルのテスト"""

    def test_minimal_frontmatter(self) -> None:
        fm = ArticleFrontmatter(title="テスト", tags=["Python"])
        assert fm.title == "テスト"
        assert fm.tags == ["Python"]
        assert fm.private is False
        assert fm.qiita_id is None

    def test_full_frontmatter(self) -> None:
        fm = ArticleFrontmatter(title="テスト", tags=["Python", "CLI"], private=True, qiita_id="abc123")
        assert fm.private is True
        assert fm.qiita_id == "abc123"

    def test_title_required(self) -> None:
        with pytest.raises(ValidationError):
            ArticleFrontmatter(tags=["Python"])  # type: ignore[call-arg]

    def test_tags_required(self) -> None:
        with pytest.raises(ValidationError):
            ArticleFrontmatter(title="テスト")  # type: ignore[call-arg]

    def test_to_qiita_tags(self) -> None:
        fm = ArticleFrontmatter(title="テスト", tags=["Python", "CLI"])
        qiita_tags = fm.to_qiita_tags()
        assert len(qiita_tags) == 2
        assert qiita_tags[0].name == "Python"
        assert qiita_tags[1].name == "CLI"
