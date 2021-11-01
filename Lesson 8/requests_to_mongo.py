from pymongo import MongoClient
from pprint import pprint
client = MongoClient('127.0.0.1', 27017)
mongo_base = client.insta
data = mongo_base['parsed_data']


def get_list_subs(user_who_has_friends):
    result = []
    for x in data.find({'parsed_from_user': user_who_has_friends, 'follower': 1}):
        if x['username'] in result:
            continue
        else:
            result.append(x['username'])
    return result


def get_list_following(user_who_follows_on_people):
    result = []
    for x in data.find({'parsed_from_user': user_who_follows_on_people, 'following': 1}):
        if x['username'] in result:
            continue
        else:
            result.append(x['username'])
    return result


a = get_list_subs('da_weeeeed')
pprint(a)
b = get_list_following('da_weeeeed')
pprint(b)
