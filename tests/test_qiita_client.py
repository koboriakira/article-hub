"""Qiita API クライアントのテスト"""

import json

import httpx
import pytest

from article_hub.qiita.client import QiitaApiError, QiitaClient
from article_hub.qiita.models import QiitaItemRequest, QiitaTag


def _make_item_json(item_id: str = "abc123", title: str = "テスト記事") -> dict:
    return {
        "id": item_id,
        "title": title,
        "url": f"https://qiita.com/test/items/{item_id}",
        "created_at": "2026-01-01T00:00:00+09:00",
        "updated_at": "2026-01-02T00:00:00+09:00",
        "tags": [{"name": "Python", "versions": []}],
        "private": False,
        "likes_count": 0,
    }


def _mock_transport(handler):
    return httpx.MockTransport(handler)


class TestQiitaClientListItems:
    """list_items のテスト"""

    def test_list_items_success(self) -> None:
        items = [_make_item_json("id1", "記事1"), _make_item_json("id2", "記事2")]

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api/v2/authenticated_user/items"
            assert request.headers["authorization"] == "Bearer test-token"
            return httpx.Response(200, json=items)

        client = QiitaClient(token="test-token", transport=_mock_transport(handler))
        result = client.list_items()
        assert len(result) == 2
        assert result[0].id == "id1"
        assert result[1].title == "記事2"
        client.close()

    def test_list_items_with_pagination(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.params["page"] == "2"
            assert request.url.params["per_page"] == "5"
            return httpx.Response(200, json=[])

        client = QiitaClient(token="test-token", transport=_mock_transport(handler))
        result = client.list_items(page=2, per_page=5)
        assert result == []
        client.close()

    def test_list_items_unauthorized(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"message": "Unauthorized"})

        client = QiitaClient(token="bad-token", transport=_mock_transport(handler))
        with pytest.raises(QiitaApiError, match="認証エラー"):
            client.list_items()
        client.close()


class TestQiitaClientCreateItem:
    """create_item のテスト"""

    def test_create_item_success(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api/v2/items"
            assert request.method == "POST"
            body = json.loads(request.content)
            assert body["title"] == "新しい記事"
            return httpx.Response(201, json=_make_item_json("new123", "新しい記事"))

        client = QiitaClient(token="test-token", transport=_mock_transport(handler))
        req = QiitaItemRequest(title="新しい記事", body="本文", tags=[QiitaTag(name="Python")])
        result = client.create_item(req)
        assert result.id == "new123"
        client.close()

    def test_create_item_rate_limit(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(429, json={"message": "Rate limit exceeded"})

        client = QiitaClient(token="test-token", transport=_mock_transport(handler))
        req = QiitaItemRequest(title="テスト", body="本文", tags=[QiitaTag(name="Python")])
        with pytest.raises(QiitaApiError, match="レート制限"):
            client.create_item(req)
        client.close()


class TestQiitaClientUpdateItem:
    """update_item のテスト"""

    def test_update_item_success(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api/v2/items/abc123"
            assert request.method == "PATCH"
            body = json.loads(request.content)
            assert body["title"] == "更新された記事"
            return httpx.Response(200, json=_make_item_json("abc123", "更新された記事"))

        client = QiitaClient(token="test-token", transport=_mock_transport(handler))
        req = QiitaItemRequest(title="更新された記事", body="更新本文", tags=[QiitaTag(name="Python")])
        result = client.update_item("abc123", req)
        assert result.title == "更新された記事"
        client.close()

    def test_update_item_not_found(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"message": "Not found"})

        client = QiitaClient(token="test-token", transport=_mock_transport(handler))
        req = QiitaItemRequest(title="テスト", body="本文", tags=[QiitaTag(name="Python")])
        with pytest.raises(QiitaApiError, match="見つかりません"):
            client.update_item("nonexistent", req)
        client.close()


class TestQiitaClientContextManager:
    """コンテキストマネージャのテスト"""

    def test_context_manager(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=[])

        with QiitaClient(token="test-token", transport=_mock_transport(handler)) as client:
            result = client.list_items()
            assert result == []
