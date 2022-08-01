from googlemaps import Client
from datetime import time
from requests_html import HTMLSession
from pathlib import Path

maps = Client(key="AIzaSyDr7db_xqI9M5Cz3lx3EWsfgpiySAbVt3k")
data = Path(__file__).parent / 'data'

def get_distance(
    gmaps: Client,
    dest: str,
    city: str,
    origin: str = "112 Bobby Dodd Way NW, Atlanta, GA 30332",
    mode: str = "driving",
) -> time:
    """Returns time distance between two points by a given mode of transport."""
    dist = gmaps.distance_matrix(origin, f'{dest}, {city}', mode=mode)
    dist = dist["rows"][0]["elements"][0]["duration"]["text"]
    tokens = dist.split()
    if "hour" in tokens:
        return time(int(tokens[0]), int(tokens[2]))
    else:
        return time(0, int(tokens[0]))

def get_html(url: str) -> None:
    """Returns html of a given url."""
    if (data / 'site.html').exists():
        return

    session = HTMLSession()
    site = session.get(url)
    site.html.render()
    with open(data / 'site.html', 'w', encoding='utf-8') as f:
        print(site.text, file=f)
