import requests
import json
from pprint import pprint

TOKEN = ""
URL = "https://api.github.com/users/"


def info(user: str):
    """
    Function prints info about github user and writes it in data.json
    :param user: github username
    """
    req = requests.get(URL + user)
    data = json.loads(req.text)
    print(f"username - {data['login']}\nName - {data['name']}\nProfile description - {data['bio']}\npublic repos - {data['public_repos']}\nfollowers - {data['followers']}")

    with open('data.json', 'w') as f:
        json.dump(data, f)

    print("Data successfully saved in data.json")


if __name__ == "__main__":
    username = input("Enter github username: ")
    info(username)

