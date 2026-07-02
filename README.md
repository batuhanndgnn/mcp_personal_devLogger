Harika fikir! O rozetler (badgeler) GitHub projelerine gerçekten çok profesyonel ve havalı bir görünüm katıyor.

Kurallarını tamamen uyguladım: Eski metninin tek bir noktasına bile dokunmadım, hiçbir şeyi silmedim. Sadece en üste istediğin o havalı rozetleri ekledim, İçindekiler kısmına Docker'ı ilave ettim ve "Kurulum" bölümünün en sonuna konuştuğumuz Docker adımlarını yerleştirdim.

Aşağıdaki metni kopyalayıp doğrudan `README.md` dosyanın içine yapıştırabilirsin:

```markdown
# MCP Personal Dev Logger

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-Ready-success.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Model Context Protocol (MCP) tabanlı, tamamen yerel çalışan geliştirici günlüğü ve hata takip sunucusu.**

Claude Desktop veya Cursor'a bağlanır, karşılaştığınız hataları ve çözümlerini doğal dille kaydetmenizi ve daha sonra yine doğal dille aramanızı sağlar. Veri hiçbir yere gönderilmez — her şey bilgisayarınızdaki bir SQLite dosyasında tutulur.

---

## İçindekiler

- [Neden Yaptım?](#neden-yaptım)
- [Nasıl Çalışıyor?](#nasıl-çalışıyor)
- [MCP Araçları](#mcp-araçları)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
  - [1. Projeyi İndirme](#1-projeyi-i̇ndirme)
  - [2. Sanal Ortam](#2-sanal-ortam-virtual-env)
  - [3. Bağımlılıkları Yükleme](#3-bağımlılıkları-yükleme)
  - [4. Claude Desktop Ayarı](#4-claude-desktop-ayarı)
  - [5. Cursor Ayarı](#5-cursor-ayarı)
  - [6. Docker ile Kurulum (Önerilen)](#6-docker-ile-kurulum-önerilen)
- [Kullanım Örnekleri](#kullanım-örnekleri)
- [Veritabanı Konumunu Değiştirme](#veritabanı-konumunu-değiştirme)
- [Sorun Giderme](#sorun-giderme)
- [Proje Yapısı](#proje-yapısı)
- [Geliştirme](#geliştirme)
- [Lisans](#lisans)

---

## Neden Yaptım?

Projelerde kod yazarken çözdüğüm hataları (port çakışmaları, framework sorunları, konfigürasyon tuzakları vb.) bir yerlere not alıyordum ama sonra bulması işkence oluyordu. Bu projeyle, yerel bilgisayarımdaki bir SQLite veritabanını Model Context Protocol (MCP) ile doğrudan Claude Desktop'a bağladım.

Artık Claude'a *"şu hatayı şöyle çözdüm not al"* diyorum, sonra lazım olunca *"geçen ayki hatayı nasıl çözmüştük?"* diye sorup cevabı alabiliyorum — ekstra bir uygulama açmadan, sohbetin içinde.

## Nasıl Çalışıyor?

Olabildiğince basit ve dışa bağımlılıksız tutmaya çalıştım:

- **Vektör DB Yok:** Karmaşık vektör veritabanları kurmak yerine doğrudan SQLite'ın yerleşik **FTS5** (Full-Text Search) özelliğini kullandım.
- **Tamamen Yerel:** Her şey `stdio` üzerinden bilgisayarınızda dönüyor, dışarı hiçbir veri çıkmıyor, API key gerekmiyor.
- **Ekstra Framework Yok:** LangChain vb. aracı katmanlar eklemedim; hangi tool'un ne zaman çağrılacağına Claude'un kendi mantığı karar veriyor.
- **stdio üzerinden MCP:** Sunucu, Claude Desktop veya Cursor tarafından bir alt process olarak başlatılır ve JSON-RPC mesajlarıyla stdin/stdout üzerinden konuşur.


```

