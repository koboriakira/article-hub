"""メインアプリケーション"""

from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .qiita.client import QiitaApiError, QiitaClient
from .qiita.frontmatter import parse_markdown_file
from .qiita.models import QiitaItemRequest

app = typer.Typer(
    name="article-hub",
    help="Qiita 記事の投稿・更新 CLI ツール",
    add_completion=False,
)
console = Console()


def _get_token() -> str | None:
    """環境変数から Qiita トークンを取得"""
    import os

    load_dotenv(Path.cwd() / ".env.local")
    load_dotenv()
    return os.environ.get("QIITA_ACCESS_TOKEN")


@app.command()
def hello(name: str = typer.Option("World", help="挨拶する相手の名前")) -> None:
    """挨拶を表示します"""
    console.print(
        Panel(
            f"[bold green]こんにちは、{name}![/bold green]",
            title="Python Project 2026",
            border_style="blue",
        )
    )


@app.command()
def version() -> None:
    """バージョン情報を表示します"""
    console.print(f"Python Project 2026 version: [bold]{__version__}[/bold]")


@app.command(name="list")
def list_items(
    page: int = typer.Option(1, help="ページ番号"),
    per_page: int = typer.Option(20, help="1ページあたりの件数"),
) -> None:
    """自分の Qiita 記事一覧を表示します"""
    token = _get_token()
    if not token:
        console.print("[red]QIITA_ACCESS_TOKEN が設定されていません[/red]")
        raise typer.Exit(code=1)

    try:
        with QiitaClient(token=token) as client:
            items = client.list_items(page=page, per_page=per_page)
    except QiitaApiError as e:
        console.print(f"[red]API エラー: {e}[/red]")
        raise typer.Exit(code=1) from e

    if not items:
        console.print("記事が見つかりませんでした")
        return

    table = Table(title="Qiita 記事一覧")
    table.add_column("ID", style="dim")
    table.add_column("タイトル", style="bold")
    table.add_column("タグ")
    table.add_column("公開", justify="center")
    table.add_column("更新日")

    for item in items:
        tags = ", ".join(tag.name for tag in item.tags)
        visibility = "限定" if item.private else "公開"
        table.add_row(item.id, item.title, tags, visibility, item.updated_at[:10])

    console.print(table)


@app.command()
def post(
    file_path: Path = typer.Argument(..., help="投稿する Markdown ファイルのパス"),
    private: bool = typer.Option(False, help="限定公開にする"),
) -> None:
    """Markdown ファイルを Qiita に投稿します"""
    token = _get_token()
    if not token:
        console.print("[red]QIITA_ACCESS_TOKEN が設定されていません[/red]")
        raise typer.Exit(code=1)

    try:
        frontmatter, body = parse_markdown_file(file_path)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[red]ファイルエラー: {e}[/red]")
        raise typer.Exit(code=1) from e

    request = QiitaItemRequest(
        title=frontmatter.title,
        body=body,
        tags=frontmatter.to_qiita_tags(),
        private=private or frontmatter.private,
    )

    try:
        with QiitaClient(token=token) as client:
            result = client.create_item(request)
    except QiitaApiError as e:
        console.print(f"[red]API エラー: {e}[/red]")
        raise typer.Exit(code=1) from e

    console.print(f"[green]投稿しました![/green] ID: {result.id}")
    console.print(f"URL: {result.url}")


@app.command()
def update(
    file_path: Path = typer.Argument(..., help="更新する Markdown ファイルのパス"),
    item_id: str | None = typer.Option(None, "--id", help="Qiita 記事 ID (frontmatter の qiita_id より優先)"),
) -> None:
    """既存の Qiita 記事を更新します"""
    token = _get_token()
    if not token:
        console.print("[red]QIITA_ACCESS_TOKEN が設定されていません[/red]")
        raise typer.Exit(code=1)

    try:
        frontmatter, body = parse_markdown_file(file_path)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[red]ファイルエラー: {e}[/red]")
        raise typer.Exit(code=1) from e

    target_id = item_id or frontmatter.qiita_id
    if not target_id:
        console.print(
            "[red]記事 ID が指定されていません。--id オプションか frontmatter の qiita_id を設定してください[/red]"
        )
        raise typer.Exit(code=1)

    request = QiitaItemRequest(
        title=frontmatter.title,
        body=body,
        tags=frontmatter.to_qiita_tags(),
        private=frontmatter.private,
    )

    try:
        with QiitaClient(token=token) as client:
            result = client.update_item(target_id, request)
    except QiitaApiError as e:
        console.print(f"[red]API エラー: {e}[/red]")
        raise typer.Exit(code=1) from e

    console.print(f"[green]更新しました![/green] ID: {result.id}")
    console.print(f"URL: {result.url}")


if __name__ == "__main__":
    app()
