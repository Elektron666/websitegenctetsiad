# genctetsiad.org — Genç TETSİAD web sitesi

Statik site. Derleme zinciri, paket yöneticisi ve CMS yok; çıktı doğrudan
sunucuya kopyalanır. Kaynak: Claude Design dosyası
`_kaynak/tasarim/Genc TETSIAD.dc.html` ve `_kaynak/WEB-SITESI-BRIEF.md`.

## Yerelde çalıştırma

Sayfa yolları köke göredir (`/assets/...`), bu yüzden `file://` ile açmak
yerine bir sunucu kullanın:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Yeniden üretme

HTML sayfaları `build.py` tarafından üretilir — üst menü, alt bilgi ve
`<head>` tek yerden gelir, sayfalar arasında sürüklenmez.

```bash
python3 build.py
```

Metin veya bölüm değişikliği `build.py` içinde yapılır, sonra script
çalıştırılır. Üretilen `.html` dosyalarını elle düzenlemeyin; bir sonraki
derlemede üzerine yazılır. Stiller `assets/site.css` içindedir ve elle
düzenlenir (script tarafından üretilmez).

## Yapı

```
index.html                 Ana sayfa
hakkimizda/index.html      /hakkimizda
programlar/index.html      /programlar
uyelik/index.html          /uyelik
iletisim/index.html        /iletisim
gizlilik-politikasi.html   ⚠️ dosya adı sabit
kullanim-kosullari.html    ⚠️ dosya adı sabit

assets/site.css            Tüm stiller; renk/tipografi değişkenleri en üstte
assets/site.js             Yalnızca fade-in gözlemcisi
assets/*.webp              Sitenin kullandığı görseller
assets/*.png               Görsellerin kayıpsız asılları (siteye servis edilmez)
assets/favicon.png         512×512 · apple-touch-icon.png 180×180 · og.png 1200×630

build.py                   Sayfa üreteci
_headers                   Netlify / Cloudflare Pages güvenlik başlıkları
.htaccess                  Apache karşılığı + uzantısız URL yönlendirmesi
robots.txt, sitemap.xml

_kaynak/                   Brief, PDF'ler, ham fotoğraflar, tasarım dosyası
```

### ⚠️ Yasal sayfaların adları değişmeyecek

`gizlilik-politikasi.html` ve `kullanim-kosullari.html` adresleri App Store
ve Google Play başvurularında verildi. Yol değişirse mağaza incelemecisinin
tıkladığı link ölür ve uygulama reddedilir.

### ⚠️ `_kaynak/` yayına yüklenmez

İçinde dernek brief'i, komisyon PDF'i ve ham fotoğraf arşivi var. Sunucuya
yalnızca yukarıdaki site dosyalarını kopyalayın. Yanlışlıkla yüklenirse
`.htaccess` erişimi kapatır ve `robots.txt` dizini dışarıda bırakır — ama
bunlar ikinci savunma hattı, birincisi yüklememektir.

## Yayına alma

Sunucu köküne kopyalanacaklar: `index.html`, `hakkimizda/`, `programlar/`,
`uyelik/`, `iletisim/`, iki yasal `.html`, `assets/`, `robots.txt`,
`sitemap.xml` ve barındırıcıya uygun olan başlık dosyası.

Kopyalanmayacaklar: `_kaynak/`, `build.py`, `README.md`.

**Güvenlik başlıkları statik HTML'den verilemez**, sunucudan gelmeli:

| Barındırıcı | Dosya |
|---|---|
| Netlify, Cloudflare Pages | `_headers` (hazır) |
| Apache, cPanel | `.htaccess` (hazır) |
| Nginx | `_headers` içindeki değerleri `add_header` olarak taşıyın |

