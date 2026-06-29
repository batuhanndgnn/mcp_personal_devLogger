"""
server.py
notes_core.py'deki fonksiyonları MCP tool'larına çeviren server.
Claude Desktop (veya başka bir MCP host'u) bu dosyayı stdio üzerinden
çalıştırarak tool'lara erişir.
"""

from mcp.server.fastmcp import FastMCP
import notes_core
from db import init_db

# Server başlarken veritabanının/şemanın hazır olduğundan emin oluyoruz
init_db()

mcp = FastMCP("personal-notes")

@mcp.tool()
def log_note(content: str, tags: str = "") -> str:
    """
    Yeni bir teknik not/hata kaydı ekler.
    
    Args:
        content: Kaydedilecek notun/hatanın metni.
        tags: Virgülle ayrılmış etiketler.
    """
    try:
        res = notes_core.log_note(content, tags)
        return f"Kaydedildi (ID: {res['id']}): {res['content']}"
    except ValueError as e:
        return f"Hata: {str(e)}"

@mcp.tool()
def delete_note(note_id: int) -> str:
    """Belirtilen ID'li notu siler."""
    if notes_core.delete_note(note_id):
        return f"ID {note_id} silindi."
    return "Not bulunamadı."

@mcp.tool()
def update_note(note_id: int, content: str) -> str:
    """Belirtilen ID'li notun içeriğini günceller."""
    try:
        if notes_core.update_note(note_id, content):
            return "Başarıyla güncellendi."
        return "Not bulunamadı."
    except ValueError as e:
        return f"Hata: {str(e)}"

@mcp.tool()
def search_notes(query: str, limit: int = 5) -> str:
    """
    Geçmiş notlarda/hatalarda arama yapar.
    
    Args:
        query: Aranacak kelime veya ifade.
        limit: Döndürülecek maksimum sonuç sayısı (varsayılan 5).
    """
    results = notes_core.search_notes(query, limit)
    if not results:
        return f"'{query}' için sonuç bulunamadı."

    lines = [f"'{query}' için {len(results)} sonuç bulundu:"]
    for r in results:
        lines.append(f"- [ID {r['id']}] {r['content']} (etiketler: {r['tags']}, tarih: {r['created_at']})")
    return "\n".join(lines)

@mcp.tool()
def get_recent_notes(limit: int = 10) -> str:
    """
    En son eklenen notları listeler.
    
    Args:
        limit: Döndürülecek maksimum not sayısı (varsayılan 10).
    """
    results = notes_core.get_recent_notes(limit)
    if not results:
        return "Henüz hiç not kaydedilmemiş."

    lines = [f"Son {len(results)} not:"]
    for r in results:
        lines.append(f"- [ID {r['id']}] {r['content']} (etiketler: {r['tags']}, tarih: {r['created_at']})")
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run()