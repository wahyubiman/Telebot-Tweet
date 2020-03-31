from .database import DB_CONNECT, first_db_init, Twitter, Tweet, Wordlist
from functools import wraps, partial

class wordlist:
    '''Helper class for read/add keyword file'''
    @classmethod
    def read(self):
        '''read keyword
        
        Return:
            (list) : return list of keyword'''
        return [w.word for w in Wordlist.select()]
    
    def add(keyword):
        '''add keyword
        
        Args:
            keyword (str): keyword to add'''
        Wordlist.create(word=keyword)

    def delete(keyword):
        '''delete keyword
        
        Args:
            keyword (str): keyword to delete'''
        Wordlist.delete().where(Wordlist.word == keyword).execute()

class twitter:
    '''wrapper class for edit a Twitter and Tweet table'''
    @classmethod
    def user_read(self):
        '''read username
        
        Return:
            (list) : return list of twitter username'''
        return [t.username for t in Twitter.select()]
    
    def user_add(username):
        '''add username
        
        Args:
            username (str): username to add'''
        Twitter.create(username=username)

    def user_delete(username):
        '''delete username
        
        Args:
            username (str): username to delete'''
        Twitter.delete().where(Twitter.username == username).execute()
        
    def tweet_check(id):
        '''check tweet id
        
        Args:
            id (str): tweet id to check
        Return:
            (bool) : return True if exist '''
        return Tweet.select().where(Tweet.tweet_id == id).exists()
    
    def tweet_add(username, tweet_id):
        '''add tweet 
        
        Args:
            username (str): username to add
            tweet_id (str): tweet id to add'''
        Tweet.create(username=username, tweet_id=tweet_id)

    def tweet_delete(username):
        '''delete tweet
        
        Args:
            username (str): tweet from username to delete'''
        Tweet.delete().where(Tweet.username == username).execute()

