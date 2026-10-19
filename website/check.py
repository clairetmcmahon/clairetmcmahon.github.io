#!/usr/bin/env python3
"""Check generated navigation, assets, and paper destinations."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'website/content.json').read_text())
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls, self.ids = [], []
        self.headings = 0
        self.lang = self.has_main = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.headings += tag == 'h1'
        self.lang |= tag == 'html' and attrs.get('lang') == 'en'
        self.has_main |= tag == 'main'
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src', 'data'):
            if key in attrs:
                self.urls.append(attrs[key])
pages = ['index.html', 'research/index.html', 'blog/index.html', 'tools/index.html', 'cv/index.html', '404.html']
checked = 0
for filename in pages:
    parsed = Page()
    parsed.feed((ROOT / filename).read_text())
    assert parsed.headings == 1, (filename, 'must have one h1')
    assert parsed.lang and parsed.has_main, (filename, 'missing document landmarks')
    assert len(parsed.ids) == len(set(parsed.ids)), (filename, 'duplicate id')
    for url in parsed.urls:
        parts = urlsplit(url)
        assert not parts.path.startswith('/http'), (filename, 'external URL rendered as local path', url)
        if parts.scheme in ('https', 'mailto'):
            continue
        assert not parts.scheme, (filename, 'unexpected URL scheme', url)
        if not parts.path:
            assert not parts.fragment or parts.fragment in parsed.ids, (filename, 'missing anchor', url)
            continue
        target = ROOT / unquote(parts.path).lstrip('/')
        if parts.path.endswith('/'):
            target /= 'index.html'
        assert target.is_file(), (filename, 'missing local file', url)
        checked += 1
    if filename == 'research/index.html':
        for paper in DATA['papers']:
            assert paper['url'] in parsed.urls, ('paper title missing destination', paper['title'])
    if filename == 'blog/index.html':
        for post in DATA['posts']:
            assert post['url'] in parsed.urls, ('post missing destination', post['title'])
assert (ROOT / '.nojekyll').is_file()
assert (ROOT / 'files/McMahon_CV.pdf').read_bytes().startswith(b'%PDF')
print(f'PASS: {len(pages)} pages, {checked} local links/assets, 5 paper destinations, 5 blog destinations, and CV PDF.')
