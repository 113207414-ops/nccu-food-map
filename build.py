import json
import re
from html import escape as h
from pathlib import Path
from urllib.parse import quote_plus, urlparse

ROOT = Path(__file__).resolve().parent
CATEGORIES = ('飯類', '麵食', '水餃', '咖哩', '素食')
AREAS = ('指南路二段', '萬壽路', '校園內')

def page(title, prefix, body, script=''):
    return f"""<!doctype html>
<html lang="zh-Hant">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(title)}</title><link rel="stylesheet" href="{prefix}assets/style.css">{script}</head>
<body><header><nav class="wrap"><a href="{prefix}index.html">政大周邊吃飯地圖</a></nav></header>
<main class="wrap">{body}</main>
<footer class="wrap">政大正餐指南 · 店家資料以各頁公開來源為準</footer></body></html>
"""

def validate(shops):
    slugs = set()
    for shop in shops:
        slug = shop['slug']
        if not re.fullmatch(r'[a-z]+(?:-[a-z]+)*', slug) or slug in slugs:
            raise ValueError(f'無效或重複 slug：{slug}')
        slugs.add(slug)
        if shop['category'] not in CATEGORIES or shop['area'] not in AREAS:
            raise ValueError(f'分類或街區有誤：{slug}')
        if not all(shop[field].strip() for field in ('name', 'dish', 'address')):
            raise ValueError(f'店名、餐點或地址空白：{slug}')
        if not shop['sources'] or any(urlparse(source['url']).scheme != 'https' for source in shop['sources']):
            raise ValueError(f'缺少 HTTPS 來源：{slug}')

def detail(shop, number):
    address = shop['address']
    maps = 'https://www.google.com/maps/search/?api=1&query=' + quote_plus(shop['name'] + ' ' + address)
    sources = ''.join(f'<li><a href="{h(s["url"])}">{h(s["label"])}</a></li>' for s in shop['sources'])
    price = shop.get('price')
    price_text = (f'<dt>參考價格</dt><dd>NT${price["amount"]} · {h(price["kind"])} · {h(price["checked"])} 查閱</dd>'
                  if price else '')
    note = f'<p>{h(shop["note"])}</p>' if shop.get('note') else ''
    return page(shop['name'] + '｜政大周邊吃飯地圖', '../', f'''
<a class="back" href="../index.html#shops">← 返回店家列表</a>
<article class="detail">
<p class="eyebrow">店家 {number:02d} ／ {h(shop['category'])}</p>
<h1>{h(shop['name'])}</h1>
<dl><dt>主打餐點</dt><dd>{h(shop['dish'])}</dd>{price_text}
<dt>地址</dt><dd>{h(address)}</dd></dl>
{note}<a class="primary" href="{maps}">在 Google Maps 查看</a>
<h2>資料來源</h2><ul>{sources}</ul></article>''')

def home(shops):
    groups = {area: [] for area in AREAS}
    cards = []
    for number, shop in enumerate(shops, 1):
        category = h(shop['category'])
        name = h(shop['name'])
        url = f'shops/{shop["slug"]}.html'
        groups[shop['area']].append(
            f'<a class="pin" href="{url}" data-category="{category}"><b>{number:02d}</b>{name}</a>')
        featured = ' · 指定餐點' if shop.get('featured') else ''
        cards.append(f'''<a class="card" href="{url}" data-category="{category}">
<p class="eyebrow">{number:02d} ／ {category}{featured}</p><h3>{name}</h3>
<p class="dish">{h(shop['dish'])}</p><p class="address">{h(shop['address'])}</p><span>查看店家 →</span></a>''')
    map_rows = ''.join(f'<section class="street"><h3>{area}</h3><div>{"".join(pins)}</div></section>'
                       for area, pins in groups.items())
    buttons = ''.join(f'<button type="button" aria-pressed="false" data-filter="{c}">{c}</button>'
                      for c in CATEGORIES)
    return page('政大周邊吃飯地圖', '', f'''
<section class="hero"><p class="eyebrow">NCCU FOOD MAP ／ 木柵・指南路</p>
<h1>下課，今天吃什麼？</h1><p>從政大正門出發，看看附近有哪些飯、麵、水餃、咖哩和素食。</p>
<a href="#shops">直接看 {len(shops)} 家店 ↓</a></section>
<section class="filters" aria-label="餐點分類" hidden>
<button type="button" aria-pressed="true" data-filter="">全部</button>{buttons}</section>
<section class="map"><h2>街區示意圖</h2><p>依地址街區分組，非比例地圖。點店家標記可開啟店家頁與導航。</p>{map_rows}</section>
<section id="shops"><div class="listing"><h2>店家列表</h2><p id="count" aria-live="polite">{len(shops)} 家店</p></div>
<div class="grid">{"".join(cards)}</div></section>''',
                '<script src="assets/filter.js" defer></script>')

def main():
    shops = json.loads((ROOT / 'data/restaurants.json').read_text())
    validate(shops)
    (ROOT / 'shops').mkdir(exist_ok=True)
    (ROOT / 'index.html').write_text(home(shops))
    for number, shop in enumerate(shops, 1):
        (ROOT / 'shops' / (shop['slug'] + '.html')).write_text(detail(shop, number))

if __name__ == '__main__':
    main()
