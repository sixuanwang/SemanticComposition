# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
from priodict import priorityDictionary

NOT_CONNECTED = 999

def Dijkstra(graph,start,end=None):
	

	final_distances = {}	# dictionary of final distances
	predecessors = {}	# dictionary of predecessors
	estimated_distances = priorityDictionary()   # est.dist. of non-final vert.
	estimated_distances[start] = 0

	for vertex in estimated_distances:
		final_distances[vertex] = estimated_distances[vertex]
		if vertex == end: break

		for edge in graph[vertex]:
			path_distance = final_distances[vertex] + graph[vertex][edge]
			if edge in final_distances:
				if path_distance < final_distances[edge]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif edge not in estimated_distances or path_distance < estimated_distances[edge]:
				estimated_distances[edge] = path_distance
				predecessors[edge] = vertex

	return (final_distances,predecessors)

	
def shortestPath(graph,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	final_distances,predecessors = Dijkstra(graph,start,end)
	path = []
	cost = 0.0
	
	try: 
		cost = final_distances[end]
	except Exception, e:
		cost = NOT_CONNECTED 
		
	while 1:
		path.append(end)
		if end == start: break
		end = predecessors[end]
	path.reverse()
	
	return path, cost
	
def shortestPathCost(graph,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	final_distances,predecessors = Dijkstra(graph,start,end)
	cost = 0.0
	try: 
		cost = final_distances[end]
	except Exception, e:
		cost = NOT_CONNECTED 
	
	return cost
	
	
import sys

#print graph
def printGraph(graph, outputf):
	for (vertex, edges) in graph.items():
		outputf.write("%s:" %vertex + " {")
		for (k,v) in edges.items():
			outputf.write(" %s:" %k + "%3.8f" %v + ", ")
		outputf.write("}\n")
		
#print graph
def printGraphRound(graph, outputf):
	for (vertex, edges) in graph.items():
		outputf.write("%s:" %vertex + " {")
		for (k,v) in edges.items():
			outputf.write(" %s:" %k + "%d" %(round(1.0/v)) + ", ")
		outputf.write("}\n")

'''
graph = { 
  's': {'u' : 10, 'x' : 5}, 
  'u': {'v' : 1, 'x' : 2}, 
  'v': {'y' : 4}, 
  'x': {'u' : 3, 'v' : 9, 'y' : 2}, 
  'y': {'s' : 7, 'v' : 6}
}

graph3 = { 
  'a': {'b' : 1, 'c' : 1}, 
  'b': {'d' : 1},
  'd': {'c' : 1},
  'c': {'b' : 1}
}

graph2 = {
	'a': {'w': 14, 'x': 7, 'y': 9},
    'b': {'w': 9, 'z': 6},
    'w': {'a': 14, 'b': 9, 'y': 2},
    'x': {'a': 7, 'y': 10, 'z': 15},
    'y': {'a': 9, 'w': 2, 'x': 10, 'z': 11},
    'z': {'b': 6, 'x': 15, 'y': 11},    
} 

#test graph
#print "\nGraph"

def shortestPath(graph,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	final_distances,predecessors = Dijkstra(graph,start,end)
	path = []
	while 1:
		path.append(end)
		if end == start: break
		end = predecessors[end]
	path.reverse()
	return path



#for (k,v) in predecessors.items():
#	print " '%s': " % k, v, ""
	
#for (k2,v2) in final_distances.items():
#	print " '%s': " % k2, v2, ""
	
#path = []
#path = shortestPath(graph2, 'b', 'c')
#print path

printGraph(graph2)
outputf.close()		
'''