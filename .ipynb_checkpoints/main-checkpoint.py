from collections.abc import Generator
from datetime import time
from itertools import chain
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from google import get_distance, get_place, gmaps, verify_resource
from summarizer import summarize


# Step 1: Parse the soup and assemble information about each restaurant
def build_atl_mag_restaurants(
    soup: BeautifulSoup,
) -> Generator[dict[str, str], None, None]:
    """Parses the soup and assembles information about a restaurant."""
    for r in soup.select("div.restLRContainer"):
        price = r.select_one("div.price")
        span = price.select_one("span")
        if span:
            span.decompose()

        website = r.select_one("em > a")
        website = website["href"] if website else "None"

        address = r.select_one("div.address").text
        city = r.select_one("div.neighbor").text

        yield {
            "name": r.select_one("h2.restName").text,
            "description": summarize(r.select_one("div.restLeft > p").text),
            # "price": price.text.count('$'),
            "search_term": f"{address}, {city} restaurant",
            "website": website,
            "source": "atl_mag",
        }


def build_atl_eater_restaurants(
    soup: BeautifulSoup,
) -> Generator[dict[str, str], None, None]:
    for r in soup.select("main > section.c-mapstack__card"):
        website = r.select_one("div.c-mapstack__info > info > div > a")
        website = website["href"] if website else "None"
        yield {
            "name": r.select_one("div.c-mapstack__card-hed > div > h1").text,
            "description": summarize(r.select_one("div.c-entry-content > p").text),
            "search_term": f'{r.select_one("div.c-mapstack__address > a").text} restaurant',
            "website": website,
            "source": "atl_eater",
        }


def build_midtown_restaurants(
    soup: BeautifulSoup,
) -> Generator[dict[str, str], None, None]:
    content = soup.select_one("div.entry_content")

    titles = content.select("h2 > strong")[:-1]
    descriptions = content.select("p")[2:-2]
    if len(titles) != 10 and len(descriptions) != 10:
        exit("Incorrect scraping on midtown website.")

    for title, description in zip(titles, descriptions):
        yield {
            "name": title.text,
            "description": summarize(description.text),
            "search_term": f"{title.text} midtown restaurant",
            "website": title.select_one("a")["href"],
            "source": "midtown",
        }


data = Path("data")
website_metadata = [
    {
        "url": "https://www.atlantamagazine.com/50bestrestaurants/",
        "name": "atl_mag.html",
    },
    {
        "url": "https://atlanta.eater.com/maps/38-best-restaurants-in-atlanta",
        "name": "atl_eater.html",
    },
    {
        "url": "https://www.atlantaeats.com/blog/midtown-atlanta-restaurant-bucket-list/",
        "name": "midtown.html",
    },
]
for site in website_metadata:
    verify_resource(site["url"], data / site["name"])


with open(data / "atl_mag.html") as fm, open(data / "atl_eater.html") as fe, open(
    data / "midtown.html"
) as fm:
    mag = BeautifulSoup(fm, "html.parser")
    eater = BeautifulSoup(fe, "html.parser")
    midtown = BeautifulSoup(fm, "html.parser")

df = pd.DataFrame(
    chain(
        build_atl_mag_restaurants(mag),
        build_atl_eater_restaurants(eater),
        build_midtown_restaurants(midtown),
    )
)

df = df.append(get_place(df, gmaps))
df = df.append(get_distance(df, gmaps))

with open(data / "output.csv", "w") as f:
    df.to_csv(f, index=False)
