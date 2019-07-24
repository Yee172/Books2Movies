import requests
import re
import json
import codecs

writefile = codecs.open("rs.txt", "w", encoding="utf-8")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
for each_url in range(0,250,25):
    url = 'https://movie.douban.com/top250?start='+ str(each_url)+'&filter='

    proxies = {
        "http": "http://123.207.96.189:80"
    }
    response = requests.get(url, proxies = proxies,headers=headers)
    text = response.text
    regix = '<div class="item">.*?<div class="pic">.*?<em class="">(.*?)</em>.*?<a.*?href="(.*?)">.*?<img.*?src="(.*?)" class="">.*?div class="info.*?class="hd".*?class="title">(.*?)</span>.*?class="other">(.*?)</span>.*?<div class="bd">.*?<p class="">(.*?)<br>(.*?)</p>.*?class="star.*?<span class="(.*?)"></span>.*?span class="rating_num".*?average">(.*?)</span>'
    results = re.findall(regix,text,re.S)

    for item in results:
        for num in range(0,200,20):
            movieurl = item[1] + "comments?start=" + str(num) + "&limit=20&sort=new_score&status=P"
            print(movieurl)
            movieresponse = requests.get(movieurl, proxies = proxies, headers = headers)
            text_comment = movieresponse.text
            #re_comment = '<div class="comment">.*?<span class="comment-vote">.*?<span class="votes">(.*?)</span>.*?<input value="(.*?)".*?type="hidden"/>.*?<span class="comment-info>.*?<a.*?href"(.*?)" class="">(.*?)</a>.*?<span class="short">(.*?)</span>'
            #re_comment = '<div class="comment">.*?<span class="comment-vote">.*?<span class="votes">(.*?)</span>.*?<input value="(.*?)".*?type="hidden"/>.*?<span class="short">(.*?)</span>'
            re_comment = '<span class="comment-info">.*?<a href="(.*?)" class="">(.*?)</a>'
            rs_comment = re.findall(re_comment, text_comment,re.S)
            for each_rs in rs_comment:

                tmp = "" + item[3]+"\t"
                for x in each_rs:
                    tmp += (str(x)+"\t")
                print(tmp)
                tmp += "\n"
                tmp = tmp.encode('utf-8')
                writefile.write((tmp.decode()))
writefile.close()