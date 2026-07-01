"""
notes_core.py
İş mantığının kendisi: not ekleme, arama, son kayıtları listeleme.
Bu fonksiyonlar Faz 2'de MCP server tarafından doğrudan çağrılacak.
"""
import re
from datetime import datetime, timezone
from db import get_connection, init_db

def _clean_tags(tags: str) -> str:
    """Etiketlerdeki fazla boşlukları temizler ve virgülle ayırır."""
    if not tags:
        return ""
    return ",".join([t.strip() for t in tags.split(",") if t.strip()])

def log_note(content: str, tags: str = "") -> dict:
    """Yeni bir not ekler, eklenen kaydı döner."""
    if not content or not content.strip():
        raise ValueError("Not içeriği boş olamaz.")
    
    cleaned_tags = _clean_tags(tags)
    
    conn = get_connection()
    cur = conn.cursor()
    created_at = datetime.now(timezone.utc).isoformat()
    cur.execute(
        "INSERT INTO notes (content, tags, created_at) VALUES (?, ?, ?)",
        (content.strip(), cleaned_tags, created_at),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "content": content.strip(), "tags": cleaned_tags, "created_at": created_at}

def delete_note(note_id: int) -> bool:
    """Belirtilen ID'li notu siler."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success

def update_note(note_id: int, content: str, tags: str = None) -> bool:
    """Belirtilen ID'li notun içeriğini ve opsiyonel olarak etiketlerini günceller."""
    if not content or not content.strip():
        raise ValueError("Not içeriği boş olamaz.")
        
    conn = get_connection()
    cur = conn.cursor()
    
    # Eğer etiketler de gönderildiyse temizleyerek güncelle (Madde 3)
    if tags is not None:
        cleaned_tags = _clean_tags(tags)
        cur.execute(
            "UPDATE notes SET content = ?, tags = ? WHERE id = ?", 
            (content.strip(), cleaned_tags, note_id)
        )
    else:
        # Sadece içeriği güncelle
        cur.execute(
            "UPDATE notes SET content = ? WHERE id = ?", 
            (content.strip(), note_id)
        )
        
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success

def search_notes(query: str, limit: int = 5) -> list[dict]:
    """FTS5 ile arama yapar, en alakalı sonuçları döner."""
    if not query or not query.strip():
        return []
        
    conn = get_connection()
    cur = conn.cursor()
    
    # Sadece alfanumerik karakterleri ve boşluğu bırakıp FTS5'i bozacak karakterleri temizliyoruz
    cleaned_query = re.sub(r'[^\w\s]', '', query)
    if not cleaned_query.strip():
        conn.close()
        return []
        
    search_term = f"{cleaned_query.strip()}*"
    
    cur.execute(
        """
        SELECT notes.id, notes.content, notes.tags, notes.created_at
        FROM notes_fts
        JOIN notes ON notes.id = notes_fts.rowid
        WHERE notes_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (search_term, limit),
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
        if len(sys.argv) < 4:
            print("Kullanım:  python notes_core.py update <id> '<yeni metin>' [yeni etiketler]")
            sys.exit(1)
        note_id = int(sys.argv[2])
        content = sys.argv[3]
        tags = sys.argv[4] if len(sys.argv) > 4 else None
        
        if update_note(note_id, content, tags):
            print(f"ID {note_id} güncellendi.")
        else:
            print("Not bulunamadı.")

    else:
        print(f"Bilinmeyen komut: {command}")