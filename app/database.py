from peewee import *
import datetime

db = SqliteDatabase('twitter_airdrop_bot.db')

class BaseModel(Model):
    class Meta:
        database = db

# ========================= #
# db model untuk store wordlist, twitter data
class Twitter(Model):
    '''Store twitter username'''
    username = CharField(default="username")
    
    class Meta:
        database = db
        indexes = ((("username", ), True),)

class Tweet(Model):
    '''Store tweet id'''
    username = ForeignKeyField(Twitter, backref='tweet')
    tweet_id = CharField(default="twittertweetid")
    
    class Meta:
        database = db
        indexes = ((("username", "tweet_id"), True),)

class Wordlist(Model):
    '''store tweet id'''
    word = CharField(default="word")
    
    class Meta:
        database = db
        indexes = ((("word", ), True),)

class Tele(Model):
    channel = CharField(default="channel")
# ========================= #

DB_CONNECT = db.connect()
DB_CLOSE = db.close()

def first_db_init():
    """first time db init"""
    db.create_tables([Tweet, Twitter, Wordlist])



