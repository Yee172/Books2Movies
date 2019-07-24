import networkx as nx
import community
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
# import PIL.ImageOps
# from PIL import Image
import numpy as np
import itertools
import math
import sys
import os
from scipy.spatial.distance import squareform

class Config():
    colors = ['aquamarine', 'bisque', 'blanchedalmond', 'blueviolet', 'brown',
              'burlywood', 'cadetblue', 'chartreuse','chocolate', 'coral',
              'cornflowerblue', 'cornsilk', 'crimson', 'darkblue', 'darkcyan',
              'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
              'darkmagenta', 'darkolivegreen', 'darkorange', 'darkslateblue',
              'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
              'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet',
              'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue',
              'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
              'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow',
              'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory']

def dismat_calculator(array):
    print("Calculating...")
    for i in range(len(array)):
        vector1 = np.array(array[i])
        for j in range(i+1,len(array)):
            vector2 = np.array(array[j])
            vector3 = []
            for z in range(len(vector1)):
                vector3.append(min(vector1[z],vector2[z]))
            dist = 1 - np.linalg.norm(vector3)/(np.linalg.norm(vector1) * np.linalg.norm(vector2))**0.5
            dismat[i][j] = dist
            dismat[j][i] = dist
    print("Calculation done")
    print(dismat)
    return dismat

