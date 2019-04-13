import pandas as pd
import csv
import networkx as nx

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def buildGraph():
    df = pd.read_csv('following.csv')
    G = nx.from_pandas_edgelist(df,source='User', target='Following', edge_attr=True)
    print(nx.info(G))
    # nx.draw(G,with_labels=True)
    # plt.show()
    pr=nx.pagerank(G,alpha=0.85)
    
    print(pr)
    layout = nx.spring_layout(G)
    nx.draw(G,pos=layout, node_color='b',with_labels=True)
    plt.show()

def main():
    buildGraph()

if __name__ == '__main__':
    main()