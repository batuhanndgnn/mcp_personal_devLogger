# MCP Personal Dev Logger

Claude Desktop için geliştirilmiş, Model Context Protocol (MCP) tabanlı yerel bir geliştirici günlüğü ve hata takip sunucusu.

## Proje Hakkında

Yazılım geliştirme süreçlerinde karşılaşılan spesifik hatalar, framework davranışları ve bulunan çözümler genellikle dağınık halde kalır. Bu proje, yerel bilgisayarınızda çalışan bir SQLite veritabanını MCP üzerinden doğrudan Claude Desktop'a bağlar. Claude, otonom olarak hata notlarınızı kaydedebilir ve geçmişteki çözümlerinizi size hatırlatabilir.

## Kurulum ve Çalıştırma

### 1. Hazırlık ve Sanal Ortam

Projeyi klonladıktan sonra temiz bir çalışma ortamı oluşturun:

```bash
# Sanal ortam oluşturma
python -m venv venv

# Sanal ortamı aktif etme
# Windows için (Eğer hata alırsanız Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process kullanın):
.\venv\Scripts\activate

# Linux/macOS için:
source venv/bin/activate

```

### 2. Gereksinimleri Yükleyin

Projenin tek dış bağımlılığı resmi Anthropic MCP SDK'sıdır:

```bash
pip install mcp

```

### 3. Veritabanını Hazırlayın

Veritabanı dosyasını ve tabloları oluşturmak için başlatma betiğini çalıştırın:

```bash
python db.py

```

*Not: Dosyaların bulunduğu dizinde olduğunuzdan emin olun.*

### 4. Claude Desktop Ayarları

Claude'un bu sunucuyla iletişim kurabilmesi için `claude_desktop_config.json` dosyanıza (Windows için: `%APPDATA%\Claude\claude_desktop_config.json`) aşağıdaki yapılandırmayı ekleyin:

```json
{
  "mcpServers": {
    "my-dev-logger": {
      "command": "python",
      "args": ["C:\\tam\\yol\\server.py"]
    }
  }
}

```

*Önemli: `C:\\tam\\yol\\server.py` kısmını kendi bilgisayarınızdaki dosya yoluyla değiştirmeyi unutmayın.*

---

## 💡 Kurulumda Karşılaşılabilecek Sorunlar

* **PowerShell Script Çalıştırma Hatası:** `.\venv\Scripts\activate` çalıştırırken "running scripts is disabled" hatası alırsanız, terminalinize şunu yazın: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
* **Dosya Bulunamadı Hatası:** `python db.py` komutunu çalıştırmadan önce `ls` (veya `dir`) komutuyla `db.py` ve `server.py` dosyalarının bulunduğunuz dizinde listelendiğinden emin olun.
* **Claude Bağlantısı:** Yapılandırmadan sonra Claude Desktop'ı mutlaka **tamamen kapatıp yeniden açın.** Başarılı bağlantıda Claude arayüzünde "my-dev-logger" sunucusunun aktif olduğunu göreceksiniz.

---

## Kullanım Örneği

Konfigürasyonu tamamladıktan sonra:

* **Not Ekleme:** "Şunu not al: PostgreSQL 5432 port çakışması hatasını docker-compose içinde portu 5433:5432 yaparak çözdüm. Etiketler: docker, postgres"
* **Not Arama:** "Geçen ay aldığım Postgres port problemini nasıl çözmüştüm, veritabanımdan kontrol eder misin?"