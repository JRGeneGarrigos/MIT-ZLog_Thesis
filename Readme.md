MIT-Zaragoza Master Thesis:
===========================
(Author JRGene)

Summary:
--------

Design and deployment of a Framework that solves this problem:
Global network total cost order delivery optimization by shipment
consolidation subject to weight, shipments schedule and time window
constraints

Content:
--------
- Two folders where are all the input and output files needed to
  run the program. (.txt, .xls, .pdf) called Pilot 1 & Pilot 2.
- Six python files:
  - One interface script: Thesis_main.py. 
  - Three layers: load_network.py, load_orders.py & consolidation_optimization
  - Two structure Classes: nodes_graph.py & routes_graph.py

Classes index of the structures:
--------------------------------  

A- Nodes_graph.py
a.1- Node and SmartNode:
a.2- Edge and WeightedEdge:
a.3- Digraph and SmartDigraph:

B- Routes_Graphs.py
b.1- Order and SmartOrder:
b.2- Route:
b.3- Transport:

Function index by Layer:
------------------------

1- Load_network.py
def load_Network(Filename):
def printPath(path):
def total_LT(g, path):
def DFS(graph, start, end, path = [], shortest = [], toPrint = False):
def DFS_exception(graph, start, end, path = [], shortest = [], exception = [], toPrint = False):
def shortestPath(graph, start, end, candidates = 3):

2- Load_orders.py
def load_Orders(Filename, graph, hash_nodes):
def creates_template_schedule(graph, rhash_nodes):
def load_network_schedule(Sheetname, used_edges, rhash_nodes):
def calc_rest_leadtime(graph, rest_path):
def DFS_path_generator(t, graph, order, rest_path, vector, df, life_cycle, rhash_nodes, start_opt):
def populate_cons_matrix(t,g,all_cand_routes, reduced_schedule, life_cycle, rhash_nodes,
start_opt):

3- consolidation_optimization.py
def calc_cost_route_comb(df_costs, df_block, order_weight,rhash_nodes, rhash_orders):
def adapt_to_df(comb_tuple, df_cons_matrix):
def load_matrix_costs():
def brute_force_opt(t,df_cons_matrix,df_costs,order_weight,rhash_nodes,rhash_orders):
def print_result_txt(final_result):


Note: the code has more comments to clarify each of the steps

Installation
-------------
This has been tested with Python 3.6

Required modules include:
- numpy
- Pandas
- time
- datetime
- openpyxl
- math
- re
- itertools
- os
- string

Next steps:
----------
Relaxation of the complexity order in the optimization layer. Using Discrete
optimization methods such as Simulated annealing or Evolutionary Algorithms.