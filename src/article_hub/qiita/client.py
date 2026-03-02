"""Qiita API v2 同期クライアント"""

from types import TracebackType

import httpx

from .models import QiitaItemRequest, QiitaItemResponse

BASE_URL = "https://qiita.com"


class QiitaApiError(Exception):
    """Qiita API エラー"""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(message)


class QiitaClient:
    """Qiita API v2 の同期クライアント"""

    def __init__(self, token: str, transport: httpx.BaseTransport | None = None) -> None:
        self._client = httpx.Client(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            transport=transport,
        )

    def list_items(self, page: int = 1, per_page: int = 20) -> list[QiitaItemResponse]:
        """認証ユーザーの記事一覧を取得"""
        response = self._client.get(
            "/api/v2/authenticated_user/items",
            params={"page": page, "per_page": per_page},
        )
        self._handle_error(response)
        return [QiitaItemResponse.model_validate(item) for item in response.json()]

    def create_item(self, item: QiitaItemRequest) -> QiitaItemResponse:
        """記事を新規作成"""
        response = self._client.post("/api/v2/items", content=item.model_dump_json())
        self._handle_error(response)
        return QiitaItemResponse.model_validate(response.json())

    def update_item(self, item_id: str, item: QiitaItemRequest) -> QiitaItemResponse:
        """既存記事を更新"""
        response = self._client.patch(f"/api/v2/items/{item_id}", content=item.model_dump_json())
        self._handle_error(response)
        return QiitaItemResponse.model_validate(response.json())

    def close(self) -> None:
        """クライアントを閉じる"""
        self._client.close()

    def __enter__(self) -> "QiitaClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    @staticmethod
    def _handle_error(response: httpx.Response) -> None:
        """HTTP レスポンスのエラーハンドリング"""
        if response.status_code < 400:
            return
        if response.status_code == 401:
            raise QiitaApiError(401, "認証エラー: トークンが無効です")
        if response.status_code == 404:
            raise QiitaApiError(404, "記事が見つかりません")
        if response.status_code == 429:
            raise QiitaApiError(429, "レート制限に達しました。しばらく待ってからリトライしてください")
        raise QiitaApiError(response.status_code, f"API エラー ({response.status_code})")
