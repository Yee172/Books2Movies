import requests, re, time, random
from bs4 import BeautifulSoup as bs
global headers, proxies

num = 3



ualist = [  # 一些可用的浏览器名称
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

headers = {"Connection": "Keep-alive", "User-Agent": random.choice(ualist)}
def login():
    # 利用账号密码登录豆瓣网，python代码模拟登录网页操作

    url = "https://accounts.douban.com/j/mobile/login/basic"
    # 随机添加/修改User-Agent
    data = {'name': '18744296191', 'password': '665599asdfghjkl'}  # 自己的账号密码
    r = requests.post(url, data=data, headers=headers)
    print(r.text)  # 查看响应内容，r.text返回的是Unicode格式的数据
    print(r.url)  # 查看完整url地址
    print(r.status_code)  # 查看响应码


def anti_anti_spider(text, url):
    while len(text) < 200:
        print('IP可能被封请注意')
        time.sleep(1000)
        response = requests.get(url, proxies = proxies, headers = headers)
        text = response.text
    return text

def get_info(url,regix):
    print(url)
    proxies = {"http": "http://123.207.96.189:80"}
    response = requests.get(url, proxies = proxies,headers=headers)
    text = response.text
    text = anti_anti_spider(text, url)
    results = re.findall(regix, text, re.S)
    return results

def get_movie_info(url,regix):
    rs = []
    print(url)
    proxies = {"http": "http://123.207.96.189:80"}
    response = requests.get(url, proxies=proxies, headers=headers)
    text = response.text
    text = anti_anti_spider(text, url)
    soup = bs(text, 'html.parser')
    soup_related = soup.find_all(class_='item')
    for i in soup_related:
        #print(str(i))
        tmp = re.findall(regix, str(i), re.S)
        if len(tmp) == 0: continue
        rs.append(tmp[0])
        #print(tmp)
    return rs

def main():
    login()
    havedone = 0
    global num
    with open('top1000_usr_{}.txt'.format(num),'r', encoding='utf-8') as opf:
        tol_url = opf.readlines()
    file_len = len(tol_url)
    for each_url in tol_url:
        ignore = len('https://www.douban.com/people/')
        base_url = 'https://movie.douban.com/people/' + each_url[ignore:-2] + '/collect?start='
        url = 'https://movie.douban.com/people/' + each_url[ignore:-2] + '/collect?start=0'
        print(url)
        regix1 = '<title>(.*?)</title>'
        regix2 = '<li class="title">.*?<a class="" href="(.*?)">.*?<em>(.*?)</em>.*?<span class="rating(.*?)"></span>'
        rs = get_info(url,regix1)
        #print(rs)
        maxnum = re.findall('\d+',rs[0], re.S)
        #print(maxnum)
        maxnum = int(maxnum[0])
        print('电影数量：',maxnum)
        spider_list = list(range(0, maxnum, 15))
        random.shuffle(spider_list)
        for each_page in spider_list:
            url = base_url + str(each_page)
            rs = get_movie_info(url, regix2)
            write_content = ''
            #print(rs)
            for i in rs:
                write_content += each_url[:-2]
                for j in i:
                    write_content += '\t' + str(j)
                write_content += '\n'
            print(write_content)
            with open('rs_usr_info{}.txt'.format(num),'a+',encoding = 'utf-8') as f:
                f.write(write_content)
        havedone += 1
        print("%.2f%%已完成" % ((100*havedone)/file_len))

if __name__ == '__main__':
    main()