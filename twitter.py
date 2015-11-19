import oauth2 as oauth
import sqlite3 as lite
import simplejson as json
import urllib
import os

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
url = """https://api.twitter.com/1.1/search/tweets.json?q=%s&lang=en&include_entities=true&result_type=recent&count=500""" % q
header, fhand = client.request(url, method="GET")
jDoc = json.loads(fhand, encoding='utf8')

# Set directory to YOUR computer and folder
directoryForDB = "./"
if not os.path.exists(directoryForDB):  # create a new one if it is not exist 
	os.makedirs(directoryForDB)

directoryForDB = directoryForDB + "twitter.db"
con = lite.connect(directoryForDB)
### open a connection to store the data
with con:
	cur = con.cursor()
	# cur.execute("DROP TABLE IF EXISTS nodes") 
	# cur.execute("DROP TABLE IF EXISTS links") 
	# cur.execute("CREATE TABLE nodes(twitter_id TEXT, user_id TEXT, user_created_at TEXT, twitter_text TEXT)")
	# cur.execute("CREATE TABLE links(twitter_id TEXT, twitter_time TEXT, source_id TEXT, source_name TEXT, target_id TEXT, target_name TEXT)")
	count = 0	#Count the number of inserted tweets.
	for tweet in jDoc['statuses']:
		insertStatement = 'INSERT INTO nodes VALUES(?, ?, ?, ?)'
		parms = (tweet['id_str'], tweet['user']['id_str'], tweet['user']['created_at'], tweet['text'])
		cur.execute(insertStatement, parms)
		count = count + 1
		print "\nInserting tweets: ", tweet['text'].replace("\n"," ")
		
		#Insert the mentioned users(target users) into the links table.
		targets = tweet['entities']['user_mentions']
		for target in targets:
			insertStatement = 'INSERT INTO links VALUES(?, ?, ?, ?, ?, ?)'
			parms = (tweet['id_str'], tweet['created_at'], tweet['user']['id_str'], tweet['user']['screen_name'], target['id_str'],target['screen_name'])
			cur.execute(insertStatement, parms)
			print " *Inserting link(s) from %s to %s." % (tweet['user']['screen_name'], target['screen_name'])
	print "Inserting count: ", count
	con.commit()
con.close()

