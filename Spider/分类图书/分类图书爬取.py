
from bs4 import BeautifulSoup as bs
import re
import requests
def anti_anti_spider(text, url):
    while len(text) < 200:
        print('IP可能被封请注意')
        time.sleep(1000)
        response = requests.get(url, proxies = proxies, headers = headers)
        text = response.text
    return text

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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
cookies = 'yourcookie'
url = 'http://www.douban.com'
r = requests.get(url, cookies = cookies, headers = headers)
txt = '马哲 哲学 社会科学 政治法律\ 军事\ 经济\ 文化科学教育体育\ 语言文字 文学 艺术 \历史地理 \自然科学 数理科学化学 天文地球科学 生物 医药卫生 农业 工业 交通 航空航天 环境'
book_tag1 = ['文学', '诗词', '散文', '随笔', '杂文', '外国文学']
book_tag2 = ['流行', '推理', '悬疑', '言情', '青春', '网络小说', '武侠', '科幻', '漫画']
book_tag3 = ['文化', '国学', '传记',  '教育','中国历史',]
book_tag4 = ['马哲', '哲学','佛教', '西方哲学', '社会学', '政治', '宗教']
book_tag5 = ['军事', '军事', '二战']
book_tag6 = ['经济金融', '经济学', '理财', '投资','金融','股票', '商业', '创业']
book_tag7 = ['艺术','艺术','戏剧', '建筑', '音乐','绘画']
book_tag8 = ['科普', '互联网', '编程', '科学', '神经网络','科技','算法', '程序']

for tag in book_tag8[-1:]:
    print(tag)
    tagurl = 'https://book.douban.com/tag/'
    tagurl += tag
    response = requests.get(tagurl, cookies=cookies, headers=headers)
    text = response.text
    text = anti_anti_spider(text, tagurl)
    soup = bs(text, 'html.parser')
    # print(soup)
    soup_related = soup.find_all(
        class_='info'
    )
    print(soup_related)
    for book in soup_related:
        bookurl = re.findall('<a href="(.*?)".*?title="(.*?)">', str(book), re.S)
        print(bookurl)
        rs = ''+tag+'\t'+str(bookurl[0][0]) + '\t' + str(bookurl[0][1]) + '\n'
        print(rs)
        with open('tag8.csv', 'a+', encoding='utf-8') as f:
            f.write(rs)



