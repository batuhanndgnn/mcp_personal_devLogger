# MCP Personal Dev Logger

Claude Desktop için geliştirilmiş, Model Context Protocol (MCP) tabanlı yerel bir geliştirici günlüğü ve hata takip sunucusu.

## 🛠 Sunulan Araçlar (MCP Tools)

* **log_note(content, tags)**: Yeni bir teknik not veya hata kaydı ekler.
* **search_notes(query)**: FTS5 altyapısıyla notlarınızda metin tabanlı arama yapar.
* **get_recent_notes(limit)**: Tarihe göre en son kaydedilen notları listeler.
* **update_note(note_id, content)**: Yanlış veya eksik kaydedilmiş bir notu günceller.
* **delete_note(note_id)**: Artık ihtiyaç duyulmayan veya geçersiz olan notu siler.

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimleri Yükleyin

Projenin tek dış bağımlılığı resmi Anthropic MCP SDK'sıdır.

```bash
pip install mcp

```

### 2. Veritabanını Hazırlayın

Veritabanı dosyasını ve tabloları oluşturmak için başlatma betiğini çalıştırın:

```bash
python init_db.py

```

### 3. Claude Desktop Ayarları

Claude'un bu sunucuyla iletişim kurabilmesi için `claude_desktop_config.json` dosyanıza aşağıdaki yapılandırmayı ekleyin:

**Windows için yol:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-dev-logger": {
      "command": "python",
      "args": ["C:/projenin/tam/yolu/server.py"]
    }
  }
}

```

## 💡 Kullanım Örnekleri

* **Not Ekleme**: "Şunu not al: PostgreSQL port çakışması hatasını, docker-compose.yml içindeki port eşleştirmesini 5433:5432 yaparak çözdüm. Etiketler: docker, postgres"
* **Arama**: "Geçen ay aldığım Postgres port problemini nasıl çözmüştüm?"
* **Güncelleme**: "ID'si 5 olan nottaki çözüm adımına 'Ayrıca servisi restart etmeyi unutma' ifadesini ekle."
* **Silme**: "ID'si 3 olan not hatalıydı, onu veritabanından sil."