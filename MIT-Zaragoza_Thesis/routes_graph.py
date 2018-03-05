# -*- coding: utf-8 -*-
"""
Created on Sun May  7 12:32:28 2017

@author: JRGene
"""


class Order(object):
#    nextIdNum = 1
    def __init__(self, id_order, node_src, node_dest, date_start, date_end,weight, name):
        """Assuming first line input first order"""
        self.id_order = id_order
#        self.idNum = Order.nextIdNum
#        self.name = 'Order ' + str(Order.nextIdNum)
        self.name = name
        self.src = node_src
        self.dest = node_dest
        self.DS = date_start
        self.DE = date_end
        self.weight = weight
#        Order.nextIdNum += 1
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def getDateStart(self):
        return self.DS
    def getDateEnd(self):
        return self.DE
    def getName(self):
        return self.name
#    def getIdNum(self):
#        return self.idNum
    def getWeight(self):
        return self.weight
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    
class SmartOrder(Order):
    def __hash__(self):
        return int(self.id_order)


class Route(object):
    def __init__(self, src, dest, route = []):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
        self.route = route # list with time_window lenght
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
#    def getTimeWindow(self):
#        return self.tw
    def __str__(self):
        #return self.src.getName() + '->' + self.dest.getName()
        return '%s->%s' % (str(self.src), str(self.dest))
               
    
class Transport(object):
    """edges is a dict mapping each node to a list of
    its children"""
    def __init__(self):
        self.orders = []
        self.routes = {}
    def addOrder(self, order):
        if order in self.orders:
            raise ValueError('Duplicate order')
        else:
            self.orders.append(order) # Adds a node to set of nodes
            #self.edges.update({node:[]})
            self.routes[order] = [] # Creates a new key Node with an empty list as value
    def addRoute(self, order, route):
        self.routes[order].append(route)
    def childrenOf(self, order):
        return self.routes[order]
    def hasOrder(self, order):
        return order in self.orders
    def getOrder(self, src, dest, date_end): # if you want to enter by name
        for n in self.oders:
            if n.getSource() == src and n.getDestination == dest \
                        and n.getDateEnd == date_end:
                return n
        raise NameError()
    def __str__(self):
        result = ''
        for i in self.routes:
            for j in self.routes[i]:
                #result = '%s%s->%s\n' % (result, str(src), str(dest))
                result = result + i.getSource() + '->'\
                         + i.getDestination() + ': ' + str(j) + '\n'
        return result[:-1] #omit final newline

