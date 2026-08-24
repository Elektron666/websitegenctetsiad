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

## Yayın öncesi kontrol listesi

Brief'in uyardığı, **yönetim veya hukuk onayı bekleyen** maddeler. Sitede
şu an ilgili yerlerde taslak uyarısı görünüyor; onaylar geldikçe hem içeriği
güncelleyin hem de uyarıyı kaldırın (`build.py` içinde `DRAFT_NOTES = False`).

- [ ] **1.500+ üye · 55 il · 40 ülke** — Uygulamada sabit yazılıydı, kaynağı
      belirsiz. Yönetime doğrulatın. Teyit edilemezse ana sayfadaki rakam
      şeridini tamamen kaldırın; yanlış rakam kurumsal sitede güven kaybettirir.
- [ ] **Başkan mesajı** — Yönetim onayı bekliyor.
- [ ] **Yasal metinler** — Dernek hukuk danışmanı onaylamalı. Metinlerdeki
      köşeli parantezli alanlar dernek kayıtlarından doldurulacak:
      `[TETSİAD — ... Derneği]` (tam tescilli unvan), `[dernek merkez adresi]`,
      `[İstanbul]` (yetkili mahkeme).
- [ ] **İletişim adresi ve telefon** — Yönetimden gelince iletişim sayfasına
      eklenecek; şu an yalnızca e-posta ve Instagram var.
- [ ] **Mağaza rozetleri** — Şu an ikisi de "YAKINDA" ve link vermiyor.
      Uygulama yayına girince `build.py` içindeki `IOS_LABEL` /
      `ANDROID_LABEL` değerlerini güncelleyip rozetleri gerçek mağaza
      adreslerine bağlayın.
- [ ] **Lighthouse** — Yayına alındıktan sonra gerçek alan adında ölçün.
      Hedef: performans ve erişilebilirlik 90+.

## Tasarımdan sapmalar

Tasarım dosyası tek sayfalık bir canvas prototipiydi (istemci tarafı sayfa
geçişli). Brief çok sayfalı statik site istediği için üç şey değişti:

1. `sc-if` ile gizlenen sayfa blokları ayrı HTML dosyalarına bölündü; menü
   gerçek bağlantılarla çalışıyor, JavaScript gerektirmiyor.
2. Satır içi stiller `assets/site.css` dosyasına taşındı. Renk, ölçü ve
   yazı tipi değerleri birebir korundu.
3. Izgara ayırıcı çizgilerinin çizim yöntemi değişti (yukarıdaki teknik not).
   Görünüm dolu ızgaralarda aynı; fark yalnızca boş gözlerde.
