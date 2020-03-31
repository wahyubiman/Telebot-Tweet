from twitter_scraper import get_tweets
import time
from .helper import twitter, wordlist
import datetime
import logging
from configobj import ConfigObj

config = ConfigObj("setting.ini")
logger = logging.getLogger()

def get_tweet(user, page=1):
    '''get tweet data
    
    Args:
        user (str): twitter username case sensitive
        page (int): number of page to get the data, default 1
    '''
    keyword = wordlist.read()
    channel = config['main']['channel']
    tweet_list = {"username": user, "data": []}
    if len(keyword) == 0:
        logger.warning("scraper.get_tweet | please add a keyword to bot")
        pass
    for tweet in get_tweets(user, pages=page):
        for word in keyword:
            if word in tweet['text'].lower():
                if not twitter.tweet_check(tweet['tweetId']):
                    twitter.tweet_add(user, tweet['tweetId'])
                    tweet_list["data"].append(tweet)
                    logger.info(tweet['tweetId'])
                    #send_msg(update, context, tweet, user)
    return tweet_list

def start_scrape():
    '''main func for get tweet data from user
    
    Args:
        channel (str): channel username for bot to send message'''
    user_list = twitter.user_read()
    if user_list == 0:
        logger.warning("scraper.start_scrape | please add a twitter username list for scrape tweet on bot")
        pass
    return [get_tweet(user) for user in user_list]
        