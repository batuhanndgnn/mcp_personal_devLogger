# MCP Personal Dev Logger

Claude Desktop için geliştirilmiş, Model Context Protocol (MCP) tabanlı yerel bir geliştirici günlüğü ve hata takip sunucusu.

## Proje Hakkında

Yazılım geliştirme süreçlerinde karşılaşılan spesifik hatalar, framework davranışları ve bulunan çözümler genellikle not defterlerinde veya Slack/Discord gibi kanallarda dağınık halde kalır. Aynı hatayla aylar sonra tekrar karşılaşıldığında, çözümü hatırlamak ve bulmak ciddi bir zaman kaybı yaratır.

Bu proje, yerel bilgisayarınızda çalışan bir SQLite veritabanını Anthropic'in Model Context Protocol (MCP) standardı üzerinden doğrudan Claude Desktop'a bağlar. Bu sayede Claude, sohbet sırasında otonom olarak hata notlarınızı kaydedebilir ve geçmişte karşılaştığınız bir sorunu sorduğunuzda veritabanınızı tarayarak size eski çözümünüzü getirebilir.

## Sistem Mimarisi ve Tasarım Kararları

Proje, gereksiz karmaşıklıktan ve dış bağımlılıklardan kaçınılarak en sade şekilde çalışacak biçimde tasarlanmıştır:

* **Sıfır Kurulumlu Veritabanı:** Arama işlemleri için karmaşık vektör veritabanları yerine SQLite'ın yerleşik FTS5 (Full-Text Search) eklentisi kullanılmıştır. Bu sayede sistem, ekstra bir kurulum veya maliyet gerektirmeden hızlı kelime bazlı aramalar yapabilir.
* **Tamamen Yerel (Local) İletişim:** Sunucu, standart girdi/çıktı (stdio) üzerinden Claude ile haberleşir. Ağ yapılandırması veya port ayarı gerektirmez, kişisel loglarınız bilgisayarınızdan dışarı çıkmaz.
* **Doğrudan Orkestrasyon:** LangChain gibi ekstra çerçeveler kullanılmamıştır. İsteklerin analizi ve hangi aracın (tool) çalıştırılacağı kararı tamamen Claude'un kendi otonom döngüsüne (ReAct) bırakılmıştır.

## Sunulan Araçlar (MCP Tools)

Claude'un kullanımına sunulan araçlar:

* **log_note(content, tags):** SQLite veritabanına yeni bir hata/çözüm kaydı ve ilgili etiketleri ekler.
* **search_notes(query):** FTS5 altyapısını kullanarak geçmiş notlarda metin tabanlı arama yapar ve en alakalı sonuçları Claude'a iletir.
* **get_recent_notes(limit):** Tarihe göre en son kaydedilen notları listeler.
* **update_note(note_id, content):** Yanlış veya eksik kaydedilmiş bir notu günceller.
* **delete_note(note_id):** Artık ihtiyaç duyulmayan veya geçersiz olan notu siler.

## Kurulum ve Çalıştırma

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

* **Mac için:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows için:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-dev-logger": {
      "command": "python",
      "args": ["/projenin/tam/yolu/server.py"]
    }
  }
}

```

## Kullanım Örneği

Konfigürasyonu tamamlayıp Claude Desktop'ı yeniden başlattıktan sonra, standart sohbet penceresinden asistanla iletişim kurabilirsiniz:

* **Not Ekleme:** "Şunu not al: PostgreSQL 5432 port çakışması hatasını, docker-compose.yml içindeki port eşleştirmesini 5433:5432 yaparak çözdüm. Etiketler: docker, postgres"
* **Not Arama:** "Geçen ay aldığım Postgres port problemini nasıl çözmüştüm, veritabanımdan kontrol eder misin?"