import sys
from io import BytesIO
import requests
from PIL import Image
from count_zoom_for_map import count_zoom_for_map

toponym_to_find = 'Саратов, Университетская, 65/73'

geocoder_api_server = " ".join(sys.argv[1:])

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
lower_corner = toponym['boundedBy']['Envelope']['lowerCorner'].split()
upper_corner = toponym['boundedBy']['Envelope']['upperCorner'].split()
width_degrees = float(upper_corner[0]) - float(lower_corner[0])
height_degrees = float(upper_corner[1]) - float(lower_corner[1])

delta = str(count_zoom_for_map(width_degrees, height_degrees))

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    'pt': f'{",".join([toponym_longitude, toponym_lattitude])},pmwtm',
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"

response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
