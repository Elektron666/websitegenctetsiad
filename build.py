#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genç TETSİAD statik site üreteci.

Tasarım kaynağı: "Genc TETSIAD.dc.html" (Claude Design canvas).
Canvas'taki tek sayfalık SPA yapısı, brief'te istenen çok sayfalı
statik siteye çevrilir. Metin, renk ve ölçüler kaynaktan birebir alınmıştır.

Çalıştırma:  python3 build.py
"""

import os, re, shutil

SITE = "https://genctetsiad.org"
OUT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# VERİ — tasarım dosyasındaki renderVals() bloğundan birebir
# --------------------------------------------------------------------------

FAALIYETLER = [
    ("Üniversiteler ve fabrikalar",
     "Boğaziçi, Bilkent, Mimar Sinan, İTÜ ve ODTÜ gibi üniversitelerin tasarım ve "
     "tekstil fakülteleriyle anlaşmalar; İstanbul, Bursa ve Denizli fabrika-sanayi ziyaretleri."),
    ("Gençlik Zirvesi",
     "Sektörün tanınmış simalarından ve mimarlardan söyleşi, oturum, seminer ve atölye "
     "faaliyetleri. Her yıl düzenlenen zirveyle katılım, belgelendirme ve ödüllendirme."),
    ("Gençlik Buluşmaları",
     "Üyelerin sosyal hayatın içerisindeki varlığını ve devamlılığını düşünerek "
     "hazırlanan sosyal aktivite buluşmaları."),
    ("Mentorluk",
     "Sektördeki gençleri bir araya getirmek ve özel olarak sektörde pay sahibi "
     "olmalarını sağlamak."),
]

PROBLEMLER = [
    ("GENÇ KATILIMI", "Gençlerin sektöre dahil olmaması."),
    ("DİJİTALLEŞME", "Sektörün dijitalleşmeden uzak olması."),
    ("NETWORK EKSİKLİĞİ", "Sektör içerisinde tanışmaların yetersizliği."),
    ("İNOVASYON", "Ev tekstilinde yenilik olmaması."),
]

HEDEFLER = [
    ("01", "Genç girişimcileri sektöre dahil etmek"),
    ("02", "Gençlerin sektörel networkünü büyütmek"),
    ("03", "Klasik ticaret anlayışına yenilikler katmak"),
    ("04", "Genç TETSİAD üyelerinin ekip ruhunu oluşturmak"),
    ("05", "Genç TETSİAD'ın uluslararası bilinirliğini arttırmak"),
    ("06", "Gençlerin projelerini desteklemek"),
]

KOMISYONLAR = [
    "SEKTÖR KONULARI KOMİSYONU",
    "İLETİŞİM, MEDYA VE PR KOMİSYONU",
    "KURUMSAL İLİŞKİLER KOMİSYONU",
    "ÜNİVERSİTELER KOMİSYONU",
    "ÜYE KABUL KOMİSYONU",
    "ORGANİZASYON VE ETKİNLİK KOMİSYONU",
    "İHRACAT GELİŞTİRME KOMİSYONU",
]

PROGRAMLAR = [
    ("3T", "TÜRKİYE TEKSTİL TEMSİLCİLERİ",
     "Yıllık liderlik ve temsil programı; seçilen üyeler ulusal ve uluslararası "
     "platformlarda sektörü temsil eder.", "12", "KİŞİ"),
    ("TBA", "TEKSTİL BÜYÜKELÇİLERİ",
     "Uluslararası fuar ve konferanslarda Türkiye ev tekstilini temsil.", "8", "KİŞİ"),
    ("Altın Mekik", "ÖDÜL VE BURS",
     "Üretim, tasarım ve ihracatta olağanüstü başarı ödülü ve bursu.", "3", "KİŞİ"),
    ("UTGİK", "ARAŞTIRMA KOMİTESİ",
     "AB ve global tekstil trendlerini izleyen araştırma komitesi.", "AÇIK", "KONTENJAN"),
]

AKADEMI = [
    ("UZMAN KONUŞMACILAR", "Alanında uzman konuşmacıların seminerleri."),
    ("DİJİTAL EĞİTİMLER", "Sosyal medya ve e-ticaret eğitimleri."),
    ("SÜREÇ EĞİTİMLERİ", "Üretimden pazarlamaya süreç eğitimleri."),
    ("MUHASEBE", "Doğru ticari muhasebe eğitimleri."),
    ("İLETİŞİM", "Diksiyon ve hitabet eğitimleri."),
    ("ÖZEL TALEPLER", "Talep hâlinde istenilen alanda eğitim başlığı oluşturulabilir."),
]

TAKVIM = [
    ("ŞUBAT", "İftar programı"),
    ("MART", "İTÜ sosyal medya semineri"),
    ("NİSAN", "İstanbul fabrika ziyareti"),
    ("MAYIS", "Hometex fuar çalışması ve İTÜ tasarım etkinlikleri"),
    ("HAZİRAN", "Bursa fabrika ziyareti"),
    ("TEMMUZ", "Gençlik Buluşması"),
    ("AĞUSTOS", "Yapay zekâ etkinlikleri"),
    ("EYLÜL", "Güneydoğu turu ve etnik desen araştırması"),
    ("EKİM", "MSGSÜ tasarım etkinliği"),
    ("KASIM", "Tasarım yarışması"),
    ("ARALIK", "Gençlik Zirvesi"),
]

KONULAR = [
    ("Üyelik", "mailto:info@genctetsiad.org?subject=Üyelik%20başvurusu",
     "Başvurular uygulama üzerinden alınır; mağaza yayını yakında. Süreçle ilgili "
     "sorularınızı bu başlıkla yazabilirsiniz."),
    ("Programlar ve akademi", "mailto:info@genctetsiad.org?subject=Program%20başvurusu",
     "3T, TBA, Altın Mekik ve UTGİK kontenjanları, akademi eğitimleri, takvim ve "
     "seçim ölçütleri."),
    ("Basın ve iş birliği", "mailto:info@genctetsiad.org?subject=Basın%20ve%20iş%20birliği",
     "Röportaj talepleri, etkinlik davetleri, üniversite ve kurum iş birliği önerileri."),
]

BASKAN_MESAJ = [
    "Ev tekstili, bu ülkenin en köklü üretim alanlarından biri. Tezgâh başında "
    "öğrenilen bir işi devraldık; şimdi onu tasarımla, ihracatla ve dijital "
    "altyapıyla birlikte yürütmek bizim işimiz.",
    "Genç TETSİAD'ı kurarken tek bir soru sorduk: bir genç iş insanı, kendi "
    "fabrikasının dışında kiminle konuşuyor? Gençlik Konseyi'nden il "
    "temsilciliklerine, akademiden mentorluğa kadar kurduğumuz her yapı bu sorunun cevabı.",
    "Üniversitelerle iş birlikleri, fabrika ziyaretleri, zirveler ve eğitimler süs "
    "değil; sektörde söz sahibi olmak isteyen genç neslin altyapısı. Bu sorumluluğu "
    "almak isteyen herkesi aramızda görmek isteriz.",
]

BASKAN_ALINTI = "“Sektörün geleceğini gençlerle inşa etmek istiyoruz. Değişim gençlerle olacak.”"

VIZYON = "Ev tekstilinde genç, öncü, yenilikçi ve sürdürülebilir bir ekip olmak."
MISYON = ("Genç temsilcileri bir araya getirerek bilgi paylaşımı, eğitim ve mentorluk "
          "yoluyla sektörün geleceğini güçlendirmek.")

UYELIK_ALINTI = ("“Genç TETSİAD üyelik esaslı, kapalı bir platformdur. Başvurunuz dernek "
                 "komisyonu tarafından değerlendirilir.”")

# mağaza durumu — tasarımdaki storeStatus varsayılanı "Yakında"
IOS_LABEL = "YAKINDA"
ANDROID_LABEL = "YAKINDA"
# Onay durumları. Bir bölüm onaylandıkça ilgili bayrak False yapılır.
DRAFT_BASKAN = False   # başkan mesajı — yönetim onayı alındı
DRAFT_LEGAL  = True    # yasal metinler — hukuk danışmanı onayı bekliyor

# İletişim bilgileri (dernek merkezi)
ADRES_SATIR  = "Ömer Avni Mah. Meclis-i Mebusan Cd. No: 71 Kat: 6"
ADRES_ILCE   = "34000 Beyoğlu / İstanbul"
TELEFON      = "0553 252 46 53"
TELEFON_HREF = "tel:+905532524653"
DERNEK_UNVAN = "TETSİAD — Türkiye Ev Tekstili Sanayicileri ve İş İnsanları Derneği"

# --------------------------------------------------------------------------
# YASAL METİNLER — tasarım dosyasından birebir, yeniden yazılmadı
# --------------------------------------------------------------------------

GIZLILIK = [
    ("01", "Veri sorumlusu", [
        "Kişisel verileriniz, 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) "
        "kapsamında veri sorumlusu olarak TETSİAD — Türkiye Ev Tekstili Sanayicileri "
        "ve İş İnsanları Derneği tarafından, Genç TETSİAD komisyonu ve Genç TETSİAD "
        "mobil uygulaması bünyesinde işlenmektedir.",
        "Adres: Ömer Avni Mah. Meclis-i Mebusan Cd. No: 71 Kat: 6, 34000 Beyoğlu / İstanbul. "
        "Telefon: 0553 252 46 53. Elektronik posta: info@genctetsiad.org. Bu metin, "
        "genctetsiad.org web sitesi ve Genç TETSİAD uygulaması üzerinden yürütülen tüm "
        "veri işleme faaliyetlerini kapsar.",
    ], []),
    ("02", "İşlenen kişisel veriler", [
        "Üyelik başvurusu ve üyelik ilişkisinin yürütülmesi kapsamında aşağıdaki veri "
        "kategorileri işlenir:",
    ], [
        "Kimlik verisi: ad, soyad, doğum yılı.",
        "İletişim verisi: e-posta adresi, telefon numarası, yazışma adresi.",
        "Mesleki ve ticari veri: temsil edilen firma, unvan, faaliyet alanı, ihracat yapılan ülkeler.",
        "Üyelik verisi: başvuru tarihi, Üye Kabul Komisyonu değerlendirme kaydı, üye kodu, program başvuruları.",
        "İşlem güvenliği verisi: uygulamaya giriş kayıtları ve oturum bilgileri.",
    ]),
    ("03", "İşleme amaçları", [
        "Kişisel verileriniz yalnızca aşağıdaki amaçlarla, amaçla bağlantılı ve ölçülü "
        "olarak işlenir:",
    ], [
        "Üyelik başvurusunun alınması ve Üye Kabul Komisyonu tarafından değerlendirilmesi.",
        "Üyelik ilişkisinin kurulması, sürdürülmesi ve üye rehberinin oluşturulması.",
        "Etkinlik, eğitim, mentorluk ve program (3T, TBA, Altın Mekik, UTGİK) süreçlerinin yürütülmesi.",
        "Üniversite ve kurum iş birliklerinin, zirve ve fuar çalışmalarının organize edilmesi.",
        "Duyuru ve bülten iletişiminin sağlanması.",
        "Dernekler mevzuatından ve ilgili diğer mevzuattan doğan yükümlülüklerin yerine getirilmesi.",
    ]),
    ("04", "Hukuki sebep", [
        "İşleme faaliyetleri; KVKK m. 5/2-c uyarınca üyelik ilişkisinin kurulması ve ifası, "
        "m. 5/2-ç uyarınca derneğin hukuki yükümlülüklerini yerine getirmesi ve m. 5/2-f "
        "uyarınca derneğin meşru menfaatleri hukuki sebeplerine dayanır.",
        "Bülten ve tanıtım iletişimi açık rızanıza dayanır; rızanızı dilediğiniz zaman geri çekebilirsiniz.",
    ], []),
    ("05", "Aktarım ve çerezler", [
        "Kişisel verileriniz, barındırma ve bilgi teknolojileri hizmeti alınan tedarikçiler "
        "ile mevzuatın zorunlu kıldığı hâllerde yetkili kamu kurum ve kuruluşlarına "
        "aktarılabilir. Bunun dışında üçüncü kişilerle paylaşılmaz, satılmaz ve ticari "
        "amaçla devredilmez.",
        "Üye rehberi ve üye iletişim bilgileri yalnızca onaylı üyelere açık olan uygulama "
        "içinde görünür; web sitesinde yayımlanmaz.",
        "genctetsiad.org üzerinde reklam veya izleme çerezi kullanılmaz ve üçüncü taraf "
        "analiz aracı çalıştırılmaz.",
    ], []),
    ("06", "Saklama süresi", [
        "Üyelik verileri, üyelik ilişkisi sürdüğü süre boyunca ve ilişkinin sona ermesinden "
        "itibaren mevzuatta öngörülen zamanaşımı ve saklama süreleri boyunca tutulur.",
        "Reddedilen veya geri çekilen başvurulara ilişkin veriler, itiraz süresinin sona "
        "ermesinden sonra silinir veya anonim hâle getirilir.",
    ], []),
    ("07", "İlgili kişinin hakları", [
        "KVKK m. 11 uyarınca aşağıdaki haklara sahipsiniz:",
        "Taleplerinizi info@genctetsiad.org adresine iletebilirsiniz. Başvurunuz en geç "
        "otuz gün içinde yanıtlanır.",
    ], [
        "Kişisel verinizin işlenip işlenmediğini öğrenme ve işlenmişse bilgi talep etme.",
        "İşleme amacını ve verilerin amacına uygun kullanılıp kullanılmadığını öğrenme.",
        "Yurt içinde veya yurt dışında verilerin aktarıldığı üçüncü kişileri bilme.",
        "Verilerin eksik veya yanlış işlenmiş olması hâlinde düzeltilmesini isteme.",
        "Silinmesini veya yok edilmesini isteme ve bu işlemin aktarılan üçüncü kişilere "
        "bildirilmesini talep etme.",
        "İşlemenin hukuka aykırılığı nedeniyle zarara uğramanız hâlinde zararın "
        "giderilmesini talep etme.",
    ]),
]

KOSULLAR = [
    ("01", "Kapsam", [
        "Bu koşullar, genctetsiad.org web sitesinin ve Genç TETSİAD mobil uygulamasının "
        "kullanımına ilişkin şartları düzenler. Siteyi kullanan veya uygulamaya üye olan "
        "herkes bu koşulları kabul etmiş sayılır.",
        "Site ve uygulama, TETSİAD — Türkiye Ev Tekstili Sanayicileri ve İş İnsanları "
        "Derneği bünyesindeki Genç TETSİAD komisyonu tarafından işletilir.",
    ], []),
    ("02", "Üyelik ve erişim", [
        "Genç TETSİAD üyelik esaslı, kapalı bir platformdur. Üyelik başvuruları uygulama "
        "üzerinden alınır ve Üye Kabul Komisyonu tarafından değerlendirilir; komisyon "
        "başvuruyu gerekçe göstermeksizin reddedebilir.",
        "Üye rehberi, etkinlik takvimi, akademi ve mentorluk bölümleri yalnızca onaylı "
        "üyelere açıktır. Üyelik hesabı kişiseldir; devredilemez ve üçüncü kişilerle paylaşılamaz.",
        "Üyelik koşullarının ihlali hâlinde erişim geçici olarak durdurulabilir veya üyelik "
        "sona erdirilebilir.",
    ], []),
    ("03", "Kullanıcı yükümlülükleri", [
        "Platformu kullanan her üye aşağıdaki yükümlülükleri kabul eder:",
    ], [
        "Üye rehberinde yer alan iletişim bilgilerini izinsiz kopyalamamak, listelememek "
        "veya pazarlama amacıyla kullanmamak.",
        "Platformu yürürlükteki mevzuata, dernek tüzüğüne ve ticari dürüstlük ilkelerine "
        "aykırı biçimde kullanmamak.",
        "Paylaşılan içeriğin doğruluğundan ve üçüncü kişilerin haklarını ihlal etmemesinden "
        "sorumlu olmak.",
        "Platformun işleyişini bozacak teknik müdahalelerde bulunmamak.",
    ]),
    ("04", "Fikri mülkiyet", [
        "TETSİAD ve Genç TETSİAD adları, amblemleri ve bunların türevleri dernek adına "
        "korunmaktadır. Site ve uygulamada yer alan metin, fotoğraf, grafik ve "
        "düzenlemelerin tamamı dernek veya lisans verenlerine aittir.",
        "Bu içerikler, derneğin yazılı izni olmaksızın çoğaltılamaz, dağıtılamaz veya "
        "ticari amaçla kullanılamaz. Kaynak göstererek alıntı yapmak bu sınırlamanın dışındadır.",
    ], []),
    ("05", "Sorumluluğun sınırlandırılması", [
        "Site ve uygulama içeriği bilgilendirme amacıyla sunulur; yatırım, hukuk veya "
        "ticaret danışmanlığı niteliği taşımaz. Üyeler arasında kurulan ticari ilişkilerin "
        "tarafı dernek değildir.",
        "Hizmetin kesintisiz ve hatasız sunulacağı garanti edilmez. Bakım, güncelleme veya "
        "teknik arıza nedeniyle erişim geçici olarak durabilir.",
        "Site üzerinden bağlantı verilen üçüncü taraf içeriklerinden dernek sorumlu değildir.",
    ], []),
    ("06", "Yürürlük, değişiklik ve uygulanacak hukuk", [
        "Dernek, bu koşullarda değişiklik yapma hakkını saklı tutar. Güncellenen koşullar "
        "bu sayfada yayımlandığı anda yürürlüğe girer; esaslı değişiklikler üyelere uygulama "
        "üzerinden ayrıca duyurulur.",
        "Bu koşullardan doğan uyuşmazlıklarda Türkiye Cumhuriyeti hukuku uygulanır ve "
        "[İstanbul] mahkemeleri yetkilidir.",
    ], []),
]

# --------------------------------------------------------------------------
# İSKELET
# --------------------------------------------------------------------------

NAV = [
    ("hakkimizda", "/hakkimizda", "HAKKIMIZDA"),
    ("programlar", "/programlar", "PROGRAMLAR"),
    ("uyelik",     "/uyelik",     "ÜYELİK"),
    ("iletisim",   "/iletisim",   "İLETİŞİM"),
]

IG_SVG = ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="1.6" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/>'
          '<circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" '
          'stroke="none"/></svg>')

HEAD = """<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="__CANON__">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Genç TETSİAD">
<meta property="og:title" content="__OGTITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__CANON__">
<meta property="og:locale" content="tr_TR">
<meta property="og:image" content="__SITE__/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="__OGTITLE__">
<meta name="twitter:description" content="__DESC__">
<meta name="twitter:image" content="__SITE__/assets/og.png">

