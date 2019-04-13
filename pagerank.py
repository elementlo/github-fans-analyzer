import pandas as pd
import csv
import networkx as nx

# If you use mac, please keep this import method to ensure the drawing method.
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def buildGraph():
    df = pd.read_csv('following_graph.csv')
    G = nx.from_pandas_edgelist(df,source='User', target='Following', edge_attr=True)
    print(nx.info(G))
    pr=nx.pagerank(G,alpha=0.85)
    
    for node, pageRankValue in pr.items():
        print(node,pageRankValue)

    list_pagerank=sorted(pr.items(),key=lambda item:item[1],reverse=True)
    df=pd.DataFrame(data=list_pagerank)
    df.to_csv('following_pagerank')
    
    print(pr)
    layout = nx.spring_layout(G)
    nx.draw(G,pos=layout, node_color='b',with_labels=True)
    plt.show()


def main():
    buildGraph()

if __name__ == '__main__':
    main()