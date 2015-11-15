import oauth2 as oauth
import sqlite3 as lite
import simplejson as json
import urllib
import re
import os

# Go to https://apps.twitter.com/ to setup a project
consumer_key='gNzYFAHNldGmNDQHL2EGwVDI7'
consumer_secret='F7ni1LTaNSXi8cr4DRix43bDuYow5v4rWDZ5imk45Xvz7SqcjH'
access_token_key='3435196294-Itqk6YQ36TPBqHKrwyaCEK2hJAX1A4IF4Qn5XrM'
access_token_secret='iocc3LEf4CmzCdnjAirkENbeFmowTabMD3KZ6GpghDxKB'
consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
token = oauth.Token(key=access_token_key, secret=access_token_secret)
client = oauth.Client(consumer, token)
q = "NBA" # what you are querying
#lat = "29.750833" # latitude @Toyota Center
#lng = "-95.362222" # longitude @Toyota Center
#r = "100" # radius 
# url = """https://api.twitter.com/1.1/search/tweets.json?q=%s&include_entities=true&result_type=recent&geocode=%s,%s,%smi""" % (q,lat,lng,r)
url = """https://api.twitter.com/1.1/search/tweets.json?q=%s&lang=en&result_type=recent&count=200""" % q
header, fhand = client.request(url, method="GET")
jDoc = json.loads(fhand, encoding='utf8')
## Set directory to YOUR computer and folder
directoryForDB = "./"
if not os.path.exists(directoryForDB):  # create a new one if it is not exist 
	os.makedirs(directoryForDB)

directoryForDB = directoryForDB + "twitter.db"
## If database does not exist, creates items
## If database does exist, opens it
con = lite.connect(directoryForDB)
### open a connection to store the data
with con:
	cur = con.cursor()
	# check for the tables it exists it will drope it and create a new one 
	cur.execute("DROP TABLE IF EXISTS nodes") 
	#Create a table named "ratings", movieName as the primary key, years , ratings and votes 
	cur.execute("CREATE TABLE nodes(twitter_id TEXT, user_id TEXT, screen_name TEXT, created_at TEXT, twitter_text TEXT)")
	for tweet in jDoc['statuses']:
		insertStatement = 'INSERT INTO nodes VALUES(?, ?, ?, ?, ?)'
		parms = (tweet['id_str'], tweet['user']['id_str'], tweet['user']['screen_name'], tweet['created_at'], tweet['text'])
		cur.execute(insertStatement, parms)
		print "Inserting: ", tweet['text']
	con.commit()
