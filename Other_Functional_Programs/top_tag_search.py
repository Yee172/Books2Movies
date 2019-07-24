# -*- coding: utf-8 -*-

# this file is used to find the certain tag of each book.
def search(num):
    rs = []

    for i in rs_info:
        tmp = i[1]
        if num in tmp:
            rs.append(i[0])
    return rs


def main():
    global rs_info
    rs_info = []
    with open('rs.txt','r',encoding='utf-8') as f:
        data = f.readlines()
    for each_line in data:
        each_line = each_line.split('\t')
        rs_info.append(each_line)
    with open('BTOP250.csv','r',encoding='utf-8') as f:
        info_search = f.readlines()

    for each_book in info_search:
        each_book = each_book.split(',')
        each_rs = search(each_book[0])
        str_rs = '' + each_book[0] + '\t' + each_book[2]
        for i in each_rs:
            str_rs += '\t' + i
        str_rs += '\n'
        with open('tag_top250.txt','a+',encoding='utf-8') as rs_f:
            rs_f.write(str_rs)
        print(str_rs)



main()