# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 13:04:02 2017

@author: JRGene
"""

class Node(object):
    def __init__(self, name):
        """Assumes name is a string"""
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
 
    
class SmartNode(Node):

    def __hash__(self):
        return int(self.name)


class Edge(object):
    def __init__(self, src, dest):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        #return self.src.getName() + '->' + self.dest.getName()
        return '%s->%s' % (str(self.src), str(self.dest))


class WeightedEdge(Edge):
    def __init__(self, src, dest, LeadTime):
        super(WeightedEdge, self).__init__(src, dest)
        self.LeadTime = LeadTime
    def getLeadTime(self):
        return self.LeadTime

               
class Digraph(object):
    """edges is a dict mapping each node to a list of
    its children"""
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node) # Adds a node to set of nodes
            #self.edges.update({node:[]})
            self.edges[node] = [] # Creates a new key Node with an empty list as value
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def getNode(self, name): # if you want to enter by name
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)
    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                #result = '%s%s->%s\n' % (result, str(src), str(dest))
                result = result + src.getName() + '->'\
                         + dest.getName() + '\n'
        return result[:-1] #omit final newline


class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)
  
      
class SmartDigraph(Digraph):

    def addEdge(self, weightededge):
        src = weightededge.getSource()
        dest = weightededge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(weightededge)
    def getEdgeDestination(self, src,dest):
        for edge in self.edges[src]:
            if hash(edge.getDestination()) == hash(dest):
                return edge
    def getEdgeLT(self,scr,dest):
        return self.getEdgeDestination(scr,dest).getLeadTime()


def buildNetworkGraph(GraphType):
    g = GraphType()
    for name in ('Houston', 'Rotterdam', 'Dubai', 'Singapore'): #Create 4 CD
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Houston'), g.getNode('Rotterdam')))
    g.addEdge(Edge(g.getNode('Rotterdam'), g.getNode('Houston')))
    g.addEdge(Edge(g.getNode('Houston'), g.getNode('Dubai')))
    g.addEdge(Edge(g.getNode('Dubai'), g.getNode('Houston')))
    g.addEdge(Edge(g.getNode('Houston'), g.getNode('Singapore')))
    g.addEdge(Edge(g.getNode('Singapore'), g.getNode('Houston')))
    g.addEdge(Edge(g.getNode('Rotterdam'), g.getNode('Dubai')))
    g.addEdge(Edge(g.getNode('Dubai'), g.getNode('Rotterdam')))
    g.addEdge(Edge(g.getNode('Rotterdam'), g.getNode('Singapore')))
    g.addEdge(Edge(g.getNode('Singapore'), g.getNode('Rotterdam')))
    g.addEdge(Edge(g.getNode('Dubai'), g.getNode('Singapore')))
    g.addEdge(Edge(g.getNode('Singapore'), g.getNode('Dubai')))
    return g

#g = buildNetworkGraph(Digraph)
#print(g)