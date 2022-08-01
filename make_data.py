import os
from datetime import time
from pathlib import Path

from googlemaps import Client
from requests_html import HTMLSession

gmaps = Client(key=os.environ['GOOGLE_API_KEY'])

def get_distance(
    gmaps: Client,
    dest: str,
    city: str,
    origin: str = "112 Bobby Dodd Way NW, Atlanta, GA 30332",
    mode: str = "driving",
) -> time:
    """Returns time distance between two points by a given mode of transport."""
    dist = gmaps.distance_matrix(origin, f"{dest}, {city}", mode=mode)
    if dist["rows"][0]["elements"][0]["status"] != "OK":
        dist = gmaps.distance_matrix(origin, f"{dest}, Atlanta", mode=mode)
    dist = dist["rows"][0]["elements"][0]["duration"]["text"]
    tokens = dist.split()
    if "hour" in tokens:
        return time(int(tokens[0]), int(tokens[2]))
    else:
        return time(0, int(tokens[0]))


def get_site(url: str, path: Path) -> None:
    """Writes fully rendered HTML to Path."""
    data = Path(__file__).parent / "data"
    if (data / "site.html").exists():
        return

    session = HTMLSession()
    site = session.get(url)
    site.html.render()
    with open(path, "w", encoding="utf-8") as f:
        print(site.text, file=f)
