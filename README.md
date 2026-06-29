
```markdown
# MCP Personal Dev Logger

Claude Desktop için geliştirilmiş, Model Context Protocol (MCP) tabanlı yerel bir geliştirici günlüğü ve hata takip sunucusu.

## 📝 Proje Hakkında
Yazılım geliştirme süreçlerinde karşılaşılan spesifik hatalar, framework davranışları ve bulunan çözümler genellikle not defterlerinde veya Slack/Discord gibi kanallarda dağınık halde kalır. Aynı hatayla aylar sonra tekrar karşılaşıldığında, çözümü hatırlamak ciddi bir zaman kaybı yaratır.

Bu proje, yerel bilgisayarınızda çalışan bir SQLite veritabanını Anthropic'in Model Context Protocol (MCP) standardı üzerinden doğrudan Claude Desktop'a bağlar. Bu sayede Claude, sohbet sırasında otonom olarak hata notlarınızı kaydedebilir ve geçmişte karşılaştığınız bir sorunu sorduğunuzda veritabanınızı tarayarak size çözümünüzü sunabilir.

## 🏗 Sistem Mimarisi ve Tasarım Kararları
Proje, gereksiz karmaşıklıktan ve dış bağımlılıklardan kaçınılarak en sade şekilde çalışacak biçimde tasarlanmıştır:

*   **Sıfır Kurulumlu Veritabanı:** Arama işlemleri için karmaşık vektör veritabanları yerine SQLite'ın yerleşik FTS5 (Full-Text Search) eklentisi kullanılmıştır. Ekstra kurulum gerektirmez.
*   **Tamamen Yerel (Local) İletişim:** Sunucu, standart girdi/çıktı (stdio) üzerinden Claude ile haberleşir. Kişisel loglarınız bilgisayarınızdan dışarı çıkmaz.
*   **Doğrudan Orkestrasyon:** LangChain gibi ekstra çerçeveler kullanılmamıştır. İsteklerin analizi Claude'un kendi otonom döngüsüne bırakılmıştır.

## 🛠 Sunulan Araçlar (MCP Tools)

*   **log_note(content, tags)**: Yeni bir teknik not veya hata kaydı ekler.
*   **search_notes(query)**: FTS5 altyapısıyla notlarınızda metin tabanlı arama yapar.
*   **get_recent_notes(limit)**: Tarihe göre en son kaydedilen notları listeler.
*   **update_note(note_id, content)**: Yanlış veya eksik kaydedilmiş bir notu günceller.
*   **delete_note(note_id)**: Artık ihtiyaç duyulmayan veya geçersiz olan notu siler.

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

```

```