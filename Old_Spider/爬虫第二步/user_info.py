import requests, re, json, codecs,time, random
'''
记住当爬虫无法爬取时，爬到的文件编号，过一会从这个文件开始爬。
我默认从文件r0开始爬，每个人开始地方不一样，分别从0，100，200开始爬
一共可爬的网址共不超过300个文件，一次爬虫爬够10文件个程序自动关闭。
记得当发现爬虫被检测到终止爬去该文件时，要酌情删除结果文件：usr_info(x).txt,让其重新写入。
'''
start = 0 #开始跑start start+1, ....  start+4五个文件
for num_i in range(10):
    f = open('r{}.txt'.format(start+num_i),'r',encoding='utf-8')
    fr = f.readlines()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
    for each_line in fr:
        each_line = each_line.split('\t')
        randomli = list(range(0,4000,20))
        random.shuffle(randomli)
        for nums in randomli:
            url = each_line[1]+"reviews?start="+str(nums)
            print(url)
            proxies = {"http": "http://123.207.96.189:80"}
            response = requests.get(url, proxies = proxies,headers=headers)
            text = response.text
            regix = '<header class="main-hd">.*?<a href=.*?class="avator">.*?<a href="(.*?)" class="name">(.*?)</a>.*?<span class="allstar(.*?) main-title-rating".*?</header>.*?<div class="action".*?<span id="r-useful_count-.*?">(.*?)</span>.*?<span id="r-useless_count-.*?">(.*?)</span>'

            results = re.findall(regix,text,re.S)
            if len(results) == 0:
                print('爬虫可能被检测到，也有可能没有这么多评论数，请打开网址查看')
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
                    write_content += (str(each_info) + '\t')
                write_content += '\r\n'
                print(write_content)
                with open('usr_info{}.txt'.format(num_i),'a+',encoding='utf-8') as f:
                    f.write(write_content)
                # usrname = i[0][len("https://www.douban.com/people/")-1:]
                # print(usrname)
        time.sleep((0.1+random.random())*20)
    num_i += 1
    time.sleep((0.2+random.random())*40)
