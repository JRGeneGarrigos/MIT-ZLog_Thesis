# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 00:46:22 2018

@author: JRGene
"""

import openpyxl
import datetime
import pandas as pd
import math
import re
import itertools
import os

def calc_cost_route_comb(df_costs, df_block, order_weight,rhash_nodes, rhash_orders):  
    b = df_block # it is just an alias
    days, vector_cost = [], []
    for i in b: days.append(i)
    days = days[1:]
    for day in days: # going over the days
        container = {}
        for j in range(len(b['Order'])): # going over the orders
            if b[day][j] not in ['X','Wait','Transit','End']:
                if b[day][j] not in container:
                    container[b[day][j]] = order_weight[rhash_orders[j]]
                else:
                    container[b[day][j]] = container[b[day][j]] + order_weight[rhash_orders[j]]
        #calculate the container column :D
        column_cost, cost = 0, 0
        for k in container:
            linkRegex = re.compile(r'(\d{1,2})->(\d{1,2})') # limited to 2 digits
            mo = linkRegex.search(k)
            link = (rhash_nodes[int(mo.group(1))], rhash_nodes[int(mo.group(2))])
            price = df_costs[(df_costs.Origin == link[0]) & \
                     (df_costs.Destination == link[1])][day] # row filter and then select column
            for l in price: cost = int(l)
            column_cost += math.ceil(math.log(container[k],18)) * cost
        vector_cost.append(column_cost)
    return vector_cost

## this dataframe is for developing the function    
#df_blockX = pd.DataFrame({'Order':['Order 1','Order 2','Order 3'],\
#                        'Mon 15 May':['1->2','X','X'],\
#                        'Tue 16 May':['Wait','3->5','X'],\
#                        'Wed 17 May':['Wait','Wait','4->5'],\
#                        'Thu 18 May':['Wait','Wait','Wait'],\
#                        'Fri 19 May':['2->5','2->5','Wait'],\
#                        'Sat 20 May':['5->6','5->6','5->6'],\
#                        'Sun 21 May':['End','End','End']},\
#    columns = ['Order','Mon 15 May','Tue 16 May','Wed 17 May',\
#               'Thu 18 May','Fri 19 May','Sat 20 May','Sun 21 May'])

def adapt_to_df(comb_tuple, df_cons_matrix):
    matrix , vector, w = [], [], []
    for i in range(len(comb_tuple)):
        vector = ['Order ' + str(i+1)]
        for j in comb_tuple[i]:
            vector.append(j)
        matrix.append(vector)
    for i in df_cons_matrix: w.append(i)
    df_block = pd.DataFrame(matrix, columns = w)
    return df_block

## dataframe for development
#df_costsX = pd.DataFrame({'Origin':['San_Mateo','Houston','Singapore','Rotterdam','Dubai'],\
#                        'Destination':['Houston','Singapore','Tokio','Singapore','Singapore'],\
#                        'Mon 15 May':[1100,1500,1000,900,800],\
#                        'Tue 16 May':[1100,1500,1000,900,800],\
#                        'Wed 17 May':[1100,1500,1000,900,800],\
#                        'Thu 18 May':[1100,1500,1000,900,800],\
#                        'Fri 19 May':[1100,1500,1000,900,800],\
#                        'Sat 20 May':[1100,1500,1000,900,800],\
#                        'Sun 21 May':[1100,1500,1000,900,800]},\
#    columns = ['Origin','Destination','Mon 15 May','Tue 16 May','Wed 17 May',\
#               'Thu 18 May','Fri 19 May','Sat 20 May','Sun 21 May'])

#a = (['1->2', 'Wait', 'Wait', 'Wait', '2->5', '5->6', 'End'],\
#     ['X', '3->5', '5->6', 'End', 'X', 'X', 'X'],\
#     ['X', 'X', '4->5', '5->6', 'End', 'X', 'X'])

def load_matrix_costs():
    path_schedule = os.getcwd() + '\\network_schedule.xlsx'
    path_costs = os.getcwd() + '\\network_costs.xlsx'
    xls = pd.ExcelFile(path_schedule)
    Sheetname = datetime.datetime(2017, 5, 14, 0, 0, 0, 0).strftime('%d %b %Y ')
    df_one = xls.parse(Sheetname)
    
    if not os.path.exists(path_costs):
        writer = pd.ExcelWriter('network_costs.xlsx')
        df_one.to_excel(writer, sheet_name= Sheetname, index=False)
        writer.save()
    else:
        wb = openpyxl.load_workbook('network_costs.xlsx', read_only=True) # open an Excel file and return a workbook
        if Sheetname in wb.sheetnames:
            print('\nThe Template is already generated.')
        else:
            writer = pd.ExcelWriter('network_costs.xlsx')
            df_one.to_excel(writer, sheet_name = Sheetname, index=False)
            writer.save()
    answer = str()
    while answer != 'OK':
        answer = input("Introduce the costs of the routes: (write 'OK' when finish)\n")
    xls = pd.ExcelFile(path_costs)
    df_one = xls.parse(Sheetname)
    return df_one


def brute_force_opt(t,df_cons_matrix,df_costs,order_weight,rhash_nodes,rhash_orders):
    result_list, matrix_to_iter = [], []
    for i in t.routes:
        matrix_to_iter.append(t.routes[i])
    matrix_comb = list(itertools.product(*matrix_to_iter))
    for i in matrix_comb:
        df_block = adapt_to_df(i, df_cons_matrix)
        vector_cost = calc_cost_route_comb(df_costs,df_block, order_weight,\
                                           rhash_nodes,rhash_orders)
        result_list.append((df_block,sum(vector_cost)))
    result_list = sorted(result_list, key=lambda x: x[1])[:10]
    return result_list


def print_result_txt(final_result, rhash_nodes):
    summary = open('Results_Summary.txt', 'w')
    for i in range(len(final_result)):
        summary.write('Option # %s, which costs %s $:\n\n' % (i+1, final_result[i][1]))
        summary.write('%s\n\n\n' % final_result[i][0])
    summary.write('\nWhere:\n')
    for i in rhash_nodes:
        summary.write('%s = %s\n' % (i, rhash_nodes[i]))
    summary.close()
