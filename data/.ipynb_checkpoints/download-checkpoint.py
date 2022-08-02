#!/usr/bin/env python3

from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://www.atlantaeats.com/blog/midtown-atlanta-restaurant-bucket-list/')
r.html.render()

with open('midtown.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
