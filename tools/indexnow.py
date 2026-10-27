"""يبلّغ محركات البحث (Bing وYandex وNaver وSeznam…) بالصفحات الجديدة والمتغيّرة فورًا عبر IndexNow.

يقرأ الروابط وتواريخ lastmod من خريطة الموقع، ويرسل كل رابط جديد أو تغيّر تاريخه منذ آخر إرسال
(أو الكل بخيار --all). المفتاح علني بطبيعته (ملف <key>.txt في جذر الموقع).
بخيار --wait ينتظر حتى تُنشر الصفحات فعلًا (تطابق خريطة الموقع المنشورة المحلية) قبل التبليغ، فلا يزورها Bing قبل النشر."""
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOST = 'ishraqa.app'
SENT = ROOT / 'tools' / '.indexnow_sent.json'


def deployed(xml, timeout=1200, step=30):   # ذاكرة GitHub Pages المؤقتة حتى 10 دقائق
    """ينتظر نشر GitHub Pages: حين تطابق خريطة الموقع المنشورة الخريطةَ المحلية تكون الصفحات الجديدة قد نُشرت"""
    end = time.time() + timeout
    while time.time() < end:
        try:
            req = urllib.request.Request(f'https://{HOST}/sitemap.xml?nocache={int(time.time())}',
                                         headers={'User-Agent': 'ishraqa-indexnow', 'Cache-Control': 'no-cache'})
            if urllib.request.urlopen(req, timeout=30).read().decode('utf-8').strip() == xml.strip():
                return True
        except Exception:
            pass
        time.sleep(step)
    print('site not deployed yet; will retry next run')
    return False


def main():
    key = next(p.stem for p in ROOT.glob('*.txt') if re.fullmatch(r'[0-9a-f]{32}', p.stem))
    xml = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    urls = dict(re.findall(r'<loc>([^<]+)</loc>(?:<lastmod>([^<]+)</lastmod>)?', xml))
    sent = json.loads(SENT.read_text()) if SENT.exists() else {}
    if isinstance(sent, list):          # الصيغة القديمة: قائمة روابط بلا تواريخ
        sent = dict.fromkeys(sent, '')
    new = list(urls) if '--all' in sys.argv else [u for u, d in urls.items() if sent.get(u) != d]
    if not new:
        print('nothing new')
        return
    if '--wait' in sys.argv and not deployed(xml):
        return
    status = None
    for i in range(0, len(new), 10000):
        body = {'host': HOST, 'key': key, 'keyLocation': f'https://{HOST}/{key}.txt', 'urlList': new[i:i + 10000]}
        req = urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps(body).encode(),
                                     method='POST', headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            status = urllib.request.urlopen(req, timeout=60).status
        except urllib.error.HTTPError as e:
            print('indexnow error', e.code)
            return
    sent.update({u: urls[u] for u in new})
    sent = {u: d for u, d in sent.items() if u in urls}
    SENT.write_text(json.dumps(sent, ensure_ascii=False, indent=0, sort_keys=True))
    print(f'indexnow: {len(new)} urls -> {status}')


if __name__ == '__main__':
    main()
