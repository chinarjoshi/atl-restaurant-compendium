import os
from datetime import time
from pathlib import Path

import numpy as np
import pandas as pd
from googlemaps import Client
from requests_html import HTMLSession

gmaps = Client(key=os.environ["GOOGLE_API_KEY"])


def get_place(df: pd.DataFrame, gmaps: Client) -> pd.DataFrame:
    """Creates dataframe with place information.

    Expects a dataframe with column "search_term". Returns columns "place_id", "price_level",
    "rating", "user_ratings_total", and "formatted_address".
    Uses Google Places API.
    """
    categories = (
        "place_id",
        "price_level",
        "rating",
        "user_ratings_total",
        "formatted_address",
    )
    columns = {column: [] for column in categories}

    for search_term in df["search_term"]:
        places = gmaps.places(search_term, location="33.773521, -84.391311")["results"][0]
        for category in categories:
            columns[category].append(places[category])

    return pd.DataFrame(columns)


def get_distance(
    df: pd.DataFrame,
    gmaps: Client,
    origin: str = "112 Bobby Dodd Way NW, Atlanta, GA 30332",
) -> pd.DataFrame:
    """Returns time between two points by a given mode of transport.

    Expects a dataframe with column "place_id". Returns columns "car_dist",
    "bike_dist", and "is_bikable".
    Uses Google Distance Matrix API.
    """
    # 3 columns to be assembled
    distances = {
        column: pd.Series() for column in ("driving", "bicycling", "is_bikable")
    }

    def time_from_dist(time_str: str) -> time:
        """Returns travel time from a distance object."""
        tokens = time_str["distance"]["text"].split()
        if "hour" in tokens:
            return time(int(tokens[0]), int(tokens[2]))
        else:
            return time(0, int(tokens[0]))

    # Iterate over batches of 25 rows
    for batch in np.array_split(df, 25):
        place_ids = list("place_id:" + batch["place_id"])

        for mode in ("driving", "bicycling"):
            dist = gmaps.distance_matrix(origin, place_ids, mode=mode)["rows"][0]["elements"]
            dist = pd.Series(map(time_from_dist, dist))
            distances[mode] = distances[mode].append(dist)

            if mode == "bicycling":
                distances["is_bikable"] = distances["is_bikable"].append(
                    dist < time(0, 20)
                )

    return pd.DataFrame(distances)


def verify_resource(url: str, path: Path) -> None:
    """Writes fully rendered HTML to Path."""
    if path.exists():
        return

    session = HTMLSession()
    site = session.get(url)
    site.html.render(timeout=15)
    with open(path, "w", encoding="utf-8") as f:
        print(site.text, file=f)
