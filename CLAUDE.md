# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Qiita記事のAPI投稿・更新を行うPython CLIツール。ローカルのMarkdownファイルとQiita上の記事を同期管理する。

### 技術スタック
- Python 3.12+ / uv（パッケージ管理）
- typer（CLI）/ httpx（HTTPクライアント）/ pydantic（データバリデーション）
- ruff（リンター・フォーマッター）/ mypy strict（型チェック）/ pytest（テスト）

## 開発コマンド

```bash
uv sync                              # 依存関係インストール
uv run pytest                        # テスト実行（カバレッジ80%以上必須）
uv run pytest tests/test_foo.py      # 単一テストファイル
uv run pytest -k "test_name"         # 特定テストのみ
uv run ruff check .                  # リンティング
uv run ruff format .                 # フォーマット
uv run mypy                          # 型チェック（strict mode）
uv add package-name                  # 依存関係追加
uv add --group dev package-name      # 開発用依存関係追加
```

## アーキテクチャ

```
src/article_hub/
├── main.py              # CLIエントリーポイント（typer）
├── api.py               # FastAPI アプリケーション（将来のWeb UI用）
├── routers/             # FastAPI ルーター
└── utils.py             # ユーティリティ関数
tests/                   # pytest classベーステスト
```

- CLIエントリーポイント: `article-hub` コマンド（`article_hub.main:app`）
- pyproject.toml に全ツール設定を集約（ruff, mypy, pytest, coverage）

## コーディング規約

- classベーステスト推奨、`@pytest.mark.parametrize` でデータ駆動テスト活用
- Python 3.12+ の型ヒント使用（`list[str]` > `List[str]`）
- ruff: `line-length = 120`、ダブルクォート
- Conventional Commits 形式（`feat:`, `fix:`, `docs:` 等）

## 環境変数

`.env.local` に設定（`.gitignore` 対象）。`.env.example` にテンプレートあり。

| 変数名 | 説明 |
|--------|------|
| `QIITA_ACCESS_TOKEN` | Qiita API v2 アクセストークン |

## 外部API

### Qiita API v2
- Base URL: `https://qiita.com/api/v2`
- 認証: `Authorization: Bearer <TOKEN>`
- レート制限: 1,000回/時間（認証済み）
- 主要エンドポイント: `POST /items`（作成）、`PATCH /items/:id`（更新）、`GET /authenticated_user/items`（一覧）