Kullanıcı (doğal dil)
│
▼
Claude Desktop / Cursor  ──stdio (JSON-RPC)──►  server.py (FastMCP)
│
▼
notes_core.py (iş mantığı)
│
▼
db.py (SQLite + FTS5)
│
▼
notes.db (yerel dosya)

```

## MCP Araçları

| Tool | Açıklama |
|---|---|
| `log_note(content, tags)` | Veritabanına yeni bir hata/çözüm notu ve etiketlerini ekler. |
| `search_notes(query, limit)` | Geçmiş notlar içinde FTS5 ile tam metin araması yapar. |
| `get_recent_notes(limit)` | En son eklenen notları kronolojik sırayla getirir. |
| `update_note(note_id, content, tags)` | Belirtilen ID'li notun içeriğini ve (opsiyonel) etiketlerini günceller. |
| `delete_note(note_id)` | Belirtilen ID'li notu siler. |

## Gereksinimler

- **Python 3.10 veya üzeri** (proje Python 3.14 ile test edilmiştir)
- **pip**
- Claude Desktop **veya** Cursor (MCP destekleyen herhangi bir istemci)
- Windows, macOS veya Linux — hepsinde çalışır, aşağıdaki örnekler Windows path formatındadır

## Kurulum

### 1. Projeyi İndirme

```bash
git clone [https://github.com/](https://github.com/)<kullanici-adiniz>/mcp_personal_devLogger.git
cd mcp_personal_devLogger

```

> **Not:** Kurulumdan sonra bu klasörü **taşımayın veya yeniden adlandırmayın**. Aşağıda 4. ve 5. adımlarda tanımlayacağınız config dosyaları, bu klasörün **tam ve sabit** yolunu referans alır. Klasörü taşırsanız config'i de güncellemeniz gerekir (bkz. [Sorun Giderme](https://www.google.com/search?q=%23sorun-giderme)).

### 2. Sanal Ortam (Virtual Env)

Projenin bağımlılıklarını sistem genelinden izole etmek için mutlaka bir sanal ortam kullanın:

```bash
python -m venv venv

```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\activate

```

**macOS / Linux:**

```bash
source venv/bin/activate

```

*(Windows'ta yetki hatası alırsanız PowerShell'i yönetici olarak açıp önce şunu çalıştırın: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*

### 3. Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt

```

`requirements.txt` içeriği:

```
mcp>=1.25,<2
python-dotenv==1.0.1

```

> `mcp` paketini `<2` üst sınırıyla tutuyoruz çünkü SDK'nın 2.x hattı hâlâ alfa/beta aşamasında ve önceki sürümlerle uyumsuz kırılımlar içerebilir. `mcp==X.Y.Z` gibi tek bir sürüme sabitlemek yerine bir aralık vermek, güncel güvenlik/uyumluluk yamalarını almanızı sağlar.

### 4. Claude Desktop Ayarı

Claude Desktop'ta `Settings > Developer > Edit Config` yolunu izleyerek `claude_desktop_config.json` dosyasını açın ve `mcpServers` altına şunu ekleyin:

```json
{
  "mcpServers": {
    "my-dev-logger": {
      "command": "C:\\tam\\yol\\mcp_personal_devLogger\\venv\\Scripts\\python.exe",
      "args": ["C:\\tam\\yol\\mcp_personal_devLogger\\server.py"]
    }
  }
}

```

**Kritik kurallar:**

1. `C:\\tam\\yol\\...` kısımlarını kendi bilgisayarınızdaki **gerçek, mutlak** yolla değiştirin. Göreli yol (`./server.py` gibi) çalışmaz.
2. `command` alanında **mutlaka projenin kendi `venv` klasöründeki** `python.exe`'yi (Windows) veya `venv/bin/python` (macOS/Linux) gösterin. Sistemdeki global `python`'ı ya da PATH üzerinden çözülen bir `python` komutunu **kullanmayın** — global kurulumda `mcp` paketi olmayabilir ve sunucu sessizce başarısız olur.
3. JSON içinde Windows path'lerinde ters slash'ları **çift** yazmayı unutmayın (`\\`), tek `\` geçersiz JSON kaçış karakteridir.

Ayarı kaydettikten sonra **Claude Desktop'ı tamamen kapatıp yeniden açın** (sadece pencereyi kapatmak yetmez, sistem tepsisinden de çıkın).

### 5. Cursor Ayarı

Cursor da aynı `mcpServers` şemasını kullanır. Config dosyasını şu konumlardan birinde oluşturun/düzenleyin:

* **Global (tüm projeler için):** `~/.cursor/mcp.json`
* Windows'ta genellikle: `C:\Users\<kullanıcı adınız>\.cursor\mcp.json`


* **Proje bazlı (sadece bu projede aktif):** proje kök dizininde `.cursor/mcp.json`

İçerik, Claude Desktop ile birebir aynıdır:

```json
{
  "mcpServers": {
    "my-dev-logger": {
      "command": "C:\\tam\\yol\\mcp_personal_devLogger\\venv\\Scripts\\python.exe",
      "args": ["C:\\tam\\yol\\mcp_personal_devLogger\\server.py"]
    }
  }
}

```

Kaydettikten sonra Cursor'ı yeniden başlatın ve **Settings > MCP** sekmesinden sunucunun "connected" (yeşil) durumda olduğunu doğrulayın.

> Aynı sunucuyu hem Claude Desktop hem Cursor'da aynı anda kullanabilirsiniz; iki config birbirinden bağımsızdır ve çakışmaz.

### 6. Docker ile Kurulum (Önerilen)

Projeyi bilgisayarınızda herhangi bir Python sürüm çakışması veya kütüphane sorunu yaşamadan, tamamen izole bir ortamda çalıştırmak için Docker kullanabilirsiniz.

#### 1. İmajı İnşa Edin

Projenin ana dizininde bir terminal açın ve aşağıdaki komutu çalıştırarak Docker imajını oluşturun:

```bash
docker compose build

```

#### 2. Claude Desktop Konfigürasyonu

İmaj başarıyla oluşturulduktan sonra, Claude Desktop'ın yapılandırma dosyasını (`claude_desktop_config.json`) Docker üzerinden çalışacak şekilde ayarlayın.

*(Not: `-v` parametresindeki dosya yolunu, projeyi bilgisayarınızda indirdiğiniz klasörün tam yolu ile değiştirin. Bu sayede `notes.db` veritabanınız konteyner kapandığında silinmez ve kayıtlarınız güvende kalır.)*

```json
{
  "mcpServers": {
    "dev-logger": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "C:/tam/yol/mcp_personal_devLogger/data:/app",
        "mcp-dev-logger-devlogger-app"
      ]
    }
  }
}

