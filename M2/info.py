import networkx as nx
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
    labels = []
    for each_row in range(row):
        curr_row = content[each_row].split('\t')
        labels.append(curr_row[1:])
    return labels


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

def community_maker(dismat,threshold,lables):
    # plt.figure(figsize=(8,8))
    # plt.imshow(dismat)
    # plt.show()
    #
    dismatflat = dismat.reshape((-1,))
    dismatflat = dismatflat[dismatflat != 0]  # Too many ones result in a bad histogram so we remove them
    # plt.figure(figsize=(15, 10))
    # _ = plt.hist(dismatflat, bins=200)

    mmax = np.max(dismatflat)
    mmin = np.min(dismatflat)
    mmean = np.mean(dismatflat)
    print('avg={0:.2f} min={1:.2f} max={2:.2f}'.format(mmean, mmin, mmax))

    adjmat = dismat.copy()
    np.fill_diagonal(adjmat,
                     np.min(dismat))  # Set the diagonal elements to a small value so that they won't be zeroed out
    adjmat = adjmat.reshape((-1,))
    adjmat[adjmat > threshold] = 0
    # adjmat[adjmat > 0] = 1
    print("{} out of {} values set to zero".format(len(adjmat[adjmat == 0]), len(adjmat)))
    adjmat = adjmat.reshape(dismat.shape)
    #
    G = make_graph(adjmat,labels = labels)
    print(len(G.nodes))
    plt.figure(figsize=(17, 15))
    pos = nx.spring_layout(G)
    # nx.draw(G, pos)
    # plt.show()
    #
    from networkx.algorithms.community.centrality import girvan_newman
    from networkx.algorithms.community.label_propagation import label_propagation_communities, asyn_lpa_communities


    comp = girvan_newman(G)
    max_shown = 3
    shown_count = 1
    possibilities = []
    for communities in itertools.islice(comp, max_shown):
        print("Possibility", shown_count, ": ", end='')
        print(communities)
        possibilities.append(communities)
        color_map = ["" for x in range(len(G))]
        color = 0
        for c in communities:
            indices = [i for i, x in enumerate(G.nodes) if x in c]
            for i in indices:
                color_map[i] = Config.colors[color]
            color += 1
        shown_count += 1
        plt.figure(figsize=(17, 15))
        pos = nx.spring_layout(G)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        nx.draw(G, pos, node_color=color_map, with_labels=True)
        plt.savefig('Graph2.png')
        plt.show()



# with open('C:/Users/Javier/Desktop/NUS/TOP250/venv/test_result.csv', 'r', encoding='utf-8') as f:
#     data = f.read().strip().split('\n')[1:]
#     l = list(map(lambda x: x.strip().split('\t')[1:], data))
# array = np.array(l, dtype = 'float')
# print(array)
# dismat = np.zeros((len(array),len(array)))

labels = tag_reader('topmovie_tag_zh.csv')
for i in range(len(labels)):
    labels[i] = ",".join(labels[i])
print(labels)

dismat = matrix_reader('dismat_matrix.txt')
print(dismat)

# dismat = dismat_calculator(array)
# print(dismat)

# save_matrix(dismat)

community_maker(dismat,0.033,labels)

