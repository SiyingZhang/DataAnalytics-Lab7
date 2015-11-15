import gexf
import sqlite3 as lite
import networkx as nx

def graph_add_node(node, graph, t):
    if graph.has_node(node):
        graph.node[node]['weight']+=1
    else:
        graph.add_node(node)
        graph.node[node]['label'] = node
        graph.node[node]['weight'] = 1
        graph.node[node]['type'] = t #source node or target node
 
#Add a edge between node1 and node2 
def graph_add_edge(n1, n2, graph):
    if graph.has_edge(n1, n2):
        graph[n1][n2]['weight']+=1
    else:
        graph.add_edge(n1,n2)
        graph[n1][n2]['weight']=1

#Initialize a new network graph object.
G = nx.Graph()

#Connect to sqlite DB
directoryForDB = "./twitter.db"
con = lite.connect(directoryForDB)

with con:
	cur = con.cursor()

	#Create a new table storing the connections between source users and target users.
	cur.execute("DROP TABLE IF EXISTS connected")
	cur.execute("CREATE TABLE connected(source_user_id TEXT, source_user_name TEXT, created_at TEXT, target_user_id TEXT, target_user_name TEXT)")

	insertToConnected = 'INSERT INTO connected SELECT nodes.user_id as user1, nodes.screen_name as name1, nodes.created_at, links.user_id as user2, links.screen_name_target as name2 FROM nodes INNER JOIN links ON nodes.twitter_id = links.twitter_id'
	cur.execute(insertToConnected)

	#Select all data in the connected table to do the following parsing operations
	selectConnectedData = 'SELECT * FROM connected'
	for row in cur.execute(selectConnectedData):
		#graph_add_node(row['source_user_name'], G, "source")
		#graph_add_node(row['target_user_name'], G, "target")
		#graph_add_edge(row['source_user_name'], row['target_user_name'], G)
		
		#Add source users to nodes
		G.add_node(int(row[0]), label = row[1])
		#Add target users to nodes
		G.add_node(int(row[3]), label = row[4])

		#Add the edge between source&target users.
		G.add_edge(int(row[0]), row[3])

		#print row

#Write the graph G into the gexf file.
nx.write_gexf(G, './tweets_graph.gexf', encoding = 'utf-8')





