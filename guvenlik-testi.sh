#!/usr/bin/env bash
# genctetsiad.org — canlı site güvenlik ve sağlık kontrolü
#
# Kullanım:  bash guvenlik-testi.sh [alanadi]
# Çıktının tamamını kopyalayıp geri gönderin.

D="${1:-genctetsiad.org}"
B="https://$D"
ok(){ printf '  \033[32m✓\033[0m %s\n' "$1"; }
no(){ printf '  \033[31m✗\033[0m %s\n' "$1"; }
wr(){ printf '  \033[33m!\033[0m %s\n' "$1"; }

echo "=============================================="
echo " $D  —  $(date '+%Y-%m-%d %H:%M')"
echo "=============================================="

echo
echo "[1] HTTP -> HTTPS yönlendirmesi"
r=$(curl -sSI --max-time 20 "http://$D/" 2>/dev/null | head -1)
loc=$(curl -sSI --max-time 20 "http://$D/" 2>/dev/null | grep -i '^location:' | tr -d '\r')
echo "     $r"; [ -n "$loc" ] && echo "     $loc"
case "$r" in *30[128]*) ok "yönlendirme var";; *) no "HTTP düz servis ediliyor - yönlendirme yok";; esac

echo
echo "[2] Sayfalar"
for p in / /hakkimizda /programlar /uyelik /iletisim \
         /gizlilik-politikasi.html /kullanim-kosullari.html; do
  c=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$B$p")
  f=$(curl -sL -o /dev/null -w '%{http_code}' --max-time 20 "$B$p")
  if   [ "$c" = "200" ];               then ok "$c  $p"
  elif [ "$f" = "200" ];               then wr "$c -> $f  $p  (yönlendirme ile açılıyor)"
  else                                      no "$c  $p"
  fi
done

echo
echo "[3] Güvenlik başlıkları"
H=$(curl -sSI --max-time 20 "$B/" 2>/dev/null | tr -d '\r')
for h in "content-security-policy" "strict-transport-security" "x-frame-options" \
         "x-content-type-options" "referrer-policy" "permissions-policy"; do
  v=$(echo "$H" | grep -i "^$h:" | cut -d' ' -f2- | cut -c1-80)
  [ -n "$v" ] && ok "$h: $v" || no "$h  YOK"
done

echo
echo "[4] Sunucu bilgisi sızdırma"
for h in "server" "x-powered-by"; do
  v=$(echo "$H" | grep -i "^$h:" | cut -d' ' -f2-)
  [ -n "$v" ] && wr "$h: $v" || ok "$h yok"
done

echo
echo "[5] Açıkta olmaması gereken yollar"
for p in /_kaynak/ /_kaynak/WEB-SITESI-BRIEF.md /_kaynak/komisyon.pdf \
         /build.py /README.md /.git/config /.htaccess /_headers \
         /genctetsiad-site.zip /cgi-bin/ /assets/ /assets/fonts/; do
  c=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$B$p")
  case "$c" in
    200) no "$c  $p   <-- ERİŞİLEBİLİR" ;;
    403|404) ok "$c  $p" ;;
    *)   wr "$c  $p" ;;
  esac
done

echo
echo "[6] Dizin listeleme"
body=$(curl -s --max-time 20 "$B/assets/" | head -c 4000)
echo "$body" | grep -qi 'index of\|<title>Directory' \
  && no "/assets/ listeleniyor - dosya listesi görünüyor" \
  || ok "/assets/ listelenmiyor"

echo
echo "[7] Dış istek var mı (gizlilik)"
ext=$(curl -s --max-time 20 "$B/" | grep -oE 'https?://[a-zA-Z0-9.-]+' \
      | grep -v "$D" | sort -u)
[ -z "$ext" ] && ok "sayfa hiçbir dış alan adına istek yapmıyor" \
              || { wr "dış alan adları:"; echo "$ext" | sed 's/^/       /'; }

echo
echo "[8] TLS sertifikası"
echo | openssl s_client -connect "$D:443" -servername "$D" 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates 2>/dev/null | sed 's/^/     /' \
  || wr "openssl yok veya bağlanılamadı"

echo
echo "[9] Yazı tipleri ve görseller"
for f in /assets/site.css /assets/fonts.css /assets/site.js \
         /assets/fonts/plus-jakarta-sans-300-normal-latin.woff2 \
         /assets/fabrika-ziyareti.webp /assets/favicon.png; do
  c=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$B$f")
  [ "$c" = "200" ] && ok "$c  $f" || no "$c  $f"
done

echo
echo "[10] Sayfa boyutu ve süre"
curl -s -o /dev/null --max-time 30 \
  -w "     index.html  %{size_download} bayt   %{time_total}s   HTTP %{http_code}\n" "$B/"

echo
echo "=============================================="
echo " bitti"
echo "=============================================="