```

## Kullanım Örnekleri

Kurulum bitince Claude Desktop veya Cursor'da normal sohbet eder gibi kullanabilirsiniz:

* *"Şunu kaydet: WhatsApp botunda session çökme sorununu `wwebjs_auth` klasörünü silerek çözdüm. Etiketler: nodejs, whatsapp"*
* *"Ollama ile ilgili aldığım notlara bir baksana, ne yazmışım?"*
* *"Son 5 notumu listele"*
* *"3 numaralı notun etiketlerini `python, sqlite` olarak güncelle"*
* *"5 numaralı notu sil"*

## Veritabanı Konumunu Değiştirme

Varsayılan olarak `notes.db` dosyası proje kök dizininde oluşturulur. Farklı bir konum istiyorsanız, **proje kök dizinine** (yani `server.py` ile aynı klasöre) bir `.env` dosyası ekleyin:

```
DB_PATH=C:\Users\kullanici\Documents\benim-notlarim.db

```

`db.py`, `python-dotenv` ile bu dosyayı otomatik okur; `.env` yoksa varsayılan konum kullanılır.

## Sorun Giderme

### "Server disconnected" / "can't open file ... No such file or directory"

Config'deki `args` yolu artık geçerli değil — proje klasörünü taşımışsınız veya yeniden adlandırmışsınız demektir. Çözüm: config'deki `command` ve `args` yollarını klasörün **güncel** konumuna göre düzeltin, ardından Claude Desktop/Cursor'ı tamamen kapatıp açın.

### Sunucu "bağlandı" görünüyor ama hiçbir tool çalışmıyor / hatalar anlaşılmaz

`server.py` içindeki `init_db()` çağrısı başarısız olmuş olabilir (örneğin `.env`'de yazılan `DB_PATH` klasörüne yazma izniniz yok). Bu sürümde `init_db()` başarısız olursa sunucu artık `sys.exit(1)` ile tamamen kapanır; Claude Desktop/Cursor loglarında `KRİTİK HATA: Veritabanı başlatılamadı: ...` satırını göreceksiniz. Belirtilen path'in var olduğundan ve yazılabilir olduğundan emin olun.

### `ModuleNotFoundError: No module named 'mcp'`

`command` alanı venv'in içindeki `python.exe` yerine global Python'a işaret ediyor. 4. adımdaki kuralı tekrar kontrol edin — `command`, projenin `venv\Scripts\python.exe` (Windows) veya `venv/bin/python` (macOS/Linux) yolunu göstermeli.

### Aynı sunucuyu birden fazla isimle/kopyayla tanımladım, tool'lar çakışıyor

Config dosyasında aynı projenin iki farklı klasör kopyasını (örneğin biri eski bir git clone, diğeri güncel) ayrı isimlerle (`my-dev-logger`, `personal-devLogger` gibi) aynı anda tanımlamayın — aynı tool isimleri (`log_note`, `search_notes` vb.) iki kez listelenir ve istemci tarafında karışıklık yaratır. Sadece **tek, güncel** kopyayı config'de tutun.

### Loglara nasıl bakarım?

* **Sunucu logu:** proje klasöründeki `server.log` dosyası — `log_note`, `search_notes` gibi her tool çağrısı ve hataları burada tutulur.
* **Claude Desktop MCP logu (Windows):** `%APPDATA%\Claude\logs\mcp-server-my-dev-logger.log`
* **Cursor MCP logu:** Cursor'ın kendi çıktı panelinde (Output > MCP Logs) görüntülenir.

## Proje Yapısı

```
mcp_personal_devLogger/
├── server.py          # MCP tool tanımları (FastMCP), stdio giriş noktası
├── notes_core.py       # İş mantığı: not ekleme/silme/güncelleme/arama
├── db.py               # SQLite bağlantısı, şema oluşturma, FTS5 kurulumu
├── requirements.txt     # mcp, python-dotenv bağımlılıkları
├── .env                 # (opsiyonel, git'e dahil değil) DB_PATH override
├── .gitignore
├── notes.db             # SQLite veritabanı (çalışma zamanında oluşur)
├── server.log            # Çalışma zamanı logları
└── README.md

```

## Geliştirme

Sunucuyu MCP istemcisi olmadan doğrudan test etmek isterseniz:

```bash
# venv aktifken
python server.py

```

stdio üzerinden çalıştığı için terminalde girdi bekleyecektir; gerçek testler için [MCP Inspector](https://github.com/modelcontextprotocol/inspector) kullanmanızı öneririm:

```bash
npx @modelcontextprotocol/inspector python server.py

```

Bu, tarayıcıda tool'ları tek tek çağırıp cevapları inceleyebileceğiniz bir arayüz açar — Claude Desktop'a bağlamadan önce hata ayıklamak için en hızlı yöntem budur.

## Lisans

MIT License — dilediğiniz gibi kullanabilir, değiştirebilir ve dağıtabilirsiniz.

---

Geri bildirim ve katkılar için issue açabilir veya pull request gönderebilirsiniz.

```

```