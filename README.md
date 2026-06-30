# MCP Personal Dev Logger

Claude Desktop için geliştirdiğim yerel bir geliştirici günlüğü ve hata takip aracı.

## Neden Yaptım?

Projelerde kod yazarken çözdüğüm hataları (port çakışmaları, framework sorunları vb.) bir yerlere not alıyordum ama sonra bulması işkence oluyordu. Bu projeyle, yerel bilgisayarımdaki bir SQLite veritabanını Model Context Protocol (MCP) ile doğrudan Claude Desktop'a bağladım. Artık Claude'a "şu hatayı şöyle çözdüm not al" diyorum, sonra lazım olunca "geçen ayki hatayı nasıl çözmüştük?" diye sorup cevabı alabiliyorum.

## Nasıl Çalışıyor?

Olabildiğince basit ve dışa bağımlılıksız tutmaya çalıştım:

* **Vektör DB Yok:** Karmaşık veri tabanları kurmak yerine doğrudan SQLite'ın yerleşik FTS5 (Full-Text Search) özelliğini kullandım.
* **Tamamen Yerel:** Her şey `stdio` üzerinden bilgisayarımda dönüyor, dışarı veri çıkmıyor.
* **Ekstra Kütüphane Yok:** LangChain vb. aracı katmanlar eklemedim, aracı seçme işini tamamen Claude'un kendi mantığına bıraktım.

## MCP Araçları

* `log_note(content, tags)`: Veritabanına yeni bir hata/çözüm notu ve etiketlerini ekler.
* `search_notes(query)`: Geçmiş notlar içinde arama yapar.
* `get_recent_notes(limit)`: En son eklenen notları getirir.
* `update_note(note_id, content, tags)`: Belirtilen ID'li notun içeriğini ve opsiyonel olarak etiketlerini günceller.
* `delete_note(note_id)`: Belirtilen ID'li notu siler.

## Kurulum

### 1. Sanal Ortam (Virtual Env)

Önce projeyi klonladığınız yerde temiz bir python ortamı oluşturun:

```bash
python -m venv venv
.\venv\Scripts\activate

```

*(Not: Windows'ta yetki hatası alırsanız PowerShell'i yönetici açıp `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` yazabilirsiniz)*
*(Not: .env dosyasına DB_PATH=yol/veritabani.db ekleyerek veritabanı dosyanızın konumunu değiştirebilirsiniz.)*

### 2. Kütüphaneleri Yükleme

Gerekli olan mcp kütüphanesini kuruyoruz:

```bash
pip install -r requirements.txt

```

### 3. Claude Desktop Ayarı

Claude'un bu sunucuyu görmesi için config dosyasını güncellememiz lazım.
Claude Desktop'ta `Settings > Developer > Edit Config` diyerek `claude_desktop_config.json` dosyasını açın ve içini şu şekilde düzenleyin:

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

**ÖNEMLİ:** `C:\\tam\\yol\\...` kısımlarını kendi bilgisayarınızdaki projenin gerçek yoluyla değiştirin. Sistemdeki global python yerine mutlaka projenin içindeki `venv` klasöründe bulunan `python.exe` yolunu vermelisiniz yoksa uygulama çalışmaz. Ayarı yaptıktan sonra Claude'u tamamen kapatıp yeniden açın.

## Nasıl Kullanılır?

Kurulum bitince Claude Desktop'ta normal sohbet eder gibi kullanabilirsiniz:

* "Şunu kaydet: Whatsapp botunda session çökme sorununu wwebjs_auth klasörünü silerek çözdüm. Etiketler: nodejs, whatsapp"
* "Ollama ile ilgili aldığım notlara bir baksana ne yazmışım"
* "5 numaralı notu sil"
* "3 numaralı notun etiketlerini güncelle"