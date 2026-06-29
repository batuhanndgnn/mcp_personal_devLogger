"""
notes_core.py
İş mantığının kendisi: not ekleme, arama, son kayıtları listeleme.
Bu fonksiyonlar Faz 2'de MCP server tarafından doğrudan çağrılacak,
şu an için sadece CLI'dan test ediyoruz.
"""

from datetime import datetime, timezone
from db import get_connection, init_db

def log_note(content: str, tags: str = "") -> dict:
    """Yeni bir not ekler, eklenen kaydı döner."""
    # DÜZELTME: Boş içerik kontrolü eklendi
    if not content or not content.strip():
        raise ValueError("Not içeriği boş olamaz.")
    
    conn = get_connection()
    cur = conn.cursor()
    created_at = datetime.now(timezone.utc).isoformat()
    cur.execute(
        "INSERT INTO notes (content, tags, created_at) VALUES (?, ?, ?)",
        (content.strip(), tags, created_at),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "content": content.strip(), "tags": tags, "created_at": created_at}

# YENİ EK: Silme fonksiyonu
def delete_note(note_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success

# YENİ EK: Güncelleme fonksiyonu
def update_note(note_id: int, content: str) -> bool:
    if not content or not content.strip():
        raise ValueError("Not içeriği boş olamaz.")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE notes SET content = ? WHERE id = ?", (content.strip(), note_id))
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success

def search_notes(query: str, limit: int = 5) -> list[dict]:
    """FTS5 ile arama yapar, en alakalı sonuçları döner."""
    conn = get_connection()
    cur = conn.cursor()
    # DÜZELTME: Tırnak işareti hatasını önlemek için temizlik
    safe_query = f'"{query.replace("\"", "")}"'
    cur.execute(
        """
        SELECT notes.id, notes.content, notes.tags, notes.created_at
        FROM notes_fts
        JOIN notes ON notes.id = notes_fts.rowid
        WHERE notes_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (safe_query, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_recent_notes(limit: int = 10) -> list[dict]:
    """En son eklenen N kaydı döner."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, content, tags, created_at FROM notes ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  python notes_core.py add '<not metni>' [etiket1,etiket2]")
        print("  python notes_core.py search '<arama kelimesi>'")
        print("  python notes_core.py recent [limit]")
        print("  python notes_core.py delete <id>")
        print("  python notes_core.py update <id> '<yeni metin>'")
        sys.exit(0)

    command = sys.argv[1]

    if command == "add":
        content = sys.argv[2]
        tags = sys.argv[3] if len(sys.argv) > 3 else ""
        result = log_note(content, tags)
        print(f"Kaydedildi (ID: {result['id']}): {result['content']}")

    elif command == "search":
        query = sys.argv[2]
        results = search_notes(query)
        if not results:
            print("Sonuç bulunamadı.")
        for r in results:
            print(f"[{r['id']}] {r['content']} (etiketler: {r['tags']}) - {r['created_at']}")

    elif command == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        results = get_recent_notes(limit)
        for r in results:
            print(f"[{r['id']}] {r['content']} (etiketler: {r['tags']}) - {r['created_at']}")
            
    elif command == "delete":
        note_id = int(sys.argv[2])
        if delete_note(note_id):
            print(f"ID {note_id} silindi.")
        else:
            print("Not bulunamadı.")
            
    elif command == "update":
        note_id = int(sys.argv[2])
        content = sys.argv[3]
        if update_note(note_id, content):
            print(f"ID {note_id} güncellendi.")
        else:
            print("Not bulunamadı.")

    else:
        print(f"Bilinmeyen komut: {command}")