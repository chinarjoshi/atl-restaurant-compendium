from datetime import time
from googlemaps import Client
from summarizer import summarizer
from bs4 import BeautifulSoup

gmaps = Client(key='AIzaSyDr7db_xqI9M5Cz3lx3EWsfgpiySAbVt3k')
summarize = summarizer(3)

with open('site.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Step 1: Parse the soup and assemble basic information about each restaurant
@dataclass
class Restaurant:
    name: str
    description: str
    price: int
    city: str
    address: str
    car_dist: time
    bike_dist: time

    @classmethod
    def from_atl_mag(cls, soup, maps):
        header = 'div.restRight > div.restInfo > div.'
        address = soup.select_one(header + 'address').text
        return cls(
            soup.select_one('h2.restName').text,
            summarize(soup.select_one('div.restLeft > p').text),
            soup.select_one(header + 'price').text.count('$'),
            soup.select_one(header + 'neighbor').text,
            address,
            # get_distance(maps, address, mode='driving'),
            # get_distance(maps, address, mode='bicycling')
            1,
            2,
        )

def build_restaurant(soup, maps):
    header = 'div.restRight > div.restInfo > div.'
    address = soup.select_one(header + 'address').text
    return {
        'name': soup.select_one('h2.restName').text,
        'description': summarize(soup.select_one('div.restLeft > p').text),
        'price': soup.select_one(header + 'price').text.count('$'),
        'city': soup.select_one(header + 'neighbor').text,
        'address': address,
        # 'car_dist': get_distance(maps, address, mode='driving'),
        # 'bike_dist': get_distance(maps, address, mode='bicycling')
        'car_dist': 1,
        'bike_dist': 2,
    }

def get_distance(
    gmaps: Client,
    dest: str,
    origin: str = '112 Bobby Dodd Way NW, Atlanta, GA 30332',
    mode: str = 'driving'
) -> time:
    distance = gmaps.distance_matrix(origin, dest + ' Atlanta', mode=mode)['rows'][0]['elements'][0]['duration']['text']
    tokens = distance.split()
    if 'hour' in tokens:
        return time(int(tokens[0]), int(tokens[2]))
    else:
        return time(0, int(tokens[0]))

restaurants = [Restaurant.from_atl_mag(r, gmaps) for r in soup.select('div.restLRContainer')]


# Step 2: Update the restaurants with their distance from the user

# def distances_from_restaurants(
#     restaurants: list[Restaurant],
#     origin: str = '112 Bobby Dodd Way NW, Atlanta, GA 30332') -> Distances:
#     """Update list of restaurants with driving, walking, and bicycling distances from origin."""

    
#     dists = [
#         [
#             v['duration']['text']
#             for v in maps.distance_matrix(origin, [r.address for r in restaurants][:20], mode=mode)['rows'][0]['elements']
#             if v['status'] == 'OK'
#         ]
#         for mode in ['driving', ]#'bicycling', 'walking']
#     ]

#     for r, d, b, w in zip(restaurants, dists[0], dists[1], dists[2]):
#         r.distances = Distances(driving=d, bicycling=b, walking=w)

# distances_from_restaurants(restaurants)

# print(restaurants)
