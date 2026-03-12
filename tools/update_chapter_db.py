#!/usr/bin/env python3
from __future__ import annotations

import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "chapters"
DB_PATH = ROOT / "novel.db"

MIN_CHARS = 1500
MAX_CHARS = 2200
CHAPTER_NO_RE = re.compile(r"第\s*(\d+)\s*章")


def count_chars(text: str) -> int:
    body = "".join(ch for ch in text if ch not in {" ", "\n", "\r", "\t"})
    return len(body)


def parse_title(text: str, default: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return default


def parse_chapter_no(title: str, filename: str) -> int:
    for source in (title, filename):
        match = CHAPTER_NO_RE.search(source)
        if match:
            return int(match.group(1))
    raise ValueError(f"无法从标题或文件名解析章节号: {filename}")


def main() -> None:
    chapter_files = sorted(CHAPTER_DIR.glob("*.md"))
    if not chapter_files:
        raise SystemExit("No chapter files found.")

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY,
            chapter_no INTEGER NOT NULL UNIQUE,
            title TEXT NOT NULL,
            file_path TEXT NOT NULL,
            char_count INTEGER NOT NULL,
            hook TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    items: list[tuple[int, Path, str, int, str]] = []
    for chapter_file in chapter_files:
        text = chapter_file.read_text(encoding="utf-8")
        char_count = count_chars(text)
        if not (MIN_CHARS <= char_count <= MAX_CHARS):
            raise SystemExit(
                f"{chapter_file.name} 字数 {char_count} 不在 {MIN_CHARS}-{MAX_CHARS} 区间"
            )

        title = parse_title(text, chapter_file.stem)
        chapter_no = parse_chapter_no(title, chapter_file.stem)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        hook = lines[-1] if lines else ""
        items.append((chapter_no, chapter_file, title, char_count, hook))

    for chapter_no, chapter_file, title, char_count, hook in sorted(items, key=lambda x: x[0]):
        conn.execute(
            """
            INSERT INTO chapters (chapter_no, title, file_path, char_count, hook, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(chapter_no) DO UPDATE SET
                title=excluded.title,
                file_path=excluded.file_path,
                char_count=excluded.char_count,
                hook=excluded.hook,
                updated_at=CURRENT_TIMESTAMP
            """,
            (chapter_no, title, str(chapter_file.relative_to(ROOT)), char_count, hook),
        )

    conn.commit()
    conn.close()
    print(f"Updated {len(items)} chapters into {DB_PATH.name}")


if __name__ == "__main__":
    main()
