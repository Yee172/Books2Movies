# -*- coding:utf-8 -*-

'''
author:     CalmCat
date:       2019.7.16
function:   Markov Chain Algorithm
'''

import numpy as np


def MarkovChain(d_matrix, power=2, inflation=2, numIter=1):

    row, column = np.size(d_matrix, 0), np.size(d_matrix, 1)
    for (i, j) in zip(range(row), range(column)):
        d_matrix[i][j] = 1
    d_matrix = d_matrix/d_matrix.mean(0)
    tmp_matrix = d_matrix
    tar_matrix = np.random.rand(row, column)
    #print(d_matrix)
    # while ((tar_matrix != tmp_matrix).all()):
    for num_i in range(numIter):
        tar_matrix = tmp_matrix
        base_matrix = tmp_matrix
        for i in range(power):
            tmp_matrix = np.matmul(tmp_matrix, base_matrix)
            # print(tmp_matrix)
            # input
        tmp_base_matrix = tmp_matrix
        for i in range(inflation - 1):
            tmp_matrix = tmp_matrix * tmp_base_matrix
            # print(tmp_matrix)

            # input('上面是inflate结果')
        tmp_matrix = tmp_matrix / tmp_matrix.mean(0)
        # print(tmp_matrix)
    tmp_matrix = tmp_matrix / tmp_matrix.max()
    return tmp_matrix

if __name__ == '__main__':
    tmp_mat = np.array([[1,2,3],[1,4,5],[1,8,9]])
    rs_mat = MarkovChain(tmp_mat)
    print(rs_mat)