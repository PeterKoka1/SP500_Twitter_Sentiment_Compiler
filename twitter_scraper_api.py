import re
import datetime
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class SPX_Twitter_Scraper(object):


    def __init__(self):

        consumer_key = 'YOUR_CONSUMER_KEY'
        consumer_secret = 'YOUR_CONSUMER_SECRET'
        access_token = 'YOUR_ACCESS_TOKEN'
        access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

        try:
            self.auth = OAuthHandler(
                consumer_key,
                consumer_secret
                )
            self.auth.set_access_token(
                access_token,
                access_token_secret
                )
            self.api = tweepy.API(
                self.auth,
                wait_on_rate_limit=True
                )
        except:
            print("Error: Authentication Failed")


    def clean_tweet(self, tweet):
        parsed_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet).split())
        parsed_tweet = parsed_tweet.replace("RT ", "")
        return parsed_tweet


    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1


    def get_tweets(self, _SYMBOL_, count):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=_SYMBOL_, count=count)
            for tweet in fetched_tweets:
                if (datetime.datetime.now() - tweet.created_at).days == 0:
                    parsed_tweet = {}
                    parsed_tweet['text'] = self.clean_tweet(tweet.text)
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                    if tweet.retweet_count > 0:
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


    def return_percentages(self, stock):
        tweets = self.get_tweets(_SYMBOL_=stock, count=2)
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 1]
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == -1]
        ntrtweets = [tweet for tweet in tweets if tweet['sentiment'] == 0]

        return 0 if len(tweets) == 0 else [len(ptweets), len(ntweets), len(ntrtweets)]
