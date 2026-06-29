"""
db.py
Veritabanı bağlantısı ve şema kurulumu.
Bu modül, hem Faz 1'deki CLI test scripti hem de Faz 2'deki MCP server
tarafından ortak olarak kullanılacak.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "notes.db"


def get_connection() -> sqlite3.Connection:
    """Veritabanı bağlantısını döner, yoksa dosyayı oluşturur."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Tabloları ve FTS5 sanal tablosunu, yoksa oluşturur."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tags TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
            content,
            tags,
            content='notes',
            content_rowid='id'
        )
        """
    )

    # notes tablosuna ekleme/güncelleme/silme oldukça notes_fts'i senkron tutan triggerlar
    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
            INSERT INTO notes_fts(rowid, content, tags) VALUES (new.id, new.content, new.tags);
        END
        """
    )

    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
            INSERT INTO notes_fts(notes_fts, rowid, content, tags) VALUES ('delete', old.id, old.content, old.tags);
        END
        """
    )

    cur.execute(
        """
        CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
            INSERT INTO notes_fts(notes_fts, rowid, content, tags) VALUES ('delete', old.id, old.content, old.tags);
            INSERT INTO notes_fts(rowid, content, tags) VALUES (new.id, new.content, new.tags);
        END
        """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Veritabanı hazır: {DB_PATH}")