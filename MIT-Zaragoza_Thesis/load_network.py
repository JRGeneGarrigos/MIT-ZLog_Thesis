# -*- coding: utf-8 -*-
"""
Created on Fri May  5 18:18:15 2017

@author: JRGene
"""
 
from nodes_graph import WeightedEdge, SmartDigraph, SmartNode


def load_Network(Filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        mapFilename : name of the map file

    Assumes:
        One line per each edge-entry in the map file consists of two strings 
        (origin and destiny) and one (integer leadtime), all separated by a 
        blank space:
            From To TotalLeadtime
        e.g.
            Houston Rotterdam 23
            Rotterdam Singapore 30
        This entry would become an edge from Houston to Rotterdam.

    Returns:
        a directed weighted graph representing the Network
    """
    print("Loading Network map from file ", Filename)
    g = SmartDigraph()
    hash_table = {}
    counter = 1
    
    lines = open(Filename, 'r').readlines()
    
    for i in lines:
        for j in range(2):
            line = i.split()
            if line[j] not in hash_table:
                hash_table[line[j]] = counter
                counter += 1
                
    for i in hash_table:
        g.addNode(SmartNode(hash_table[i]))
                      
    for i in lines:
        line = i.split()
        start_node = g.getNode(str(hash_table[line[0]]))
        end_node = g.getNode(str(hash_table[line[1]]))
        lead_time = int(line[2])

        edge = WeightedEdge(start_node, end_node,lead_time) # creates the edge
        g.addEdge(edge) # adds the edge to the smartdigrahp

    return g, hash_table

def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result

def total_LT(g, path):
    suma = 0
    for i in range(len(path)-1):
        suma += g.getEdgeLT(path[i],path[i+1])
    return suma

def DFS(graph, start, end, path = [], shortest = [], toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start] # adds the node
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for edge in graph.childrenOf(start):
        if edge.getDestination() not in path: #avoid cycles
            if shortest == [] or total_LT(graph, path) < total_LT(graph, shortest): # prunes if bigger than the current candidate
                newPath = DFS(graph, edge.getDestination(), end, path, shortest, toPrint)
                if newPath != []:
                    shortest = newPath
        elif toPrint:
            print('Already visited', edge.getDestination())
    return shortest


def DFS_exception(graph, start, end, path = [], shortest = [], exception = [], toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start] # adds the node
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for edge in graph.childrenOf(start):
        if edge.getDestination() not in path: #avoid cycles
            if shortest == [] or total_LT(graph, path) < total_LT(graph, shortest): # prunes if bigger than the current candidate
                newPath = DFS_exception(graph, edge.getDestination(), end, path, shortest,exception, toPrint)
                if newPath != [] and newPath not in exception:
                    shortest = newPath
        elif toPrint:
            print('Already visited', edge.getDestination())
    return shortest
    
def shortestPath(graph, start, end, candidates = 3):
    container, exception = [], []
    while len(container) < candidates:
        container.append(DFS_exception(graph, start, end, [], [], exception))
        exception = container
    return container
