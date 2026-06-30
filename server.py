"""
server.py
notes_core.py'deki fonksiyonları MCP tool'larına çeviren server.
Claude Desktop bu dosyayı stdio üzerinden çalıştırarak tool'lara erişir.
"""

import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP
import notes_core
from db import init_db


# Kurumsal Loglama Ayarları
log_path = Path(__file__).parent / "server.log"
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Server başlarken veritabanının hazır olduğundan emin oluyoruz
try:
    init_db()
    logging.info("Veritabanı bağlantısı başarılı ve şema hazır.")
except Exception as e:
    logging.critical(f"Veritabanı başlatılamadı: {str(e)}")

mcp = FastMCP("personal-notes")

@mcp.tool()
def log_note(content: str, tags: str = "") -> str:
    """Yeni bir teknik not/hata kaydı ekler."""
    try:
        res = notes_core.log_note(content, tags)
        logging.info(f"Yeni not eklendi. ID: {res['id']}")
        return f"Kaydedildi (ID: {res['id']}): {res['content']}"
    except ValueError as e:
        logging.warning(f"Geçersiz not ekleme girişimi: {str(e)}")
        return f"Hata: {str(e)}"
    except Exception as e:
        logging.error(f"Not eklenirken beklenmedik hata: {str(e)}")
        return f"Hata: {str(e)}"

@mcp.tool()
def delete_note(note_id: int) -> str:
    """Belirtilen ID'li notu siler."""
    try:
        if notes_core.delete_note(note_id):
            logging.info(f"Not silindi. ID: {note_id}")
            return f"ID {note_id} silindi."
        logging.warning(f"Silinmek istenen not bulunamadı. ID: {note_id}")
        return "Not bulunamadı."
    except Exception as e:
        logging.error(f"Not silinirken hata (ID: {note_id}): {str(e)}")
        return f"Hata: {str(e)}"

@mcp.tool()
def update_note(note_id: int, content: str, tags: str = None) -> str:
    """Belirtilen ID'li notun içeriğini ve opsiyonel olarak etiketlerini günceller."""
    try:
        if notes_core.update_note(note_id, content, tags):
            logging.info(f"Not güncellendi. ID: {note_id}")
            return "Başarıyla güncellendi."
        logging.warning(f"Güncellenmek istenen not bulunamadı. ID: {note_id}")
        return "Not bulunamadı."
    except ValueError as e:
        logging.warning(f"Geçersiz not güncelleme girişimi (ID: {note_id}): {str(e)}")
        return f"Hata: {str(e)}"
    except Exception as e:
        logging.error(f"Not güncellenirken hata (ID: {note_id}): {str(e)}")
        return f"Hata: {str(e)}"

@mcp.tool()
def search_notes(query: str, limit: int = 5) -> str:
    """Geçmiş notlarda/hatalarda arama yapar."""
    try:
        results = notes_core.search_notes(query, limit)
        if not results:
            logging.info(f"Arama yapıldı ancak sonuç bulunamadı. Sorgu: '{query}'")
            return f"'{query}' için sonuç bulunamadı."

        logging.info(f"Arama yapıldı. Sorgu: '{query}' - Sonuç sayısı: {len(results)}")
        lines = [f"'{query}' için {len(results)} sonuç bulundu:"]
        for r in results:
            lines.append(f"- [ID {r['id']}] {r['content']} (etiketler: {r['tags']}, tarih: {r['created_at']})")
        return "\n".join(lines)
    except Exception as e:
        logging.error(f"Arama işlemi başarısız (Sorgu: '{query}'): {str(e)}")
        return f"Hata: {str(e)}"

@mcp.tool()
def get_recent_notes(limit: int = 10) -> str:
    """En son eklenen notları listeler."""
    try:
        results = notes_core.get_recent_notes(limit)
        if not results:
            return "Henüz hiç not kaydedilmemiş."
            
        logging.info(f"Son {len(results)} not listelendi.")
        lines = [f"En son eklenen {len(results)} not:"]
        for r in results:
            lines.append(f"- [ID {r['id']}] {r['content']} (etiketler: {r['tags']}, tarih: {r['created_at']})")
        return "\n".join(lines)
    except Exception as e:
        logging.error(f"Son notları getirme işlemi başarısız: {str(e)}")
        return f"Hata: {str(e)}"