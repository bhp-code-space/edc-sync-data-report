import unittest

from django.test import TestCase
from datetime import datetime

import json

import pandas as pd

import tweepy

class JsonObject:

    def __init__(self, data):
        self.data = data


class CollectSummaryDataTestCase(unittest.TestCase):

    def test_tweets(self):
        api_key='HHN6g177c0hREDmQzmSbYDcK8'
        api_key_secret='GoWIHn6Nlu5XQJSK4tTCkYXPNXU7atxYbdMC9OXRVYEpKQi9wz'
        access_token='1553104206873100288-odkHdn1vDyQKkMdKarSyNor52uAQkg'
        access_token_secret='6agORnChD1GoYJmM3QA6a4irlNe5B2bC3iDRi3yb5CjcL'
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api_v2 = tweepy.Client(bearer_token=None, consumer_key=api_key, consumer_secret=api_key_secret,
                               access_token=access_token, access_token_secret=access_token_secret)

        # public_tweets = api.home_timeline()
        public_tweets = api_v2.get_tweets(ids='tshepi_setsiba')
        print(public_tweets)



    def test_tweets_1(self):
        # rbV_B&.nk3p#USy
        api_key='B765mW1aP58iKqMfpJhRSeUqu'
        api_key_secret='tNggaPGL9HwpyggP67E2E5mMphlMhfcLKZTHznjUuIFa1ToGk7'
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIOtfQEAAAAA%2F0G1k%2B%2B%2FEZhWMVykzWo%2F1pebLek%3DDEIuVqiOsenQl3YCbsXUnQv3NAGf3Jl3uRH5RjCrgQeU5TcbSo'

        access_token='1553104206873100288-TYav1ATS5RiKfzpl8hFiKyEakbyM4m'
        access_token_secret='KDH6b8mv96HQNHtAoIQvdguP7HePcTQM2ArAXHmqq9nQc'
        #auth = tweepy.OAuthHandler(api_key, api_key_secret)
        #auth.set_access_token(access_token, access_token_secret)
        #api = tweepy.API(auth)
        api_v2 = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret,
                               access_token=access_token, access_token_secret=access_token_secret)


        #public_tweets = api.home_timeline()
        #public_tweets = api_v2.get_home_timeline()
        tweets = api_v2.search_recent_tweets(query='happiness')
        print(tweets)

    def test_tweets_2(self):
        # rbV_B&.nk3p#USy
        api_key = 'B765mW1aP58iKqMfpJhRSeUqu'
        api_key_secret = 'tNggaPGL9HwpyggP67E2E5mMphlMhfcLKZTHznjUuIFa1ToGk7'
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIOtfQEAAAAA%2F0G1k%2B%2B%2FEZhWMVykzWo%2F1pebLek%3DDEIuVqiOsenQl3YCbsXUnQv3NAGf3Jl3uRH5RjCrgQeU5TcbSo'

        access_token = '1553104206873100288-TYav1ATS5RiKfzpl8hFiKyEakbyM4m'
        access_token_secret = 'KDH6b8mv96HQNHtAoIQvdguP7HePcTQM2ArAXHmqq9nQc'
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # api_v2 = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret,
        #                        access_token=access_token, access_token_secret=access_token_secret)


        # public_tweets = api_v2.get_home_timeline()'
        user = 'veritasium'
        limit = 100
        public_tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')
        for tweet in public_tweets:
            print(tweet.full_text)
        #tweets = api_v2.get_home_timeline()
        # print(public_tweets)


    def test_tweets_3(self):
        # rbV_B&.nk3p#USy
        api_key = 'B765mW1aP58iKqMfpJhRSeUqu'
        api_key_secret = 'tNggaPGL9HwpyggP67E2E5mMphlMhfcLKZTHznjUuIFa1ToGk7'
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIOtfQEAAAAA%2F0G1k%2B%2B%2FEZhWMVykzWo%2F1pebLek%3DDEIuVqiOsenQl3YCbsXUnQv3NAGf3Jl3uRH5RjCrgQeU5TcbSo'

        access_token = '1553104206873100288-TYav1ATS5RiKfzpl8hFiKyEakbyM4m'
        access_token_secret = 'KDH6b8mv96HQNHtAoIQvdguP7HePcTQM2ArAXHmqq9nQc'
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)


        user = 'veritasium'
        limit = 500
        results = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)
        # public_tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended').
        columns = ['User', 'Tweets']
        data = []
        i = 0
        for tweet in results:
            data.append([tweet.user.screen_name, tweet.full_text])
            # print(i, tweet.full_text)
            # i =i +1
        df = pd.DataFrame(data, columns=columns)

        print(df)

    def save_as_json(self, data):
        #
        with open('finance.json', 'w') as f:
            f.write(json.dumps(data))

        # for tweet in data:
        #     with open('finance.json', 'w') as f:
        #         f.write(json.dumps(tweet) + "\n")
                # json.dumps(data, default=vars)
                # json.dump(data, f, ensure_ascii=False)

    def get_api(self):
        """
            Twitter API Authentication Configuration
        :return: authenticated api object
        """
        api_key = 'B765mW1aP58iKqMfpJhRSeUqu'
        api_key_secret = 'tNggaPGL9HwpyggP67E2E5mMphlMhfcLKZTHznjUuIFa1ToGk7'
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIOtfQEAAAAA%2F0G1k%2B%2B%2FEZhWMVykzWo%2F1pebLek%3DDEIuVqiOsenQl3YCbsXUnQv3NAGf3Jl3uRH5RjCrgQeU5TcbSo'

        access_token = '1553104206873100288-TYav1ATS5RiKfzpl8hFiKyEakbyM4m'
        access_token_secret = 'KDH6b8mv96HQNHtAoIQvdguP7HePcTQM2ArAXHmqq9nQc'
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api

    def date_format(self, value):
        return None


    def test_duplicates_records(self):
        # Download data from Twitter using API.
        api = self.get_api()
        limit = 5000 # Number of tweets to download
        keywords = "#finance" # Filter keyword
        json_data = []
        results = tweepy.Cursor(api.search_tweets, q=keywords, count=200, tweet_mode='extended'
                                ).items(limit)

        # Data format..
        columns = ['id', 'User', 'Tweets', 'Created_at', 'geo', 'entities']
        data = []
        i = 0
        for tweet in results:
            data.append([tweet.id, tweet.user.screen_name, tweet.full_text, tweet.created_at, tweet.geo, tweet.entities])

        # self.save_as_json(json_data)

        df = pd.DataFrame(data, columns=columns)
        df.to_csv('finance_data.csv', encoding='utf-8', index=False) # Create a CSV File for data analysis
        print(df)

        # Find duplicates
        # duplicates = self.find_duplicates(df)
        #print(duplicates)




    def find_duplicates(self, df):
        return df[df.duplicated(['User', 'Tweets', 'Created_at'], keep=False)]
