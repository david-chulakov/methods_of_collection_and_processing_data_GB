import requests
import json
import urllib.request

TOKEN = ""

URL = "https://api.nasa.gov/planetary/apod?"

params = {'api_key': TOKEN}


def get_info():
    """
    Function prints info about this day in Nasa history and saves image of day
    """
    req = requests.get(URL, params)
    data = json.loads(req.text)
    with open(f"{data['date']} - in nasa history.txt", "w") as f_obj:
        f_obj.write(f"Date - {data['date']}\nExplanation: {data['explanation']}")
        f_obj.close()

    urllib.request.urlretrieve(data['url'], f"image_of_the_day-{data['date']}.jpg")


if __name__ == "__main__":
    get_info()