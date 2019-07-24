import sys

from bs4 import BeautifulSoup as bs
import re
import random
import time
import simulation
browser = simulation.simulation_douban()

# tag_num = 0 -> 1 - 250
# tag_num = 1 -> 251 - 500
# tag_num = 2 -> 501 - 750
# tag_num = 3 -> 751 - 1000
tag_num = 0


PATH = sys.path[0] + '/'
def browser_sleep_get(url):
    response = browser.get(url)
    time.sleep(2)
    return response

with open('1000users_{}_to_{}.csv'.format(tag_num * 250 + 1, (tag_num + 1) * 250), 'r', encoding='utf-8') as f:
    usrs = f.read().strip().split('\n')
# print(usrs)

for each_line in usrs:
    usr_movie = each_line[len('https://www.douban.com/people/'):]
    url = 'https://movie.douban.com/people/' + usr_movie + "collect?start=" + str(0)
    regix1 = '<title>(.*?)</title>'
    time.sleep(0.1)
    response = browser.get(url)
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
    randomli = list(range(0, min(1500,results), 15))
    for nums in randomli:
        url = 'https://movie.douban.com/people/'+ usr_movie +'collect?'+"start="+str(nums)
        print(url, flush=True)
        response = browser.get(url)
        text = browser.page_source
        regix = '<a.*?href="(.*?)".*?<em>(.*?)</em>.*?<span class="rating(\d+)-t">'
        soup = bs(text, 'html.parser')
        soup_related = soup.find_all(class_='item')
        for i in soup_related:
            rs = each_line
            tmp = re.findall(regix, str(i), re.S)
            if len(tmp) == 0: continue
            for rows in tmp:
                for row in rows:
                    rs += '\t' + row
            print(rs)

            with open('1000user_movie_{}.txt'.format(tag_num),'a+', encoding='utf-8') as f:
                f.write(rs + '\n')
        time.sleep(random.random() * 2 + 1)
