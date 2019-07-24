from spider_usr_info import get_info, headers, ualist, anti_anti_spider, proxies
import requests
from bs4 import BeautifulSoup as bs
import re
def get_movie_tag(url):
    print(url)
    rs = []
    regix = '<span property="v:genre">(.*?)</span>'
    response = requests.get(url, headers=headers, proxies=proxies)
    text = response.text
    text = anti_anti_spider(text, url)
    soup = bs(text, 'html.parser')
    soup_related = soup.find_all(class_='subject clearfix')
    print(soup_related)
    for i in soup_related:
        tmp = re.findall(regix, str(i), re.S)
        for i in tmp:
            rs.append(i)
    return rs

def main():
    with open('top_movie_info.txt', 'r',encoding='utf-8') as f:
        movie_url = f.readlines()
    for i in movie_url:
        i = i.split('\t')
        tag = get_movie_tag(i[0])
        rs = '' + i[0]
        for j in tag:
            rs += '\t' + j
        print(rs)
        rs += '\n'
        with open('topmovie_tag.txt', 'a+', encoding='utf-8') as f:
            f.write(rs)
main()