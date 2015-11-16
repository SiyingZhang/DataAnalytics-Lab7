import sqlite3 as lite
import networkx as nx

#Connect to sqlite DB
directoryForDB = "./twitter.db"
con = lite.connect(directoryForDB)

with con:
	cur = con.cursor()

	#Create a new table storing the connections between source users and target users.
	#cur.execute("DROP TABLE IF EXISTS connected")
	#cur.execute("CREATE TABLE connected(source_user_id TEXT, source_user_name TEXT, created_at TEXT, target_user_id TEXT, target_user_name TEXT)")

	#insertToConnected = 'INSERT INTO connected SELECT nodes.user_id as user1, nodes.screen_name as name1, nodes.created_at, links.user_id as user2, links.screen_name_target as name2 FROM nodes INNER JOIN links ON nodes.twitter_id = links.twitter_id'
	#cur.execute(insertToConnected)

	selectStatement = 'SELECT nodes.user_id as source_id, nodes.screen_name as source_name, links.user_id as target_id, links.screen_name_target as target_name, nodes.created_at as created_at FROM nodes, links WHERE nodes.twitter_id = links.twitter_id'
	twitterData = cur.execute(selectStatement)
	con.commit()

	nodeDic = {}
	linkDic = {}
	nodeSize = {}

	for tweet in twitterData:
		source_name = tweet[1]
		target_name = tweet[3]
		if source_name not in nodeDic:
			nodeDic[source_name] = {'label':source_name}
		if target_name not in nodeDic:
			nodeDic[target_name] = {'lable':target_name}
		link = tuple([source_name, target_name])
		print ('source: ',source_name,' target: ',target_name)
		linkDic[link] = linkDic.get(link, 0) + 1
		nodeSize[source_name] = nodeSize.get(source_name, 0) + 1
		nodeSize[target_name] = nodeSize.get(target_name, 0) + 1

con.close()

#Initialize a new network graph object.
G = nx.Graph()

for node in nodeDic:
	G.add_node(node,nodeDic[node])
	G.node[node]['viz'] = {'size': nodeSize[node]}

for link in linkDic:
	G.add_edge(link[0], link[1], {'weight': linkDic[link]})

#Write the graph G into the gexf file.
nx.write_gexf(G, './tweets_graph_name.gexf', version = '1.2draft')





