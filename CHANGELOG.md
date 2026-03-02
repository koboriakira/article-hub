# Changelog

すべての注目すべき変更はこのファイルに記録されます。

このプロジェクトは[セマンティックバージョニング](https://semver.org/spec/v2.0.0.html)に従い、
[Conventional Commits](https://conventionalcommits.org/)を使用して自動的にリリースを生成します。

## 0.1.0 (2026-03-02)


### Features

* CLI コマンド追加 (list, post, update) ([ed45dc9](https://github.com/koboriakira/article-hub/commit/ed45dc93aee7df655d94eb60b5d8406443fa7f29))
* Markdown frontmatter パーサー (parse_markdown_file) ([8a4e668](https://github.com/koboriakira/article-hub/commit/8a4e668fa160978519168b20a56b9b248822e128))
* Qiita API v2 同期クライアント (list/create/update) ([16023e9](https://github.com/koboriakira/article-hub/commit/16023e9c67ceda2b517f4963dd25baaa19672ebe))
* Qiita API の Pydantic モデル定義（QiitaTag, QiitaItemRequest, QiitaItemResponse, ArticleFrontmatter） ([6938a10](https://github.com/koboriakira/article-hub/commit/6938a10348dfa32e697ad0f2de26db90909d5709))
* Qiita記事管理CLIプロジェクトの初期セットアップ ([cc23cf8](https://github.com/koboriakira/article-hub/commit/cc23cf8fe5890754d309d2d0c5b4928c36fa23c6))
* 記事校閲チームのサブエージェント定義（fact-checker, proofreader, copy-editor, orchestrator） ([24d30b1](https://github.com/koboriakira/article-hub/commit/24d30b1e7ee30b06c8116cb000e9229b3291fb60))

## [0.3.0](https://github.com/koboriakira/article-hub/compare/v0.2.0...v0.3.0) (2026-01-02)


### Features

* add fastapi ([#16](https://github.com/koboriakira/article-hub/issues/16)) ([bfb1cf6](https://github.com/koboriakira/article-hub/commit/bfb1cf607fd7d176e3b21c4f2630802b7c2cd6c3))

## [0.2.0](https://github.com/koboriakira/article-hub/compare/v0.1.1...v0.2.0) (2026-01-01)


### Features

* プロジェクトテンプレート化機能の実装 ([#11](https://github.com/koboriakira/article-hub/issues/11)) ([50a3309](https://github.com/koboriakira/article-hub/commit/50a3309976a643a9bd0c921940f729c48186e1dd))


### Bug Fixes

* Update README and install script for improved project setup instructions ([#13](https://github.com/koboriakira/article-hub/issues/13)) ([7c5e88c](https://github.com/koboriakira/article-hub/commit/7c5e88cfb8e7414195b5e275693d250f6adb0a8d))

## [0.1.1](https://github.com/koboriakira/article-hub/compare/v0.1.0...v0.1.1) (2026-01-01)


### Bug Fixes

* TestPyPI Trusted Publisher用にenvironment設定を追加 ([#8](https://github.com/koboriakira/article-hub/issues/8)) ([51a7431](https://github.com/koboriakira/article-hub/commit/51a7431ff16fbdcc5e43c5faf825c76f1af02e83))

## 0.1.0 (2026-01-01)


### Features

* 2026年最新Python開発テンプレート初期作成 ([5981110](https://github.com/koboriakira/article-hub/commit/59811108ece62d1b869abc820c55ec1b77cf13b0))


### Bug Fixes

* CIのセキュリティ監査でpip-auditが見つからない問題を修正 ([d623a65](https://github.com/koboriakira/article-hub/commit/d623a6597347358220e3847a2048ef7d65477cdd))
* GitHub Actions CI依存関係インストールエラーを修正 ([#4](https://github.com/koboriakira/article-hub/issues/4)) ([445af52](https://github.com/koboriakira/article-hub/commit/445af520cc2756d331eceb9b595d72083d275b37))
* mypy設定のパッケージ名にスラッシュが含まれていた問題を修正 ([1324114](https://github.com/koboriakira/article-hub/commit/132411404699aeab60881b83e00deb2656077cac))
* release-please GitHub Actions権限エラーを修正 ([#2](https://github.com/koboriakira/article-hub/issues/2)) ([42f7871](https://github.com/koboriakira/article-hub/commit/42f78712fb912d58245eb16769993decd0634de8))


### Documentation

* Claude Code機能統合とワークフロー最適化 ([#3](https://github.com/koboriakira/article-hub/issues/3)) ([09af203](https://github.com/koboriakira/article-hub/commit/09af2033e9cd0a3b79dda323e65b274e080158f7))
* Update GITHUB_SETUP.md to include Codecov configuration and error resolution ([#5](https://github.com/koboriakira/article-hub/issues/5)) ([836c6e0](https://github.com/koboriakira/article-hub/commit/836c6e01b306d3e74ab1de8f641e4061963c2a66))

## [Unreleased]

### Features

- 初期プロジェクト作成
- uv、ruff、pytest、mypy統合
- release-pleaseによる自動リリース管理
- CLIアプリケーション（typer + rich）
- 包括的なテストスイート
- GitHub Actions CI/CDパイプライン
- pre-commit品質管理フック
