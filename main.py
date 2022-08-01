from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from datetime import time

from summarizer import summarizer
from make_data import get_distance, get_site, gmaps

data = Path("data")
summarize = summarizer(3)  # 3 sentences of description

if not (data / 'site.html').exists():
    get_site(url='https://www.atlantamagazine.com/50bestrestaurants/', path=data/'site.html')

# Step 1: Parse the soup and assemble information about each restaurant
def build_restaurant(r: BeautifulSoup) -> dict[str, str]:
    """Parses the soup and assembles information about a restaurant."""
    price = r.select_one("div.price")
    span = price.select_one("span")
    if span:
        span.decompose()

    website = r.select_one("em > a")
    website = website.text if website else 'None'

    address = r.select_one("div.address").text
    city = r.select_one("div.neighbor").text
    car_dist = get_distance(gmaps, address, city, mode='driving')
    bike_dist = get_distance(gmaps, address, city, mode='bicycling')

    return {
        "name": r.select_one("h2.restName").text,
        "description": summarize(r.select_one("div.restLeft > p").text),
        "price": price.text.count('$'),
        "city": city,
        "address": address,
        "website": website,
        "bike_dist": bike_dist,
        "car_dist": car_dist,
        "is_bikable": bike_dist < time(0, 20)
    }


with open(data / "site.html") as f:
    soup = BeautifulSoup(f, "html.parser")

df = pd.DataFrame(
    build_restaurant(r) for r in soup.select("div.restLRContainer")
)

with open(data / 'output.csv', 'w') as f:
    df.to_csv(f, index=False)
