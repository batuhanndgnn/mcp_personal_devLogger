Tamamdır, README dosyanı konuştuğumuz eksikleri (gereksiz veritabanı adımı, venv yolu, requirements.txt mantığı) giderecek şekilde baştan aşağı düzenledim. Doğrudan kopyalayıp kendi `README.md` dosyanın içine yapıştırabilirsin:

```markdown
# MCP Personal Dev Logger

Claude Desktop için geliştirilmiş, Model Context Protocol (MCP) tabanlı yerel bir geliştirici günlüğü ve hata takip sunucusu.

## Proje Hakkında

Yazılım geliştirme süreçlerinde karşılaşılan spesifik hatalar, framework davranışları ve çözümler genellikle not defterlerinde veya mesajlaşma kanallarında dağınık halde kalır. Aynı sorunla aylar sonra tekrar karşılaşıldığında çözüm sürecini hatırlamak ciddi bir zaman kaybına yol açar.

Bu proje, yerel bilgisayarınızda çalışan bir SQLite veritabanını Anthropic'in Model Context Protocol (MCP) standardı üzerinden doğrudan Claude Desktop'a bağlar. Claude, sohbet sırasında otonom olarak hata notlarınızı kaydedebilir ve geçmişte karşılaştığınız bir sorunu sorduğunuzda veritabanınızı tarayarak size eski çözümünüzü sunabilir.

## Sistem Mimarisi ve Tasarım Kararları

Proje, gereksiz karmaşıklıktan ve dış bağımlılıklardan kaçınılarak sade bir yapıda tasarlanmıştır:

* **Sıfır Kurulumlu Veritabanı:** Sunucu ayağa kalktığında veritabanı şemasını otonom olarak hazırlar. Arama işlemleri için karmaşık vektör veritabanları yerine SQLite'ın yerleşik FTS5 (Full-Text Search) eklentisi kullanılmıştır.
* **Tamamen Yerel İletişim:** Sunucu, standart girdi/çıktı (stdio) üzerinden Claude ile haberleşir. Ağ yapılandırması veya port ayarı gerektirmez; verileriniz bilgisayarınızdan dışarı çıkmaz.
* **Doğrudan Orkestrasyon:** LangChain gibi ek çerçeveler kullanılmamıştır. İstek analizi ve araç seçimi, Claude'un kendi otonom döngüsüne (ReAct) bırakılmıştır.

## Sunulan Araçlar (MCP Tools)

* `log_note(content, tags)`: SQLite veritabanına yeni bir hata veya çözüm kaydı ile ilgili etiketleri ekler.
* `search_notes(query)`: FTS5 altyapısını kullanarak geçmiş notlarda metin tabanlı arama yapar ve en alakalı sonuçları Claude'a iletir.
* `get_recent_notes(limit)`: Tarihe göre en son kaydedilen notları listeler.

## Kurulum ve Çalıştırma

### 1. Hazırlık ve Sanal Ortam

Projeyi klonladıktan sonra temiz bir çalışma ortamı oluşturun:

```bash
# Sanal ortam oluşturma
python -m venv venv

# Sanal ortamı aktif etme (Windows)
.\venv\Scripts\activate

# Sanal ortamı aktif etme (Linux/macOS)
source venv/bin/activate

```

*Not: Windows üzerinde `.\venv\Scripts\activate` çalıştırırken "running scripts is disabled" hatası alırsanız, `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` komutunu kullanarak yetki verebilirsiniz.*

### 2. Gereksinimleri Yükleyin

Projenin bağımlılıklarını kurmak için ana dizindeki `requirements.txt` dosyasını kullanın:

```bash
pip install -r requirements.txt

```

### 3. Claude Desktop Ayarları

Claude'un bu sunucuyla iletişim kurabilmesi için `claude_desktop_config.json` dosyanızı yapılandırın:

1. **Dosyayı Açın:** Claude Desktop uygulamasını açın.
2. **Ayarlar:** Menü çubuğundan `File` > `Settings` (Mac üzerinde `Claude` > `Settings`) yolunu izleyin.
3. **Developer:** `Developer` sekmesine tıklayın.
4. **Edit Config:** `Edit Config` butonuna basarak `claude_desktop_config.json` dosyasını açın.
5. **Düzenleyin:** Dosya içeriğine aşağıdakini ekleyin (eğer dosya mevcut değilse bu konumda oluşturun: Windows için `%APPDATA%\Claude\claude_desktop_config.json`, Mac için `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-dev-logger": {
      "command": "C:\\tam\\yol\\venv\\Scripts\\python.exe",
      "args": ["C:\\tam\\yol\\server.py"]
    }
  }
}

```

*Önemli: `command` kısmına mutlaka projede oluşturduğunuz sanal ortamın (`venv`) içindeki `python.exe` yolunu vermelisiniz. Sisteminizdeki global `python` komutunu kullanmak uygulamanın çökmesine neden olabilir. `args` kısmına ise `server.py` dosyasının tam yolunu yazın. Konfigürasyondan sonra Claude Desktop'ı tamamen kapatıp yeniden başlatın.*

## ⚠️ Gelişmiş Sorun Giderme

* **Sunucu Başlatılamıyor (Kırmızı İkon):** Claude Desktop, sanal ortamdaki `python.exe` dosyasını bulamıyor olabilir. Yolların doğru olduğundan ve çift ters eğik çizgi (`\\`) ile yazıldığından emin olun.
* **JSON Yapısal Hataları:** Konfigürasyon dosyasında eksik parantez veya fazladan virgül bulunması Claude'un dosyayı tamamen yok saymasına neden olur. JSON formatınızı kontrol ettiğinizden emin olun.
* **Python Sürüm Uyumluluğu:** MCP SDK'sının kararlı çalışması için Python 3.10 veya daha yeni bir sürüm kullanmanız önerilir.

## Kullanım Örneği

Konfigürasyonu tamamladıktan sonra sohbet penceresinden asistanla iletişime geçebilirsiniz:

* **Not Ekleme:** "Şunu not al: PostgreSQL 5432 port çakışması hatasını, docker-compose.yml içindeki port eşleştirmesini 5433:5432 yaparak çözdüm. Etiketler: docker, postgres"
* **Not Arama:** "Geçen ay aldığım Postgres port problemini nasıl çözmüştüm, veritabanımdan kontrol eder misin?"

```

Bunu kopyalayıp kaydettikten sonra hazır olduğunda ses et, kod tarafındaki ("motor") değişiklikler için nereye el atacağımızı sen söyle.

```