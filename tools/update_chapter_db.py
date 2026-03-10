#!/usr/bin/env python3
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "chapters"
DB_PATH = ROOT / "novel.db"

MIN_CHARS = 1500
MAX_CHARS = 2200


def count_chars(text: str) -> int:
    body = "".join(ch for ch in text if ch not in {" ", "\n", "\r", "\t"})
    return len(body)


def parse_title(text: str, default: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return default


def main() -> None:
    chapter_files = sorted(CHAPTER_DIR.glob("chapter_*.md"))
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

    for chapter_file in chapter_files:
        text = chapter_file.read_text(encoding="utf-8")
        char_count = count_chars(text)
        if not (MIN_CHARS <= char_count <= MAX_CHARS):
            raise SystemExit(
                f"{chapter_file.name} 字数 {char_count} 不在 {MIN_CHARS}-{MAX_CHARS} 区间"
            )

        chapter_no = int(chapter_file.stem.split("_")[1])
        title = parse_title(text, chapter_file.stem)

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        hook = lines[-1] if lines else ""

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
    print(f"Updated {len(chapter_files)} chapters into {DB_PATH.name}")


if __name__ == "__main__":
    main()
