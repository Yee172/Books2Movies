import sys

from bs4 import BeautifulSoup as bs
import re

import time
import simulation
import random
browser = simulation.simulation_douban()
# browser.set_page_load_timeout(10)



with open('user_name_table.csv','r',encoding='utf-8') as f:
    usrs = f.read().strip().split('\n')


for usr in usrs[0:300]:
    rs = ''
    usr = usr.split('\t')
    url = usr[1]
    rs = ''
    time.sleep(0.1)
    response = browser.get(url)
    # time.sleep(random.random()*5)
    follower = browser.find_element_by_xpath('//*[@id="content"]/div/div[2]/p[1]/a')
    rs += usr[0] + '\t' + str(follower.text) + '\n'
    with open('user_info.txt','a+', encoding='utf-8') as f:
        f.write(rs)