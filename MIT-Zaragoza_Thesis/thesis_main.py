# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 00:46:25 2018

@author: JRGene
"""

import load_network as ln
import load_orders as lo
import consolidation_optimization as co
import datetime
import time


if __name__ == "__main__":
    g , hash_nodes = ln.load_Network('HB_Hubs.txt')
    
    t, used_edges, all_cand_routes, last_arrival = lo.load_Orders('HB_Orders.txt', g, hash_nodes)
    
    rhash_nodes = {v:k for k, v in hash_nodes.items()}
    
#******************************************************************************
    
    #creates_template_schedule(g, rhash_nodes)
    
    date = datetime.datetime(2017, 5, 14, 0, 0, 0, 0) # it is a sunday
    time_window = last_arrival - date
    time_window = int(time_window.total_seconds()/(60*60*24))
    
    lo.creates_template_schedule(g, rhash_nodes, date, time_window)
    
    Sheetname = date.strftime('%d %b %Y ')
    #Sheetname = datetime.datetime.today().strftime('%d %b %Y ')
    
    reduced_schedule = lo.load_network_schedule(Sheetname, used_edges.keys(), rhash_nodes)
    
    start_opt = date + datetime.timedelta(days=1)
    
    df_cons_matrix , cons_matrix = lo.populate_cons_matrix(t,g,all_cand_routes,\
                                reduced_schedule,time_window,rhash_nodes, start_opt)
    
    #******************************************************************************
        
    # dict with the nameOrders as key and weight as value
    order_weight = {} #{Order_name: tones }
    for i in t.orders:
        order_weight[i.getName()] = i.getWeight()
    
    # updating the cost link-edge matrix
    df_costs = co.load_matrix_costs()
    
    # dict with int() as key and str OrderName as value
    names =[]
    for i in df_cons_matrix.Order: names.append(i)
    rhash_orders = {number: name for  number, name in zip(range(len(names)),names)}
    
    print('\nCalculating...\n')
    
    start_time = time.time()
    # updating the final result, it is a list of 10 tuples, where [0]'s are dataframes
    # and the [1]'s are int's
    final_result = co.brute_force_opt(t,df_cons_matrix,df_costs,order_weight,\
                                   rhash_nodes,rhash_orders)
    
    elapsed_time = time.time() - start_time
    print('Elapsed time: ', elapsed_time)
    co.print_result_txt(final_result, rhash_nodes)
