# Genç TETSİAD — Web Sitesi

Genç TETSİAD tanıtım sitesi. Bağımlılık yok: düz HTML, CSS ve vanilla JavaScript.

## Çalıştırma

Derleme adımı yok. `index.html` dosyasını doğrudan tarayıcıda açabilir ya da
basit bir sunucu ile servis edebilirsiniz:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Dosya yapısı

```
index.html            Tek sayfalık site (tüm bölümler)
assets/styles.css     Stil sistemi — renk/tipografi değişkenleri en üstte
assets/main.js        Mobil menü, scroll durumu, reveal animasyonu, form doğrulama
assets/*.png          Görseller
```

## ⚠️ Yer tutucu içerikler

Bu sürüm, tasarım dosyasındaki (`Genç TETSİAD.dc.html`) görsellere **erişilemeden**
oluşturulmuştur. Aşağıdakiler yer tutucudur ve gerçek içerikle değiştirilmelidir:

**Görseller** — `assets/` altındaki 8 PNG programatik olarak üretilmiş yer
tutuculardır. Gerçek dosyaları **aynı adlarla** üzerine yazmanız yeterlidir;
HTML'de değişiklik gerekmez:

| Dosya | Kullanım | Önerilen en-boy |
|---|---|---|
| `emblem.png` | Hero amblemi | 1:1 |
| `mark-gold.png` | Favicon + üyelik bölümü | 1:1 |
| `wordmark.png` | Header ve footer logosu | ~5.5:1, şeffaf zemin |
| `wordwave.png` | Hero ve üyelik dalga deseni | ~3.8:1, şeffaf zemin |
| `baskan.png` | Başkan portresi | 4:5 |
| `bolge-komite.png` | Bölge komiteleri görseli | 5:4 |
| `fabrika-ziyareti.png` | Faaliyet kartı | 16:10 |
| `hometex-acilis.png` | Faaliyet kartı | 16:10 |

**Metinler** — köşeli parantezle işaretlenmiştir: `[Başkan Adı Soyadı]`,
`[Adres satırı]`, `[İlçe / İl]`. Ayrıca:

- Hero'daki istatistik şeridinde sayılar `—` olarak bırakıldı.
- Bölge komitesi listesi örnektir; gerçek yapıya göre güncellenmeli.
- Footer'daki e-posta ve telefon örnektir.

**Üyelik formu** yalnızca istemci tarafında doğrulama yapar; gönderim yoktur.
Gerçek gönderim için `assets/main.js` içindeki submit işleyicisine bir uç nokta
(kendi backend'iniz veya bir form servisi) bağlanmalıdır.

## Notlar

- Renk ve tipografi `assets/styles.css` içindeki `:root` değişkenlerinden yönetilir.
- Yazı tipleri Google Fonts'tan (Fraunces + Inter) yüklenir; erişilemezse
  sistem yazı tiplerine düşer.
- `prefers-reduced-motion` desteklenir; animasyonlar kapatılır.
- JavaScript devre dışıysa tüm içerik görünür kalır (reveal yalnızca `.js` altında).
- Erişilebilirlik: içeriğe atlama bağlantısı, `aria-expanded` menü, görünür odak halkaları.