def matrix_reader(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.readlines()
    row = len(content)
    column = len(content[0].split(' '))
    tar_np = np.zeros((row, column))
    for each_row in range(row):
        curr_row = content[each_row].split(' ')
        for each_column in range(column):
            tar_np[each_row][each_column] = float(curr_row[each_column])
    return tar_np

def tag_reader(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')
    row = len(content)
    column = len(content[0].split(' '))
    tags = []
    for each_row in range(row):
        curr_row = content[each_row].split('\t')
        tags.append(curr_row[1:])
    for i in range(len(tags)):
        tags[i] = ",".join(tags[i])
        tags[i] = str(i) +": " + tags[i]
    return tags


def make_graph(sim, labels=None):
    G = nx.Graph()
    for (i, j) in [(i, j) for i in range(sim.shape[0]) for j in range(sim.shape[1]) if i != j and sim[i,j] != 0]:
        if labels == None:
            G.add_edge(i, j, weight=sim[i,j])
        else:
            G.add_edge(labels[i], labels[j], weight=sim[i,j])
    return G

def save_matrix(dismat):
    with open('dismat_matrix.txt', 'w', encoding='utf-8') as f:
        write_content = ''
        row = len(dismat)
        for i in range(row):
            eachline = ''
            column = len(dismat[0])
            for j in range(len(dismat[0])):
                eachline += str(dismat[i][j])
                if j != len(dismat[0])-1: eachline += ' '
            write_content += eachline
            if i != row-1 : write_content += '\n'
        f.write(write_content)

def normalize(dismat):# normalize the dismat so that every element is evenly spread between 0 and 1
    dismatflat = dismat.reshape((-1,))
    mmax = np.max(dismatflat)
    mmin = np.min(dismatflat)
    for i in range(len(dismat)):
        for j in range(len(dismat)):
            dismat[i][j] = (dismat[i][j] - mmin) / (mmax - mmin)
    print(dismat)

    return dismat

def analysis(dismat):
    dismatflat = dismat.reshape((-1,))
    dismatflat = dismatflat[dismatflat != 0]  # Too many ones result in a bad histogram so we remove them
    plt.figure(figsize=(15, 10))
    _ = plt.hist(dismatflat, bins=200)
    plt.show()
    mmax = np.max(dismatflat)
    mmin = np.min(dismatflat)
    mmean = np.mean(dismatflat)
    mstd = np.std(dismatflat)
    print('avg={0:.2f} min={1:.2f} max={2:.2f} mstd={3:.2f}'.format(mmean, mmin, mmax, mstd))

def sim_community_maker(dismat,threshold,tags=None):
    adjmat = dismat.copy()
    np.fill_diagonal(adjmat,
                     np.min(dismat))  # Set the diagonal elements to a small value so that they won't be zeroed out
    adjmat = adjmat.reshape((-1,))
    adjmat[adjmat > threshold] = 0
    adjmat = adjmat.reshape(dismat.shape)

    G = make_graph(adjmat,labels=tags)
    partition = community.best_partition(G,random_state=600)
    F = community.modularity(partition, G)
    return(F)

def sim_community_maker1(dismat,threshold,tags=None):
    adjmat = dismat.copy()
    np.fill_diagonal(adjmat,
                     np.min(dismat))  # Set the diagonal elements to a small value so that they won't be zeroed out
    adjmat = adjmat.reshape((-1,))
    adjmat[adjmat > threshold] = 0
    adjmat = adjmat.reshape(dismat.shape)

    G = make_graph(adjmat,labels=tags)
    partition = partition_calculate(G)
    F = community.modularity(partition, G)
    return(F)

def sim_community_maker2(dismat,threshold,tags=None):
    adjmat = dismat.copy()
    np.fill_diagonal(adjmat,
                     np.min(dismat))  # Set the diagonal elements to a small value so that they won't be zeroed out
    adjmat = adjmat.reshape((-1,))
    adjmat[adjmat > threshold] = 0
    adjmat = adjmat.reshape(dismat.shape)

    G = make_graph(adjmat,labels=tags)
    partition = partition_calculate1(G)
    F = community.modularity(partition, G)
    return(F)

def partition_calculate(G):

    from networkx.algorithms.community.centrality import girvan_newman
    from networkx.algorithms.community import k_clique_communities
    from networkx.algorithms.community.modularity_max import greedy_modularity_communities
    from networkx.algorithms.community.modularity_max import _naive_greedy_modularity_communities

    comp = list(greedy_modularity_communities(G))
    partition = dict()
    for j in range(len(comp)):
        communities = comp[j]
        for x in communities:
            partition[x] = j
    return partition

def partition_calculate1(G):

    from networkx.algorithms.community.centrality import girvan_newman
    from networkx.algorithms.community import k_clique_communities
    from networkx.algorithms.community.modularity_max import greedy_modularity_communities
    from networkx.algorithms.community.modularity_max import _naive_greedy_modularity_communities

    comp = list(girvan_newman(G))
    partition = dict()

    communities = itertools.islice(comp, 1)
    c = list(communities)
    c = c[0]
    for i in range(len(c)):
        t = c[i]
        for x in t:
            partition[x] = i
    return partition

def Louvain(dismat, threshold, tags=None):
    adjmat = dismat.copy()
    np.fill_diagonal(adjmat,
                     np.min(dismat))  # Set the diagonal elements to a small value so that they won't be zeroed out
    adjmat = adjmat.reshape((-1,))
    adjmat[adjmat > threshold] = 0
    # adjmat[adjmat > 0] = 1
    print("{} out of {} values set to zero".format(len(adjmat[adjmat == 0]), len(adjmat)))
    adjmat = adjmat.reshape(dismat.shape)
    #
    G = make_graph(adjmat, labels=tags)
    print(len(G.nodes))

    partition = community.best_partition(G,random_state=600)

    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    comp = []
    for com in set(partition.values()):
        count += 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        comp.append(list_nodes)


    color_map = ['white' for x in range(len(G))]
    color = 0
    shown_count = 1
    print("Community Numbers: ", len(comp))
    for j in range(len(comp)):
        communities = comp[j]
        print("Community", shown_count, ": ", end='')
        print(communities)
        print("Length of every Community: ", len(communities))
        indices = [i for i, x in enumerate(G.nodes) if x in communities]
        for i in indices:
            color_map[i] = Config.colors[color]
        color += 1
        shown_count += 1

    plt.figure(figsize=(17, 15))
    pos = nx.spring_layout(G)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    nx.draw(G, pos, node_color=color_map, with_labels=True)
    plt.savefig('Graph.png')
    plt.show()
    # print(G.edges)

def community_maker(dismat,threshold,tags=None):
    adjmat = dismat.copy()
    np.fill_diagonal(adjmat,
                     np.min(dismat))  # Set the diagonal elements to a small value so that they won't be zeroed out
    adjmat = adjmat.reshape((-1,))
    adjmat[adjmat > threshold] = 0
    # adjmat[adjmat > 0] = 1
    print("{} out of {} values set to zero".format(len(adjmat[adjmat == 0]), len(adjmat)))
    adjmat = adjmat.reshape(dismat.shape)
    #
    G = make_graph(adjmat,labels=tags)
    print(len(G.nodes))

    from networkx.algorithms.community.centrality import girvan_newman
    from networkx.algorithms.community import k_clique_communities
    from networkx.algorithms.community.modularity_max import greedy_modularity_communities
    from networkx.algorithms.community.modularity_max import _naive_greedy_modularity_communities

    comp = list(greedy_modularity_communities(G))
    print(len(comp))
    shown_count = 1
    possibilities = []
    color_map = ['white' for x in range(len(G))]
    color = 0
    partition = dict()
    for j in range(len(comp)):
        communities = comp[j]
        print("Possibility", shown_count, ": ", end='')
        for x in communities:
            partition[x] = j
        print(communities)
        print(len(communities))
        possibilities.append(communities)
        indices = [i for i, x in enumerate(G.nodes) if x in communities]
        for i in indices:
            color_map[i] = Config.colors[color]
        color += 1
    F = community.modularity(partition, G)
    print(F)
    shown_count += 1
    plt.figure(figsize=(17, 15))
    pos = nx.spring_layout(G)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    print(color_map)
    nx.draw(G, pos, node_color=color_map, with_labels=True)
    plt.savefig('Graph.png')
    plt.show()

def data_reader(filename,num):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')[1:]
        l = list(map(lambda x: x.strip().split('\t')[1:], data))[:num]
    array = np.array(l, dtype = 'float')
    return array

def threshold_helper(dismat,num1,num2):
    plot1 = []
    plot2 = []
    plot3 = []
    x = []
    x1 = []
    for i in range(num1, num2):
        plot1.append(sim_community_maker(dismat, i / 1000, tags))
        plot2.append(sim_community_maker1(dismat, i / 1000, tags))
        plot3.append(sim_community_maker2(dismat, i / 1000, tags))
        x.append(i / 1000)
    print(plot1)
    plot1 = np.array(plot1)
    plot2 = np.array(plot2)
    plot3 = np.array(plot3)
    plt.figure(figsize=(15, 10))
    plt.plot(x, plot1,linewidth = 2,label='Louvain')
    plt.plot(x, plot2,linewidth = 2,label='Greedy_modularity_communities')
    plt.plot(x, plot3,linewidth = 2,label='Girvan_Newman')
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 23,
             }
    plt.legend(prop = font1)  # 显示图例
    plt.xlabel('Threshold',size = 30)
    plt.ylabel('Modularity',size = 30)
    plt.show()

num = 125
array = data_reader('Graph2_data.csv',num)

dismat = np.zeros((len(array),len(array)))

tags = tag_reader('Movie&Clustet_tag.csv')
# tags = []
# for i in range(len(array)):
#     tags.append(i)
# print(tags)

# dismat = matrix_reader('dismat_matrix.txt')
# print(dismat)

dismat = dismat_calculator(array)
print(dismat)
dismat = normalize(dismat)
analysis(dismat)
# save_matrix(dismat)

# threshold_helper(dismat,50,150)
# community_maker(dismat,0.043)
Louvain(dismat,0.125,tags)