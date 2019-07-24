import sys

from bs4 import BeautifulSoup as bs
import re

import time
import simulation
import random
browser = simulation.simulation_douban()

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
# cookies = {'cookie': 'bid=Zr0xLjPNUH0; douban-fav-remind=1; ll="118371"; _vwo_uuid_v2=D690018C49C2B83B6195508B031F91851|8581f7fc12cecf5f8c98dee614b06fcf; ct=y; push_doumail_num=0; gr_user_id=5c279cfc-eb69-4458-8c06-a62c90e15f1f; __utmv=30149280.14496; viewed="4718973_1770782_4913064"; push_noty_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1563502132%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dnq9RH2ts87fRnnMKOPQ5sCQXBuNzmGFA70S_ALU_PTU7xdhhCV1b4gyOBICjGTsA%26wd%3D%26eqid%3Dd88e313600326089000000065d31262d%22%5D; _pk_id.100001.8cb4=ec78e2bd846c73dd.1560593993.13.1563502132.1563205608.; _pk_ses.100001.8cb4=*; __utma=30149280.1164937969.1563018575.1563284841.1563502138.17; __utmc=30149280; __utmz=30149280.1563502138.17.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1563502138; dbcl2="144963469:4Q2bplBjsWU"'}
# url = 'http://www.douban.com'
# r = requests.get(url, cookies = cookies, headers = headers)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
tag_nums = [4,8]
for tag_num in tag_nums:



    PATH = sys.path[0] + '/'
    def browser_sleep_get(url):
        response = browser.get(url)
        time.sleep(2)
        return response



    with open('tag{}_usr.txt'.format(tag_num),'r',encoding='utf-8') as f:
        usrs = f.read().strip().split('\n\n')
    # print(usrs)


    for each_line in usrs:
        each_line = each_line.split('\t')
        usr_movie = each_line[1][len('https://www.douban.com/people/'):]
        url = 'https://movie.douban.com/people/' + usr_movie + "collect?start=" + str(0)
        regix1 = '<title>(.*?)</title>'
        time.sleep(0.1)
        response = browser.get(url)
        time.sleep(random.random()*10)
        text = browser.page_source
        # print(text)
        results = re.findall(regix1, text, re.S)
        # results = re.findall(regix2,text,re.S)
        #print(results)
        results = re.findall("\d+", str(results))
        # print(results)
        if len(results) == 0: results = 0
        else: results = int(results[-1])
        # print(results)
        print('电影数：',results)
        randomli = list(range(0,min(1500,results),15))
        for nums in randomli:
            url = 'https://movie.douban.com/people/'+ usr_movie +'collect?'+"start="+str(nums)
            print(url, flush=True)
            response = browser.get(url)
            text = browser.page_source
            regix = '<a.*?href="(.*?)".*?<em>(.*?)</em>.*?<span class="rating(\d+)-t">'
            soup = bs(text, 'html.parser')
            soup_related = soup.find_all(class_='item')
            for i in soup_related:
                rs =''+ each_line[1] + '\t' + each_line[2]
                tmp = re.findall(regix, str(i), re.S)
                if len(tmp) == 0: continue
                for rows in tmp:
                    for row in rows:
                        rs += '\t' + row
                    rs += '\n'
                print(rs)

                with open('user_movie{}.txt'.format(tag_num),'a+', encoding='utf-8') as f:
                    f.write(rs)
