"""يبلّغ محركات البحث (Bing وYandex وNaver وSeznam…) بالصفحات الجديدة والمتغيّرة فورًا عبر IndexNow.

يقرأ الروابط وتواريخ lastmod من خريطة الموقع، ويرسل كل رابط جديد أو تغيّر تاريخه منذ آخر إرسال
(أو الكل بخيار --all). المفتاح علني بطبيعته (ملف <key>.txt في جذر الموقع)."""
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOST = 'ishraqa.otwox.com'
SENT = ROOT / 'tools' / '.indexnow_sent.json'


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
