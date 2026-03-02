"""Qiita API のデータモデル"""

from pydantic import BaseModel, ConfigDict


class QiitaTag(BaseModel):
    """Qiita のタグ"""

    name: str
    versions: list[str] = []


class QiitaItemRequest(BaseModel):
    """Qiita 記事の作成・更新リクエスト"""

    title: str
    body: str
    tags: list[QiitaTag]
    private: bool = False


class QiitaItemResponse(BaseModel):
    """Qiita API からの記事レスポンス"""

    model_config = ConfigDict(extra="ignore")

    id: str
    title: str
    url: str
    created_at: str
    updated_at: str
    tags: list[QiitaTag]
    private: bool


class ArticleFrontmatter(BaseModel):
    """Markdown ファイルの frontmatter"""

    title: str
    tags: list[str]
    private: bool = False
    qiita_id: str | None = None

    def to_qiita_tags(self) -> list[QiitaTag]:
        """タグ名のリストを QiitaTag のリストに変換"""
        return [QiitaTag(name=tag) for tag in self.tags]