Ayarlananlar: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`,
`Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` ve
bir `Content-Security-Policy`. CSP yalnızca kendi kaynaklarına ve Google
Fonts'a izin verir; siteye yeni bir dış kaynak eklerseniz CSP'yi de
güncelleyin, yoksa sessizce bloklanır.

## Güvenlik

Site tamamen statiktir: form gönderimi, veritabanı, oturum, çerez ve
sunucu tarafı kod yoktur. Klasik web açıkları (SQL enjeksiyonu, XSS,
CSRF, yetki atlatma) için gereken girdi yüzeyi bulunmaz.

Alınan önlemler:

- **Yazı tipleri yerel.** Google Fonts'a istek gitmez; ziyaretçinin IP
  adresi üçüncü tarafa ulaşmaz. Sayfalar hiçbir dış alan adına bağlanmaz.
- **CSP** `default-src 'self'` ile kilitli. `script-src` satır içi script'in
  SHA-256 özetine bağlı, `'unsafe-inline'` içermez. `style-src` düzen için
  satır içi `style=` kullanıldığından `'unsafe-inline'` içerir.
- **Dizin listeleme kapalı** (`Options -Indexes`). Olmasaydı `/assets/`
  altındaki her dosya tarayıcıdan listelenebilirdi.
- **HTTPS zorunlu** ve HSTS bir yıl.
- **Gizli ve kaynak dosyalar** (`.py`, `.md`, `.json`, nokta ile başlayanlar)
  sunucudan servis edilmez; `_kaynak/` tümüyle reddedilir.
- `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`,
  `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-Opener-Policy`.
- Dış bağlantılarda `rel="noopener noreferrer"`.
- `build.py` içerik verisini HTML'e yazmadan önce kaçırır.

**Tüm başlıklar `.htaccess`'ten gelir.** Dosya yüklenmezse veya
`mod_headers` kapalıysa hiçbiri uygulanmaz — yükledikten sonra
`bash guvenlik-testi.sh` çalıştırıp doğrulayın.

## Teknik notlar

- **Çerez yok, analitik yok.** KVKK metni "üçüncü taraf izleme aracı
  kullanılmaz" diyor. Google Analytics eklerseniz o metni de güncellemeniz
  gerekir.
- **Türkçe büyük harf.** `text-transform: uppercase` hiçbir yerde
  kullanılmadı; büyük harfli etiketler HTML'e doğrudan büyük yazıldı. Böylece
  `i → I` bozulması oluşamaz. Yeni etiket eklerken aynı yolu izleyin.
- **Görseller.** Tüm `<img>` etiketlerinde `width`/`height` var, ilk ekran
  dışındakiler `loading="lazy"`. Kapak görseli `fetchpriority="high"`.
  PNG'ler WebP'ye Chromium'un canvas kodlayıcısıyla çevrildi: 4,8 MB → 470 KB.
- **JavaScript.** Tek iş yapıyor: görünür alana giren bölümleri yavaşça
  belirtmek. Kapalıysa veya `prefers-reduced-motion` açıksa tüm içerik
  olduğu gibi görünür.
- **Izgara çizgileri.** 1px altın ayırıcılar, kapsayıcı zemini yerine hücre
  gölgesiyle çizilir; böylece son satırda boş kalan ızgara gözü açık renk
  bir blok olarak görünmez.

## Onay durumu

Tüm bölümler dernek tarafından onaylandı; sitede taslak veya "onay bekliyor"
uyarısı kalmadı. `build.py` başındaki bayraklar:

```python
DRAFT_BASKAN = False   # başkan mesajı — onaylandı
DRAFT_LEGAL  = False   # yasal metinler — onaylandı
```

Bir metin yeniden gözden geçirmeye açılırsa ilgili bayrağı `True` yapıp
`python3 build.py` çalıştırmak uyarıyı geri getirir.

Onaylanan içerik:

- **Rakamlar** — 1.500+ üye · 55 il · 3 ülke. Ana sayfada hem rakam
  şeridinde hem kapak metninde geçer; ikisi de `build.py` içinde.
- **Başkan mesajı** — Resul Öden, üç paragraf.
- **Yasal metinler** — gizlilik politikası ve kullanım koşulları. Dernek
  unvanı, merkez adresi ve yetkili mahkeme (İstanbul) dolduruldu; köşeli
  parantezli alan kalmadı.
- **İletişim** — adres, telefon ve e-posta; iletişim sayfası, alt bilgi ve
  gizlilik politikasının veri sorumlusu bölümünde.

Yayın sonrası kalan tek teknik iş: **Lighthouse ölçümü**, gerçek alan adında
ve gerçek sunucu başlıklarıyla. Hedef performans ve erişilebilirlikte 90+.

Not: posta kodu `34000` dernekten geldiği gibi yazıldı. Beyoğlu için gerçek
kod farklı olabilir; değişirse `build.py` içindeki `ADRES_ILCE` sabitini
güncelleyip yeniden derleyin — adres hem sitede hem KVKK metninde bu
sabitten gelir.

## Tasarımdan sapmalar

Tasarım dosyası tek sayfalık bir canvas prototipiydi (istemci tarafı sayfa
geçişli). Brief çok sayfalı statik site istediği için üç şey değişti:

1. `sc-if` ile gizlenen sayfa blokları ayrı HTML dosyalarına bölündü; menü
   gerçek bağlantılarla çalışıyor, JavaScript gerektirmiyor.
2. Satır içi stiller `assets/site.css` dosyasına taşındı. Renk, ölçü ve
   yazı tipi değerleri birebir korundu.
3. Izgara ayırıcı çizgilerinin çizim yöntemi değişti (yukarıdaki teknik not).
   Görünüm dolu ızgaralarda aynı; fark yalnızca boş gözlerde.
