import sys
import io
import requests
import re
import json
import codecs
import time
import simulation
browser = simulation.simulation_douban()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
cookies = {'cookie': 'bid=Zr0xLjPNUH0; douban-fav-remind=1; ll="118371"; _vwo_uuid_v2=D690018C49C2B83B6195508B031F91851|8581f7fc12cecf5f8c98dee614b06fcf; ct=y; push_doumail_num=0; gr_user_id=5c279cfc-eb69-4458-8c06-a62c90e15f1f; __utmv=30149280.14496; viewed="4718973_1770782_4913064"; push_noty_num=0; __utmc=30149280; __utmz=30149280.1563502138.17.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="144963469:4Q2bplBjsWU"; ck=xoG-; douban-profile-remind=1; __utmc=81379588; __utmz=81379588.1563502731.9.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1563522593%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.1164937969.1563018575.1563502138.1563522593.18; __utmb=30149280.0.10.1563522593; __utma=81379588.1883385721.1563000694.1563502731.1563522593.10; __utmb=81379588.0.10.1563522593; _pk_id.100001.3ac3=26efb4105ebb6cd3.1563000694.10.1563523018.1563509626.'}
url = 'http://www.douban.com'
r = requests.get(url, cookies = cookies, headers = headers)
print(r.text)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
tag_num = 5


PATH = sys.path[0] + '/'




with open('tag{}.csv'.format(tag_num),'r',encoding='utf-8') as f:
    usrs = f.read().strip().split('\n')


for each_line in usrs:
    each_line = each_line.split('\t')
    url = each_line[1] + "reviews?start=" + str(0)
    regix = '<span class="count">(.*?)</span>'
    proxies = {"http": "http://123.207.96.189:80"}
    response = requests.get(url, proxies=proxies, headers=headers, cookies=cookies)
    text = response.text
    results = re.findall(regix, text, re.S)
    #print(results)
    results = re.findall("\d+", str(results))
    if len(results) == 0: results = 0
    else: results = int(results[0])
    print('评论数：',results, flush=True)
    randomli = list(range(0,min(200,results),20))
    for nums in randomli:
        url = each_line[1]+"reviews?start="+str(nums)
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
            print(i)
            for jj in range(2,len(i)):
                tmp = re.findall('\d+',i[jj])
                if len(tmp) != 0:
                    i[jj] = tmp[0]
                else:
                    i[jj] = 0
            #print(i)
            write_content = ''+each_line[1] + '\t'
            for each_info in i:
                write_content += (str(each_info).strip() + '\t')
            write_content += '\r\n'
            print(write_content, flush=True)
            with open('tag{}_usr.txt'.format(tag_num),'a+',encoding='utf-8') as f:
                f.write(write_content)
            # usrname = i[0][len("https://www.douban.com/people/")-1:]
            # print(usrname)
#        time.sleep((0.1+random.random())*20)
#    time.sleep((0.2+random.random())*40)