# The Best Restaurants of Atlanta

From someone who lives to eat, here is a [database](https://github.com/chinarjoshi/atl-restaurant-compendium/blob/main/compendium.csv) of expert reccomended restaurants, comprising of [Atlanta Eater's top 38](https://atlanta.eater.com/maps/38-best-restaurants-in-atlanta), [Atlanta Eats Midtown Bucket list](https://www.atlantaeats.com/blog/midtown-atlanta-restaurant-bucket-list/), and [Atlanta Magazine's top 75](https://www.atlantamagazine.com/50bestrestaurants/).

The columns labels are as follows:
* 'name' (str): Name of the restaurant
* 'price' (int): Price level from 1-4 inclusive
* 'rating' (float): User ratings from 1.0-5.0 inclusive
* 'user_ratings_total' (int): Number of ratings to back it up
* 'driving' (timestamp): Time it takes to drive from Towers residence hall
* 'bicycling' (timestamp): Time it takes to bike from Towers residence hall
* 'worth_driving' (bool): 'driving' <= 20 mins
* 'worth_bicycling' (bool): 'bicycling' <= 20 mins
* 'multiple_mentions' (bool): Whether multiple articles reccomend the same restaurant
* 'description' (str): 3 sentence summary of the journalist's description
* 'website' (str): Restaurant website and menu
* 'formatted_address' (str): Street address
* 'search_keywords' (str): Keywords used to find the restaurant on Maps
* 'place_id' (str): ID in Google's Place database

Data is scraped from the articles, then augmented using Google Maps [Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix) and [Places API](https://developers.google.com/maps/documentation/places/web-service) to be more useful for Georgia Tech students living in east campus dorms.

The database is [compendium.csv](https://github.com/chinarjoshi/atl-restaurant-compendium/blob/main/compendium.csv), and methodology is [main.ipynb](https://github.com/chinarjoshi/atl-restaurant-compendium/blob/main/main.ipynb).
