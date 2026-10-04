"""يبلّغ محركات البحث (Bing وYandex وNaver…) بالصفحات الجديدة فورًا عبر IndexNow.

يقرأ روابط المقالات من خريطة الموقع، ويرسل ما أُضيف منذ آخر إرسال (أو الكل بخيار --all).
المفتاح علني بطبيعته (ملف <key>.txt في جذر الموقع)."""
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOST = 'ishraqa.otwox.com'
SENT = ROOT / 'tools' / '.indexnow_sent.json'


def main():
    key = next(p.stem for p in ROOT.glob('*.txt') if re.fullmatch(r'[0-9a-f]{32}', p.stem))
    urls = re.findall(r'<loc>([^<]+)</loc>', (ROOT / 'sitemap.xml').read_text(encoding='utf-8'))
    sent = set(json.loads(SENT.read_text())) if SENT.exists() else set()
    new = urls if '--all' in sys.argv else [u for u in urls if u not in sent]
    if not new:
        print('nothing new')
        return
    body = {'host': HOST, 'key': key, 'keyLocation': f'https://{HOST}/{key}.txt', 'urlList': new}
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps(body).encode(),
                                 method='POST', headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        status = urllib.request.urlopen(req, timeout=60).status
    except urllib.error.HTTPError as e:
        print('indexnow error', e.code)
        return
    SENT.write_text(json.dumps(sorted(sent | set(new)), ensure_ascii=False))
    print(f'indexnow: {len(new)} urls -> {status}')


if __name__ == '__main__':
    main()
