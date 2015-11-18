import sqlite3 as lite
import networkx as nx
import simplejson as json
import oauth2 as oauth

def convertTime(timeStr):
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    return timeStr[-4:]+'-'+months.get(timeStr[4:7])+'-'+timeStr[8:10]

consumer_key='gNzYFAHNldGmNDQHL2EGwVDI7'
consumer_secret='F7ni1LTaNSXi8cr4DRix43bDuYow5v4rWDZ5imk45Xvz7SqcjH'
access_token_key='3435196294-Itqk6YQ36TPBqHKrwyaCEK2hJAX1A4IF4Qn5XrM'
access_token_secret='iocc3LEf4CmzCdnjAirkENbeFmowTabMD3KZ6GpghDxKB'
consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
token = oauth.Token(key=access_token_key, secret=access_token_secret)
client = oauth.Client(consumer, token)

#Connect to sqlite DB
directoryForDB = "./twitter.db"
con = lite.connect(directoryForDB)

with con:
	cur = con.cursor()

	selectStatement = 'SELECT n.user_id as source_id, l.source_name as source_name, l.target_id as target_id, l.target_name as target_name, n.user_created_at as user_time, l.twitter_time as twitter_time FROM nodes as n, links as l WHERE n.twitter_id = l.twitter_id'
	twitterData = cur.execute(selectStatement)
	con.commit()

	nodeDic = {}
	linkWeight = {}
	linkTime = {}
	nodeSize = {}
	targets = []
	targetList = {}

	for tweet in twitterData:
		source_id = tweet[0]
		target_id = tweet[2]
		if source_id not in nodeDic:
			nodeDic[source_id] = {'label':tweet[1], 'start': str(convertTime(tweet[4]))}
		if target_id not in nodeDic:
			targets.append(target_id);
		link = tuple([source_id, target_id])
		print ('source: ',tweet[1],' target: ',tweet[3])
		linkWeight[link] = linkWeight.get(link, 0) + 1
		if link not in linkTime:
			linkTime[link] = [str(convertTime(tweet[5]))]
		else:
			linkTime[link].append(str(convertTime(tweet[5])))
		nodeSize[source_id] = nodeSize.get(source_id, 0) + 1
		nodeSize[target_id] = nodeSize.get(target_id, 0) + 1

	length = len(targets)
	times = length/100
	jointer = ','

	for index in range(times+1):
		if(times > index):
			nameListStr = jointer.join(targets[index*100:(index+1)*100])
		else:
			nameListStr = jointer.join(targets[times*100:length+1])
		url = """https://api.twitter.com/1.1/users/lookup.json?user_id=%s""" % nameListStr
		header, fhand = client.request(url, method="GET")
		jDoc = json.loads(fhand, encoding='utf8')

		for user in jDoc:
			targetList[user['id_str']] = {'label': user['screen_name'], 'start': str(convertTime(user['created_at']))}

	for user in targetList:
		if user not in nodeDic:
			nodeDic[user] = targetList[user]
con.close()

#Initialize a new network graph object.
G = nx.Graph(mode='dynamic')
G.graph['timeformat']='date'

for node in nodeDic:
	G.add_node(node,nodeDic[node])
	G.node[node]['viz'] = {'size': nodeSize[node]}

for link in linkTime:
	if (len(linkTime[link])==1):
		G.add_edge(link[0], link[1], {'start': linkTime[link][0]})
	else:
		timeSpan=[]
		for time in linkTime[link]:
			timeSpan.append(time)
		timeSpan.sort()
		G.add_edge(link[0],link[1])
		G[link[0]][link[1]]['start']=timeSpan[0]
		G[link[0]][link[1]]['end'] = timeSpan[len(timeSpan)-1]

#Write the graph G into the gexf file.
nx.write_gexf(G, './tweets_graph_name_new.gexf', version = '1.2draft')
