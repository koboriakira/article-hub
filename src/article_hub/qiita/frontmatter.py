"""Markdown frontmatter パーサー"""

from pathlib import Path

import yaml
from pydantic import ValidationError

from .models import ArticleFrontmatter


def parse_markdown_file(path: Path) -> tuple[ArticleFrontmatter, str]:
    """Markdown ファイルを読み込み、frontmatter と本文に分割する。

    Args:
        path: Markdown ファイルのパス

    Returns:
        (ArticleFrontmatter, 本文テキスト) のタプル

    Raises:
        FileNotFoundError: ファイルが存在しない場合
        ValueError: frontmatter が不正な場合
    """
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {path}")

    content = path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        msg = "frontmatter が見つかりません (--- で始まる必要があります)"
        raise ValueError(msg)

    end_index = content.index("---", 3)
    yaml_str = content[3:end_index].strip()
    body = content[end_index + 3 :].strip()

    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        msg = f"YAML のパースに失敗しました: {e}"
        raise ValueError(msg) from e

    if not isinstance(data, dict):
        msg = "frontmatter が不正です (YAML が辞書形式ではありません)"
        raise ValueError(msg)

    try:
        frontmatter = ArticleFrontmatter.model_validate(data)
    except ValidationError as e:
        msg = str(e)
        raise ValueError(msg) from e

    return frontmatter, body
