import sys
import io
import requests
import re
import json
import codecs
import time
import random
'''
这个程序用来爬取每本书评论的相关信息。
要用到BTOP250开头的相关文件

记住当爬虫无法爬取时，爬到的文件编号，过一会从这个文件开始爬。
我默认从文件r0开始爬，每个人开始地方不一样，分别从0，100，200开始爬
一共可爬的网址共不超过300个文件，一次爬虫爬够10文件个程序自动关闭。
记得当发现爬虫被检测到终止爬去该文件时，要酌情删除结果文件：usr_info(x).txt,让其重新写入。
'''
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

global url, proxies, headers

PATH = sys.path[0] + '/'

def wudidaxunhuan(text):
    while len(text) < 200:
        print("啊啊啊啊被豆瓣发现了！先睡1小时！", flush=True)
        time.sleep(3600)
        response = requests.get(url, proxies=proxies, headers=headers)
        text = response.text
    return text

counter = 0
for num_i in [50]:
# for num_i in [50]:
# for num_i in [100]:
# for num_i in [150]:
# for num_i in [200]:
    f = open(PATH + '/BTOP250_%d_to_%d.txt' % (num_i + 1, num_i + 50),'r',encoding='utf-8')
    fr = f.readlines()
    counter += 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
    for each_line in fr:
        each_line = each_line.strip()
        url = each_line + "reviews?start=" + str(0)
        regix = '<span class="count">(.*?)</span>'
        proxies = {"http": "http://123.207.96.189:80"}
        response = requests.get(url, proxies=proxies, headers=headers)
        text = response.text
        text = wudidaxunhuan(text)
        results = re.findall(regix, text, re.S)
        #print(results)
        results = re.findall("\d+", str(results))
        if len(results) == 0: results = 0
        else: results = int(results[0])
        print('评论数：',results, flush=True)
        randomli = list(range(0,min(4000,results),20))
        random.shuffle(randomli)
        for nums in randomli:
            url = each_line+"reviews?start="+str(nums)
            print(url, flush=True)
            proxies = {"http": "http://123.207.96.189:80"}
            response = requests.get(url, proxies = proxies,headers=headers)
            text = response.text
            text = wudidaxunhuan(text)
            regix = '<header class="main-hd">.*?<a href=.*?class="avator">.*?<a href="(.*?)" class="name">(.*?)</a>.*?<span class="allstar(.*?) main-title-rating".*?</header>.*?<div class="action".*?<span id="r-useful_count-.*?">(.*?)</span>.*?<span id="r-useless_count-.*?">(.*?)</span>'
            results = re.findall(regix,text,re.S)
            if len(results) == 0:
                print('爬虫可能被检测到，也有可能没有这么多评论数，请打开网址查看', flush=True)
                continue
            for i in results:
                i = list(i)
                #print(i)
                for jj in range(2,len(i)):
                    tmp = re.findall('\d+',i[jj])
                    if len(tmp) != 0:
                        i[jj] = tmp[0]
                    else:
                        i[jj] = 0
                #print(i)
                write_content = ''+each_line + '\t'
                for each_info in i:
                    write_content += (str(each_info) + '\t')
                write_content += '\r\n'
                print(write_content, flush=True)
                with open(PATH + 'book_usr_info{}.txt'.format(counter+num_i),'a+',encoding='utf-8') as f:
                    f.write(write_content)
                # usrname = i[0][len("https://www.douban.com/people/")-1:]
                # print(usrname)
#        time.sleep((0.1+random.random())*20)
#    time.sleep((0.2+random.random())*40)