<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="theme-color" content="#051C11">

<link rel="icon" href="/assets/favicon.png" sizes="512x512" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Plus+Jakarta+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body>

<a class="skip" href="#icerik">İÇERİĞE GEÇ</a>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="/" aria-label="Genç TETSİAD — ana sayfa">
      <span class="brand-stack" aria-hidden="true">
        <img class="brand-emblem" src="/assets/emblem.webp" alt="" width="871" height="296">
        <span class="brand-genc">GENÇ</span>
        <img class="brand-word" src="/assets/wordmark.webp" alt="" width="1231" height="246">
      </span>
    </a>
    <nav class="site-nav" aria-label="Ana menü">
__NAVLINKS__
      <a class="nav-cta" href="/uyelik">BAŞVUR</a>
    </nav>
  </div>
</header>
"""

FOOT = """
<footer class="site-footer">
  <div class="cols">
    <div>
      <div class="foot-mark" role="img" aria-label="Genç TETSİAD">
        <img class="em" src="/assets/emblem.webp" alt="" aria-hidden="true" width="871" height="296" loading="lazy">
        <span class="genc" aria-hidden="true">GENÇ</span>
        <img class="wv" src="/assets/wordwave.webp" alt="" aria-hidden="true" width="1244" height="406" loading="lazy">
      </div>
      <p class="blurb">Türkiye ev tekstilinin genç iş insanları platformu.</p>
    </div>

    <nav aria-label="Site bağlantıları">
      <h2>SİTE</h2>
      <div class="links">
        <a href="/hakkimizda">Hakkımızda</a>
        <a href="/programlar">Programlar</a>
        <a href="/uyelik">Üyelik</a>
        <a href="/iletisim">İletişim</a>
      </div>
    </nav>

    <nav aria-label="Yasal bağlantılar">
      <h2>YASAL</h2>
      <div class="links">
        <a href="/gizlilik-politikasi.html">Gizlilik Politikası</a>
        <a href="/kullanim-kosullari.html">Kullanım Koşulları</a>
      </div>
    </nav>

    <div>
      <h2>İLETİŞİM</h2>
      <div class="links">
        <a class="mail" href="mailto:info@genctetsiad.org">info@genctetsiad.org</a>
        <a href="__TELHREF__">__TELEFON__</a>
        <a class="ig-sm" href="https://www.instagram.com/genctetsiad/" target="_blank" rel="noopener noreferrer">__IG14__ @genctetsiad</a>
        <span class="plain">__ADRES1__<br>__ADRES2__</span>
        <span class="plain">TETSİAD çatısı altında</span>
      </div>
    </div>
  </div>

  <div class="bar">
    <span>© 2026 GENÇ TETSİAD</span>
    <span>KONSEPT &amp; TASARIM — FATİH ÖZDEMİR · ORMEN TEKSTİL · ANKARA</span>
  </div>
