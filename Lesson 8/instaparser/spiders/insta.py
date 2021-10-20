import scrapy
from instaparser.items import InstaparserItem
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    def __init__(self, query):
        self.insta_login_link = "https://www.instagram.com/accounts/login/ajax/"
        self.login_username = 'da_weeeeed'
        self.login_enc_password = '#PWD_INSTAGRAM_BROWSER:10:1634650812:AalQADcf6LXqLz2N1Ra+FjpNY2tMfZ5fGWXEz3MVgyrDsRdJr2lFO/2mIS/nDpezlzjBN4hFPxIpoPykPIVsSklBH7SLRQPbZRtEAzeBm85Ly/Z6652kuaF0TxP3cRd7LsD839qdLrsm3+JB'
        self.users_for_parse = query
        self.get_posts_url = 'https://i.instagram.com/api/v1/feed/user/'
        self.get_subs_url = 'https://i.instagram.com/api/v1/friendships/'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.insta_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.login_username,
                      'enc_password': self.login_enc_password},
            headers={'x-csrftoken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for username in self.users_for_parse:
                yield response.follow(
                    f'/{username}',
                    callback=self.user_parse,
                    cb_kwargs={'username': username}
                )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables_for_subs = {'count': 12}
        variables_for_followers = {'count': 12}
        url_subs = f'{self.get_subs_url}{user_id}/following/?{urlencode(variables_for_subs)}'
        url_followers = f'{self.get_subs_url}{user_id}/followers/?{urlencode(variables_for_followers)}'
        yield response.follow(url_subs,
                              callback=self.subs_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'following': 1,
                                         'follower': 0,
                                         'variables_for_subs': deepcopy(variables_for_subs)})

        yield response.follow(url_followers,
                              callback=self.followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'following': 0,
                                         'follower': 1,
                                         'variables_for_followers': deepcopy(variables_for_followers)})

    def followers_parse(self, response: HtmlResponse, username, user_id, following, follower, variables_for_followers):
        j_data = response.json()
        variables = {'count': 12}
        if j_data.get('big_list'):
            variables_for_followers['max_id'] = j_data.get('next_max_id')
            url_followers = f'{self.get_subs_url}{user_id}/followers/?{urlencode(variables_for_followers)}'
            yield response.follow(url_followers,
                                    callback=self.followers_parse,
                                    cb_kwargs={"username": username,
                                               "user_id": user_id,
                                               'following': following,
                                               'follower': follower,
                                               'variables_for_followers': deepcopy(variables_for_followers)})

            for user in j_data.get('users'):
                yield response.follow(f'https://www.instagram.com/{user.get("username")}/',
                                      callback=self.user_url_parse,
                                      cb_kwargs={'username': user.get("username"),
                                                 'user_id': user.get("pk"),
                                                 'following': following,
                                                 'follower': follower,
                                                 'parsed_from_user': username,
                                                 'parsed_from_user_id': user_id,
                                                 'variables': variables})

        print()

    def subs_parse(self, response: HtmlResponse, username, user_id, following, follower, variables_for_subs):
        j_data = response.json()
        variables = {'count': 12}
        if j_data.get('big_list'):
            variables_for_subs['max_id'] = j_data.get('next_max_id')
            url_subs = f'{self.get_subs_url}{user_id}/following/?{urlencode(variables_for_subs)}'
            yield response.follow(url_subs,
                                  callback=self.subs_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'following': following,
                                             'follower': follower,
                                             'variables_for_subs': deepcopy(variables_for_subs)})

            for user in j_data.get('users'):
                yield response.follow(f'https://www.instagram.com/{user.get("username")}/',
                                      callback=self.user_url_parse,
                                      cb_kwargs={'username': user.get("username"),
                                                 'user_id': user.get("pk"),
                                                 'following': following,
                                                 'follower': follower,
                                                 'parsed_from_user': username,
                                                 'parsed_from_user_id': user_id,
                                                 'variables': variables})

    def user_url_parse(self, response: HtmlResponse, username, user_id, following, follower, parsed_from_user, parsed_from_user_id, variables):
        yield response.follow(f'https://i.instagram.com/api/v1/feed/user/{user_id}/?count=12',
                                callback=self.user_posts_parse,
                                cb_kwargs={'username': username,
                                           'user_id': user_id,
                                           'following': following,
                                           'follower': follower,
                                           'parsed_from_user': parsed_from_user,
                                           'parsed_from_user_id': parsed_from_user_id,
                                           'variables': variables})

    def user_posts_parse(self, response: HtmlResponse, username, user_id, following, follower, parsed_from_user, parsed_from_user_id, variables):
        j_data = response.json()
        if j_data.get('more_available'):
            variables['max_id'] = j_data.get('next_max_id')
            url_posts = f'{self.get_posts_url}{user_id}?{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_posts_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'following': following,
                                             'follower': follower,
                                             'parsed_from_user': parsed_from_user,
                                             'parsed_from_user_id': parsed_from_user_id,
                                             'variables': deepcopy(variables)}
                                  )
            posts = j_data.get('items')
            for post in posts:
                item = InstaparserItem(
                    user_id=user_id,
                    username=username,
                    following=following,
                    follower=follower,
                    parsed_from_user=parsed_from_user,
                    parsed_from_user_id=parsed_from_user_id,
                    photo=post.get('image_versions')[0].get('url'),
                    likes=post.get('like_count'),
                    post_data=post
                    )
                yield item


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')