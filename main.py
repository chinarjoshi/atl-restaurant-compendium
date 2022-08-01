from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from datetime import time, datetime

from summarizer import summarizer

data = Path("data")
summarize = summarizer(3)  # 3 sentences of description

# Step 1: Parse the soup and assemble information about each restaurant
def build_restaurant(r: BeautifulSoup) -> dict[str, str]:
    """Parses the soup and assembles information about a restaurant."""
    price = r.select_one("div.price")
    span = price.select_one("span")
    if span:
        span.decompose()

    website = r.select_one("em > a")
    website = website.text if website else 'None'

    return {
        "name": r.select_one("h2.restName").text,
        "description": summarize(r.select_one("div.restLeft > p").text),
        "price": price.text.count('$'),
        "city": r.select_one("div.neighbor").text,
        "address": r.select_one("div.address").text,
        "website": website,
    }


with open(data / "site.html") as f:
    soup = BeautifulSoup(f, "html.parser")

restaurants = pd.DataFrame(
    build_restaurant(r) for r in soup.select("div.restLRContainer")
)
distances = pd.read_csv(data / "dist.csv")

df = restaurants.join(distances)

def is_bikable(row) -> bool:
    """Returns True if the restaurant is bikable."""
    return datetime.strptime(row['bike_dist'], '%H:%M:%S').time() < time(0, 20)

df['is_bikable'] = df.apply(is_bikable, axis=1)