</footer>

<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def shell(body, title, desc, canon, active=None, og_title=None):
    links = []
    for key, href, label in NAV:
        cur = ' aria-current="page"' if key == active else ""
        links.append('      <a href="%s"%s>%s</a>' % (href, cur, label))
    head = (HEAD
            .replace("__TITLE__", title)
            .replace("__OGTITLE__", og_title or title)
            .replace("__DESC__", desc)
            .replace("__CANON__", canon)
            .replace("__SITE__", SITE)
            .replace("__NAVLINKS__", "\n".join(links)))
    foot = (FOOT.replace("__IG14__", IG_SVG % (14, 14))
                .replace("__TELHREF__", TELEFON_HREF)
                .replace("__TELEFON__", TELEFON)
                .replace("__ADRES1__", ADRES_SATIR)
                .replace("__ADRES2__", ADRES_ILCE))
    return head + body + foot


def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  %-42s %6.1f KB" % (path, len(html.encode("utf-8")) / 1024))


def draft(text, show=True):
    return '<p class="draft">%s</p>' % text if show else ""


def badges():
    return ('<div class="badges">'
            '<div class="badge"><span class="k">APP STORE</span><span class="v">%s</span></div>'
            '<div class="badge"><span class="k">GOOGLE PLAY</span><span class="v">%s</span></div>'
            '</div>' % (IOS_LABEL, ANDROID_LABEL))


