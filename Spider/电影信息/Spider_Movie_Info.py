import sys

from bs4 import BeautifulSoup as bs
import re

import time
import simulation
import random
browser = simulation.simulation_douban()
# browser.set_page_load_timeout(10)


with open('top_movies.txt','r',encoding='utf-8') as f:
    movies = f.read().strip().split('\n')


for movie in movies[:200]:
    rs = ''
    time.sleep(0.1)
    response = browser.get(movie)
    # time.sleep(random.random()*5)
    text = browser.page_source
    watched = browser.find_element_by_xpath('//*[@id="subject-others-interests"]/div/a[1]')
    star = re.findall('bigstar(\d+)',text)
    print(star)
    soup = bs(text, 'html.parser')

    name_related = soup.find_all('title')
    # print(name_related)
    name_regix = '>(.*?)<'
    for name in name_related:
        name = re.findall(name_regix, str(name), re.S)
        rs += name[0].strip()+'\t'
        # print(rs)
    info_related = soup.find_all(id='info')
    info_regix_1 = '<span class="pl">导演</span>: <span class="attrs"><a href=".*?>(.*?)</a></span>'
    info_regix_2 = '<span class="pl">编剧</span>: <span class="attrs">(.*?)</a></span></span><br/>'
    info_regix_3 = '<span property="v:genre">(.*?)</span>'
    info_regix_4 = '<a href=".*?" rel="v:starring">(.*?)</a>'
    # print(info_related, flush=True)
    # info_regix_5 = '(\d+)人看过'
    # watched_related = re.findall(info_regix_5, str(soup.string), re.S)
    # print(soup)
    # print(watched_related)
    for info in info_related:
        info1 = re.findall(info_regix_1, str(info), re.S)
        info2 = re.findall(info_regix_2, str(info), re.S)
        info3 = re.findall(info_regix_3, str(info), re.S)
        info4 = re.findall(info_regix_4, str(info), re.S)
        for i in info1:
            inner_regix = '<a href=".*?">(.*?)</a>'
            inner_info = re.findall(inner_regix, str(i), re.S)
            for j in inner_info:
                rs += str(j)+','
        rs += '\t'
        for i in info2:
            inner_regix = '<a href=".*?">(.*?)</a>'
            inner_info = re.findall(inner_regix, str(i), re.S)
            for j in inner_info:
                rs += str(j)+','
        rs += '\t'
        for i in info3:
            rs += str(i)+','
        rs += '\t'
        for i in info4[:6]:
            rs += str(i)+','
        rs += '\t'
    rs += str(star[0]) + '\t' + str(watched.text)
    rs += '\n'
    print(rs)
    with open('movie_info_new.txt','a+', encoding='utf-8') as f:
        f.write(rs)