def baskan_figure(bottom="24px"):
    return ('<figure class="portrait" data-reveal>'
            '<img src="/assets/baskan.webp" alt="Genç TETSİAD Başkanı Resul Öden" '
            'width="470" height="588" loading="lazy">'
            '<div class="veil"></div>'
            '<figcaption><div class="name">Resul Öden</div>'
            '<div class="role">GENÇ TETSİAD BAŞKANI<br>ROSSA HOME · İSTANBUL</div>'
            '</figcaption></figure>')


def vizyon_misyon():
    return ('<div class="vm-grid">'
            '<div class="vm-card" data-reveal><p class="lbl-sm">VİZYONUMUZ</p><p>%s</p></div>'
            '<div class="vm-card" data-reveal><p class="lbl-sm">MİSYONUMUZ</p><p>%s</p></div>'
            '</div>' % (VIZYON, MISYON))

# --------------------------------------------------------------------------
# ANA SAYFA
# --------------------------------------------------------------------------

def page_home():
    faal = "".join(
        '<li><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in FAALIYETLER)

    prog = "".join(
        '<li><div class="name"><h3>%s</h3><div class="sub">%s</div></div>'
        '<p class="desc">%s</p><div class="qty">%s</div></li>' % (t, s, d, c)
        for t, s, d, c, _u in PROGRAMLAR)

    mesaj = "".join('<p class="body-tt">%s</p>' % p for p in BASKAN_MESAJ)

    feats = "".join('<li>%s</li>' % f for f in
                    ["ÜYE REHBERİ", "ETKİNLİK TAKVİMİ", "AKADEMİ",
                     "MENTORLUK", "BÜLTEN", "DUYURULAR"])

    steps = "".join(
        '<li><div class="no">%s</div><div class="t">%s</div></li>' % (n, t)
        for n, t in [("01", "Başvuru"), ("02", "Üye Kabul Komisyonu"), ("03", "Üyelik onayı")])

    return """
<main id="icerik">

  <section class="hero">
    <img src="/assets/fabrika-ziyareti.webp" alt="Genç TETSİAD üyeleri bir üye fabrikasında saha ziyaretinde" width="1179" height="499" fetchpriority="high">
    <div class="veil"></div>
    <div class="inner">
      <p class="lbl" style="margin-bottom:28px">TÜRKİYE EV TEKSTİLİ · GENÇ İŞ İNSANLARI</p>
      <h1>Değişim<br>gençlerle<br><span class="gold">olacak.</span></h1>
      <p class="lede">Sektörün geleceğini gençlerle inşa etmek istiyoruz. 1.500'ü aşkın genç iş insanı, 55 ilde ve 40 ülkede.</p>
      <div class="actions">
        <a class="btn btn-solid" href="/uyelik">ÜYELİK BAŞVURUSU</a>
        <a class="btn btn-line" href="/hakkimizda">VİZYON VE MİSYON</a>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="vm-h">
    <h2 class="lbl" id="vm-h" style="margin-bottom:clamp(40px,5vw,56px)">VİZYON VE MİSYON</h2>
    __VM__
    <p class="body-t" style="max-width:720px;line-height:1.95;margin:clamp(48px,6vw,64px) 0 0">Genç TETSİAD, sektördeki gençleri bir araya getirerek onlara network oluşturmayı hedefler. Bunun yanı sıra etkinlikler, seminerler, ortak ticari çalışmalar, sosyal ve ticari buluşmalar yaparak genç bir tekstil zemini oluşturmayı hedefler.</p>
  </section>

  <!-- Rakamlar yönetim teyidi bekliyor — bkz. README "Yayın öncesi kontrol listesi" -->
  <section class="stats" aria-label="Genç TETSİAD sayılarla">
    <div class="inner">
      <div class="grid">
        <div class="cell"><div class="num">1.500+</div><div class="cap">ÜYE</div></div>
        <div class="cell"><div class="num">55</div><div class="cap">İL</div></div>
        <div class="cell"><div class="num">40</div><div class="cap">ÜLKE</div></div>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="faaliyet-h">
    <div class="row-head" style="margin-bottom:clamp(40px,5vw,56px)">
      <h2 class="serif-h2" id="faaliyet-h">Faaliyetlerimiz</h2>
      <p class="meta">YIL BOYUNCA · TÜRKİYE GENELİNDE</p>
    </div>
    <ul class="cellgrid cards">__FAAL__</ul>
  </section>

  <section class="band" aria-labelledby="baskan-h">
    <div class="split">
      __BASKANFIG__
      <div data-reveal>
        <h2 class="lbl" id="baskan-h" style="margin-bottom:34px">BAŞKANDAN</h2>
        <blockquote class="pull">__ALINTI__</blockquote>
        <div class="rule"></div>
        __MESAJ__
        __DRAFT1__
      </div>
    </div>
  </section>

  <section class="sec-tight" aria-labelledby="programlar-h">
    <div class="row-head" style="margin-bottom:clamp(40px,5vw,56px)">
      <h2 class="serif-h2" id="programlar-h">Programlar</h2>
      <p class="meta">DÖRT PROGRAM · YILLIK KONTENJAN</p>
    </div>
    <ul class="prog">__PROG__</ul>
    <a class="link-under" href="/programlar" style="margin-top:44px">PROGRAMLAR, AKADEMİ VE TAKVİM →</a>
  </section>

  <section class="band-top" aria-labelledby="uygulama-h">
    <div class="app-grid">
      <div>
        <h2 class="lbl" id="uygulama-h" style="margin-bottom:28px">UYGULAMA</h2>
        <p class="serif-h3" style="font-size:clamp(30px,4.4vw,52px);margin:0 0 24px;line-height:1.15">Üyelere özel,<br>cebinizde.</p>
        <p class="body-t" style="max-width:520px;margin:0 0 40px">Genç TETSİAD uygulaması yalnızca onaylı üyelere açıktır. Üye rehberi KVKK korumasındadır ve web sitesinde yayımlanmaz.</p>
        <ul class="cellgrid on-deep feat">__FEATS__</ul>
        __BADGES__
      </div>
      <div class="phone" role="img" aria-label="Genç TETSİAD uygulamasının temsili giriş ekranı">
        <div class="bar"><span>09:41</span><span>GT</span></div>
        <div class="mid">
          <div class="t">Değişim<br>gençlerle<br><span class="gold">olacak.</span></div>
          <div class="s">ÜYE GİRİŞİ</div>
        </div>
        <div class="foot">UYGULAMA GÖRSELİ — TEMSİLİ</div>
      </div>
    </div>
  </section>

  <section class="joinband" aria-labelledby="uyelik-h">
    <img src="/assets/hometex-acilis.webp" alt="" aria-hidden="true" width="923" height="558" loading="lazy">
    <div class="veil"></div>
    <div class="inner">
      <h2 class="lbl" id="uyelik-h" style="margin-bottom:28px">ÜYELİK</h2>
      <p class="serif-h3" style="font-size:clamp(30px,4.4vw,52px);margin:0 0 26px;line-height:1.15;max-width:640px">Üç adımda üyelik.</p>
      <p class="body-t" style="max-width:560px;margin:0 0 clamp(40px,5vw,56px)">__UYEALINTI__</p>
      <ol class="steps">__STEPS__</ol>
      <a class="btn btn-solid" href="/uyelik">ÜYELİK BAŞVURUSU</a>
    </div>
  </section>

</main>
""".replace("__VM__", vizyon_misyon()) \
   .replace("__FAAL__", faal) \
   .replace("__BASKANFIG__", baskan_figure()) \
   .replace("__ALINTI__", BASKAN_ALINTI) \
   .replace("__MESAJ__", mesaj) \
   .replace("__DRAFT1__", draft("TASLAK METİN — YÖNETİM ONAYI BEKLİYOR", DRAFT_BASKAN)) \
   .replace("__PROG__", prog) \
   .replace("__FEATS__", feats) \
   .replace("__BADGES__", badges()) \
   .replace("__UYEALINTI__", UYELIK_ALINTI) \
   .replace("__STEPS__", steps)

# --------------------------------------------------------------------------
# HAKKIMIZDA
# --------------------------------------------------------------------------

def page_about():
    probs = "".join('<li><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in PROBLEMLER)
    goals = "".join('<li><span class="no">%s</span><span class="tx">%s</span></li>' % (n, t)
                    for n, t in HEDEFLER)
    units = "".join('<li>%s</li>' % k for k in KOMISYONLAR)
    mesaj = "".join('<p class="body-tt">%s</p>' % p for p in BASKAN_MESAJ)

    return """
<main id="icerik" class="page page-open">
  <p class="lbl">HAKKIMIZDA</p>
  <h1 style="max-width:820px;margin-bottom:30px">Bir dokuma geleneğinin genç kuşağı.</h1>
  <p class="body-t" style="max-width:640px;margin:0 0 clamp(48px,7vw,70px)">Genç TETSİAD, TETSİAD çatısı altında çalışan bir komisyondur. Sektördeki gençleri bir araya getirerek network oluşturmayı; etkinlikler, seminerler, ortak ticari çalışmalar ve buluşmalarla genç bir tekstil zemini kurmayı hedefler.</p>

  <img class="wide" src="/assets/bolge-komite.webp" alt="Genç TETSİAD bölge komite toplantısı" width="1064" height="980" loading="lazy" style="object-position:50% 88%;margin-bottom:clamp(64px,9vw,96px)">

  <section class="sec-block" aria-labelledby="vm-h2">
    <h2 class="lbl" id="vm-h2" style="margin-bottom:clamp(36px,5vw,52px)">VİZYON VE MİSYON</h2>
    __VM__
  </section>

  <section class="sec-block" aria-labelledby="problem-h">
    <h2 class="serif-h3" id="problem-h" style="margin-bottom:clamp(32px,4vw,44px)">Sektörün karşılaştığı problemler</h2>
    <ul class="cellgrid boxes">__PROBS__</ul>
  </section>

  <section class="sec-block" aria-labelledby="hedef-h">
    <h2 class="serif-h3" id="hedef-h" style="margin-bottom:clamp(32px,4vw,44px)">Hedeflerimiz</h2>
    <ol class="goals">__GOALS__</ol>
  </section>

  <section class="sec-block" aria-labelledby="org-h">
    <h2 class="serif-h3" id="org-h" style="margin-bottom:clamp(32px,4vw,44px)">Organizasyon yapısı</h2>
    <div class="org">
      <div>
        <h3>Komisyon başkanlığı</h3>
        <p style="margin-bottom:18px">Komisyon başkanı ve dört başkan yardımcısı:</p>
        <ul class="stack"><li>EĞİTİM</li><li>İLETİŞİM</li><li>ORGANİZASYON</li><li>ULUSLARARASI İLİŞKİLER</li></ul>
      </div>
      <div>
        <h3>Gençlik Konseyi</h3>
        <p>Tüm Türkiye'den Genç TETSİAD çalışmalarının içerisinde yer alan ekibin bir arada olduğu topluluk. Yönetim kurulu gibi çalışır; kararlar alınır, programlar düzenlenir.</p>
      </div>
      <div>
        <h3>Sektör Kurulu ve il temsilcilikleri</h3>
        <p>Döşemelik, perde, aksesuar, mekanik, ev tekstili, paketli ürünler, halı ve züccaciye gibi sektörel temsilcilikler; üyelerin bulunduğu tüm illerde temsilcilikler ve alt kadro oluşumları.</p>
      </div>
    </div>
    <h3 class="lbl" style="margin-bottom:28px">ALT BİRİMLER</h3>
    <ul class="cellgrid units">__UNITS__</ul>
  </section>

  <section class="sec-block" aria-labelledby="isbirligi-h">
    <h2 class="lbl" id="isbirligi-h" style="margin-bottom:32px">İŞ BİRLİKLERİMİZ</h2>
    <p class="serif-h3" style="font-size:clamp(23px,2.8vw,32px);line-height:1.5;max-width:900px;text-wrap:pretty">Mimar Sinan Üniversitesi, Milli Eğitim Bakanlığı, Boğaziçi Üniversitesi, Yalova Üniversitesi, Bilkent Üniversitesi ve TMMOB Mimarlar Odası ile güçlü iş birlikleri.</p>
  </section>

  <section aria-labelledby="baskan-h2" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:clamp(40px,5vw,72px);align-items:start;padding-bottom:clamp(80px,10vw,110px)">
    __BASKANFIG__
    <div data-reveal>
      <h2 class="lbl" id="baskan-h2" style="margin-bottom:34px">BAŞKANDAN</h2>
      <blockquote class="pull" style="font-size:clamp(25px,3vw,36px)">__ALINTI__</blockquote>
      __MESAJ__
      __DRAFT1__
    </div>
  </section>
</main>
""".replace("__VM__", vizyon_misyon()) \
   .replace("__PROBS__", probs) \
   .replace("__GOALS__", goals) \
   .replace("__UNITS__", units) \
   .replace("__BASKANFIG__", baskan_figure("22px")) \
   .replace("__ALINTI__", BASKAN_ALINTI) \
   .replace("__MESAJ__", mesaj) \
   .replace("__DRAFT1__", draft("TASLAK METİN — YÖNETİM ONAYI BEKLİYOR", DRAFT_BASKAN))


# --------------------------------------------------------------------------
# PROGRAMLAR
# --------------------------------------------------------------------------

def page_programs():
    prog = "".join(
        '<li data-reveal><div class="name"><h2>%s</h2><div class="sub">%s</div></div>'
        '<p class="desc">%s</p>'
        '<div class="qty"><div>%s</div><div class="unit">%s</div></div></li>' % (t, s, d, c, u)
        for t, s, d, c, u in PROGRAMLAR)

    acad = "".join('<li><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in AKADEMI)
    cal = "".join('<li><span class="m">%s</span><span class="e">%s</span></li>' % (a, b)
                  for a, b in TAKVIM)

    return """
<main id="icerik" class="page">
  <p class="lbl">PROGRAMLAR</p>
  <h1>Temsil, ödül ve araştırma.</h1>
  <p class="body-t" style="max-width:580px;margin:0 0 clamp(48px,7vw,64px)">Dört program; sektörü temsil etme, başarıyı ödüllendirme ve trendleri okuma sorumluluğunu genç üyelere devreder. Kontenjanlar yıllıktır.</p>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2px;margin-bottom:clamp(64px,9vw,90px)">
    <figure class="figcap-wrap">
      <img class="wide" src="/assets/hometex-acilis.webp" alt="Hometex 2026 açılış töreni" width="923" height="558" loading="lazy" style="object-position:50% 100%;filter:saturate(.45) contrast(1.05) brightness(.9)">
      <div class="veil"></div>
      <figcaption>HOMETEX 2026 · İSTANBUL</figcaption>
    </figure>
    <figure class="figcap-wrap">
      <img class="wide" src="/assets/bolge-komite.webp" alt="Bölge komite toplantısı" width="1064" height="980" loading="lazy" style="object-position:50% 88%;filter:saturate(.45) contrast(1.05) brightness(.9)">
      <div class="veil"></div>
      <figcaption>BÖLGE KOMİTE TOPLANTISI</figcaption>
    </figure>
  </div>

  <ul class="prog prog-lg" style="margin-bottom:clamp(72px,9vw,110px)">__PROG__</ul>

  <section class="sec-block" aria-labelledby="akademi-h">
    <div class="row-head" style="margin-bottom:clamp(28px,4vw,40px)">
      <h2 class="serif-h3" id="akademi-h">TETSİAD Akademi</h2>
      <p class="meta">ÜYELERE AÇIK EĞİTİM BAŞLIKLARI</p>
    </div>
    <p class="body-t" style="max-width:620px;margin:0 0 clamp(32px,4vw,44px)">Hedefimiz her alanda kendini geliştirmeye açık genç üyelerle sağlam bir zemin oluşturmak. Talep hâlinde istenilen alanda yeni eğitim başlığı açılabilir.</p>
    <ul class="cellgrid boxes boxes-acad">__ACAD__</ul>
  </section>

  <section style="margin-bottom:clamp(56px,7vw,80px)" aria-labelledby="takvim-h">
    <div class="row-head" style="margin-bottom:clamp(28px,4vw,40px)">
      <h2 class="serif-h3" id="takvim-h">2026 etkinlik takvimi</h2>
      <p class="meta">BAŞLANGIÇ PLANLAMASI</p>
    </div>
    <ol class="cal">__CAL__</ol>
    <p class="meta" style="font-size:10.5px;letter-spacing:2px;margin:26px 0 0;padding-top:22px;border-top:1px solid var(--gold-line)">TARİHLER VE İÇERİKLER DEĞİŞEBİLİR · GÜNCEL TAKVİM UYGULAMADA</p>
  </section>

  <div class="callout">
    <p>Programlara ve akademiye başvuru, üyelik onayından sonra açılır.</p>
    <a class="btn btn-solid" href="/uyelik">ÜYELİK BAŞVURUSU</a>
  </div>
</main>
""".replace("__PROG__", prog).replace("__ACAD__", acad).replace("__CAL__", cal)

# --------------------------------------------------------------------------
# ÜYELİK
# --------------------------------------------------------------------------

def page_membership():
    steps = [
        ("01", "Başvuru", "Uygulamayı indirin ve başvuru formunu doldurun. Firma bilgileriniz ve sektördeki konumunuz sorulur."),
        ("02", "Üye Kabul Komisyonu", "Başvuru, Üye Kabul Komisyonu tarafından incelenir. Gerekirse ek belge ve görüşme talep edilir."),
        ("03", "Üyelik onayı", "Onay sonrası üye kodunuz tanımlanır; Gençlik Konseyi, akademi ve mentorluk bölümleri açılır."),
    ]
    st = "".join('<li data-reveal><div class="no">%s</div><h2>%s</h2><p>%s</p></li>' % s for s in steps)

    return """
<main id="icerik" class="page">
  <p class="lbl">ÜYELİK</p>
  <h1>Kapalı platform, açık davet.</h1>
  <p class="body-t" style="max-width:600px;margin:0 0 clamp(48px,7vw,64px)">__UYEALINTI__</p>

  <figure class="figcap-wrap" style="margin:0 0 clamp(64px,9vw,90px)">
    <img class="wide" src="/assets/fabrika-ziyareti.webp" alt="Genç TETSİAD üyeleri bir üye fabrikasında" width="1179" height="499" loading="lazy" style="object-position:50% 38%;filter:saturate(.5) contrast(1.05) brightness(.9)">
    <div class="veil" style="background:linear-gradient(180deg,rgba(3,15,9,.15) 35%,rgba(3,15,9,.92) 100%)"></div>
    <figcaption style="left:clamp(20px,3vw,30px);right:clamp(20px,3vw,30px);bottom:26px;display:flex;flex-wrap:wrap;gap:12px 16px;justify-content:space-between;align-items:baseline">
      <span style="font-family:var(--serif);font-style:italic;font-size:clamp(20px,2.4vw,26px);color:var(--ivory);letter-spacing:normal">Üye firmalarda saha ziyareti.</span>
      <span style="color:var(--gold)">DERNEK ARŞİVİ</span>
    </figcaption>
  </figure>

  <ol class="steps steps-lg">__STEPS__</ol>

  <div class="applybox">
    <img src="/assets/mark-gold.webp" alt="" aria-hidden="true" width="1244" height="692" loading="lazy">
    <div class="txt">
      <p class="big">Başvuru uygulama üzerinden alınır.</p>
      <p class="sm">MAĞAZA YAYINI YAKINDA · SORULARINIZ İÇİN <a href="mailto:info@genctetsiad.org">INFO@GENCTETSIAD.ORG</a></p>
    </div>
    __BADGES__
  </div>
</main>
""".replace("__UYEALINTI__", UYELIK_ALINTI).replace("__STEPS__", st).replace("__BADGES__", badges())


# --------------------------------------------------------------------------
# İLETİŞİM
# --------------------------------------------------------------------------

def page_contact():
    topics = "".join(
        '<a href="%s"><div class="t">%s</div><p>%s</p><span class="go">YAZ →</span></a>'
        % (h, t, d) for t, h, d in KONULAR)

    return """
<main id="icerik">
  <section class="contact-top">
    <div>
      <p class="lbl" style="margin-bottom:26px">İLETİŞİM</p>
      <h1 class="serif-xl" style="font-size:clamp(38px,6vw,74px);margin:0 0 30px;line-height:1.06">Bize yazın.</h1>
      <p class="body-t" style="max-width:460px;margin:0 0 44px">Konusu ne olursa olsun tek bir adres yeterli. Aşağıdaki başlıklardan birini seçerseniz, yazınız doğru komisyona daha hızlı ulaşır.</p>
      <a class="mailto-xl" href="mailto:info@genctetsiad.org">info@genctetsiad.org</a>
      <div class="social-row">
        <a class="ig" href="https://www.instagram.com/genctetsiad/" target="_blank" rel="noopener noreferrer">__IG15__ @GENCTETSIAD</a>
        <span class="meta" style="font-size:10.5px;letter-spacing:2.2px">YANIT SÜRESİ · İKİ İŞ GÜNÜ</span>
      </div>
    </div>
    <figure class="figcap-wrap">
      <img src="/assets/bolge-komite.webp" alt="Genç TETSİAD bölge komite toplantısı" width="1064" height="980" loading="lazy" style="width:100%;height:auto;aspect-ratio:4/5;max-height:60vh;object-fit:cover;object-position:50% 62%;display:block;filter:saturate(.45) contrast(1.05) brightness(.85)">
      <div class="veil" style="background:linear-gradient(180deg,rgba(3,15,9,.1) 45%,rgba(3,15,9,.88) 100%)"></div>
      <figcaption style="right:26px">BÖLGE KOMİTE TOPLANTISI · DERNEK ARŞİVİ</figcaption>
    </figure>
  </section>

  <section aria-labelledby="konu-h" style="max-width:var(--wrap);margin:0 auto;padding:clamp(72px,9vw,110px) var(--pad) 0">
    <h2 class="lbl" id="konu-h" style="margin-bottom:44px">NE HAKKINDA YAZIYORSUNUZ?</h2>
    <div class="topics">__TOPICS__</div>
    <div style="border-top:1px solid var(--gold-line)"></div>
  </section>

  <section style="max-width:var(--wrap);margin:0 auto;padding:clamp(64px,8vw,100px) var(--pad) clamp(80px,10vw,120px)">
    <dl class="deflist">
      <div>
        <dt>ADRES</dt>
        <dd>__ADRES1__<br>__ADRES2__</dd>
      </div>
      <div>
        <dt>TELEFON</dt>
        <dd><a href="__TELHREF__">__TELEFON__</a></dd>
      </div>
      <div>
        <dt>ÇATI KURULUŞ</dt>
        <dd>TETSİAD — Türkiye Ev Tekstili Sanayicileri ve İş İnsanları Derneği</dd>
      </div>
      <div>
        <dt>SOSYAL MEDYA</dt>
        <dd><a href="https://www.instagram.com/genctetsiad/" target="_blank" rel="noopener noreferrer">Instagram · @genctetsiad</a></dd>
      </div>
      <div>
        <dt>KİŞİSEL VERİLER</dt>
        <dd>Üye rehberi KVKK korumasındadır, sitede yayımlanmaz. <a href="/gizlilik-politikasi.html">Gizlilik politikası</a></dd>
      </div>
    </dl>
    __DRAFT__
  </section>
</main>
""".replace("__IG15__", IG_SVG % (15, 15)) \
   .replace("__TOPICS__", topics) \
   .replace("__ADRES1__", ADRES_SATIR) \
   .replace("__ADRES2__", ADRES_ILCE) \
   .replace("__TELHREF__", TELEFON_HREF) \
   .replace("__TELEFON__", TELEFON) \
   .replace("__DRAFT__", "")


# --------------------------------------------------------------------------
# YASAL SAYFALAR
# --------------------------------------------------------------------------

def page_legal(kind):
    priv = kind == "gizlilik"
    kicker = "KVKK · AYDINLATMA" if priv else "KULLANIM KOŞULLARI"
    title = "Gizlilik Politikası" if priv else "Kullanım Koşulları"
    path = ("genctetsiad.org/gizlilik-politikasi.html" if priv
            else "genctetsiad.org/kullanim-kosullari.html")
    other_href = "/kullanim-kosullari.html" if priv else "/gizlilik-politikasi.html"
    other_label = "KULLANIM KOŞULLARI" if priv else "GİZLİLİK POLİTİKASI"
    sections = GIZLILIK if priv else KOSULLAR

    blocks = []
    for no, head, body, items in sections:
        paras = "".join("<p>%s</p>" % p for p in body)
        lst = ""
        if items:
            lst = "<ul>%s</ul>" % "".join("<li>%s</li>" % i for i in items)
        blocks.append('<section class="legal-sec"><div class="no">%s</div>'
                      '<div><h2>%s</h2>%s%s</div></section>' % (no, head, paras, lst))

    notice = ""
    if DRAFT_LEGAL:
        notice = ('<div class="notice"><p class="h">HUKUK ONAYI BEKLİYOR</p>'
                  '<p>Aşağıdaki metin taslaktır ve yayına alınmadan önce derneğin hukuk '
                  'danışmanı tarafından onaylanmalıdır. Köşeli parantez içindeki alanlar '
                  '(yetkili mahkeme) dernek kayıtlarından doldurulacaktır.</p></div>')

    return """
<main id="icerik" class="legal">
  <p class="lbl">__KICKER__</p>
  <h1>__TITLE__</h1>
  <p class="path">__PATH__</p>
  <p class="upd">SON GÜNCELLEME · AĞUSTOS 2026</p>
  __NOTICE__
  <div class="legal-body">__BLOCKS__</div>
  <div class="legal-foot">
    <p>Bu metinle ilgili sorularınız için: <a href="mailto:info@genctetsiad.org">info@genctetsiad.org</a></p>
    <a class="link-under" href="__OTHERHREF__" style="font-size:10.5px">__OTHERLABEL__ →</a>
  </div>
</main>
""".replace("__KICKER__", kicker).replace("__TITLE__", title).replace("__PATH__", path) \
   .replace("__NOTICE__", notice).replace("__BLOCKS__", "".join(blocks)) \
   .replace("__OTHERHREF__", other_href).replace("__OTHERLABEL__", other_label)

# --------------------------------------------------------------------------
# EK DOSYALAR
# --------------------------------------------------------------------------

SITE_JS = """/* Genç TETSİAD — yavaş ve az fade-in. Başka iş yapmaz. */
(function () {
  'use strict';
  var els = document.querySelectorAll('[data-reveal]');
  if (!els.length) return;

  function showAll() {
    for (var i = 0; i < els.length; i++) els[i].classList.add('shown');
  }

  if (!('IntersectionObserver' in window) ||
      (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    showAll();
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('shown');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  for (var i = 0; i < els.length; i++) {
    // ilk ekranda görünen öğeleri bekletme
    if (els[i].getBoundingClientRect().top < window.innerHeight * 0.92) {
      els[i].classList.add('shown');
    } else {
      io.observe(els[i]);
    }
  }
})();
"""

ROBOTS = """User-agent: *
Allow: /
Disallow: /_kaynak/

Sitemap: %s/sitemap.xml
""" % SITE

# Güvenlik başlıkları statik HTML'den verilemez; barındırıcıya bırakılır.
HEADERS_NETLIFY = """/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'

/assets/*
  Cache-Control: public, max-age=31536000, immutable

# _kaynak/ yayına yüklenmemeli; yine de yüklendiyse dizine erişimi kapat.
/_kaynak/*
  X-Robots-Tag: noindex, nofollow
"""

HTACCESS = """# Apache — Netlify/Cloudflare dışı barındırma için
<IfModule mod_headers.c>
  Header always set X-Frame-Options "DENY"
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>

<IfModule mod_rewrite.c>
  RewriteEngine On
  # /hakkimizda -> /hakkimizda/index.html
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME}/index.html -f
  RewriteRule ^(.*)$ /$1/index.html [L]
</IfModule>

# Kaynak dosyalar (brief, ham fotoğraf, tasarım dosyası) yayına açılmaz.
<IfModule mod_rewrite.c>
  RewriteRule ^_kaynak/ - [F,L]
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType text/css "access plus 1 year"
</IfModule>
"""


def sitemap(pages):
    rows = []
    for url, prio in pages:
        rows.append("  <url>\n    <loc>%s%s</loc>\n    <changefreq>monthly</changefreq>\n"
                    "    <priority>%s</priority>\n  </url>" % (SITE, url, prio))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


# --------------------------------------------------------------------------

def main():
    print("Genç TETSİAD — statik site üretiliyor\n")

    write("index.html", shell(
        page_home(),
        "Genç TETSİAD — Türkiye ev tekstilinin genç iş insanları platformu",
        "Genç TETSİAD; ev tekstilinde genç, öncü, yenilikçi ve sürdürülebilir bir ekip "
        "olmayı hedefleyen üyelik esaslı platform. Vizyon, faaliyetler, programlar ve üyelik.",
        SITE + "/", active=None, og_title="Genç TETSİAD"))

    write("hakkimizda/index.html", shell(
        page_about(),
        "Hakkımızda — Genç TETSİAD",
        "Genç TETSİAD'ın vizyonu, misyonu, hedefleri ve organizasyon yapısı. TETSİAD "
        "çatısı altında çalışan genç kuşak komisyonu.",
        SITE + "/hakkimizda", active="hakkimizda"))

    write("programlar/index.html", shell(
        page_programs(),
        "Programlar — Genç TETSİAD",
        "3T, TBA, Altın Mekik ve UTGİK programları, TETSİAD Akademi eğitim başlıkları ve "
        "2026 etkinlik takvimi.",
        SITE + "/programlar", active="programlar"))

    write("uyelik/index.html", shell(
        page_membership(),
        "Üyelik — Genç TETSİAD",
        "Genç TETSİAD üyelik esaslı, kapalı bir platformdur. Başvuru, Üye Kabul Komisyonu "
        "değerlendirmesi ve üyelik onayı olmak üzere üç adım.",
        SITE + "/uyelik", active="uyelik"))

    write("iletisim/index.html", shell(
        page_contact(),
        "İletişim — Genç TETSİAD",
        "Üyelik, programlar, basın ve iş birliği başlıklarında Genç TETSİAD ile iletişime "
        "geçin: info@genctetsiad.org",
        SITE + "/iletisim", active="iletisim"))

    # ⚠️ Bu iki dosya adı mağaza başvurularında verildi — değiştirilmemeli.
    write("gizlilik-politikasi.html", shell(
        page_legal("gizlilik"),
        "Gizlilik Politikası — Genç TETSİAD",
        "Genç TETSİAD KVKK aydınlatma metni: işlenen kişisel veriler, işleme amaçları, "
        "hukuki sebepler, saklama süresi ve ilgili kişinin hakları.",
        SITE + "/gizlilik-politikasi.html"))

    write("kullanim-kosullari.html", shell(
        page_legal("kosullar"),
        "Kullanım Koşulları — Genç TETSİAD",
        "genctetsiad.org ve Genç TETSİAD mobil uygulamasının kullanım koşulları: üyelik, "
        "erişim, kullanıcı yükümlülükleri ve fikri mülkiyet.",
        SITE + "/kullanim-kosullari.html"))

    write("assets/site.js", SITE_JS)
    write("robots.txt", ROBOTS)
    write("_headers", HEADERS_NETLIFY)
    write(".htaccess", HTACCESS)
    write("sitemap.xml", sitemap([
        ("/", "1.0"),
        ("/hakkimizda", "0.8"),
        ("/programlar", "0.8"),
        ("/uyelik", "0.8"),
        ("/iletisim", "0.6"),
        ("/gizlilik-politikasi.html", "0.3"),
        ("/kullanim-kosullari.html", "0.3"),
    ]))

    print("\nBitti.")


if __name__ == "__main__":
    main()
