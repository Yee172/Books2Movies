import requests, re, json, codecs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}

url = 'https://book.douban.com/tag'

proxies = {"http": "http://123.207.96.189:80"}
response = requests.get(url, proxies = proxies,headers=headers)
text = response.text
regix = '<td><a href=".*?">(.*?)</a><b>.*?</b></td>'

results = re.findall(regix,text,re.S)
for i in results:
    for num_i in range(0,1000,20):
        tag = str(i)
        tag_url = 'https://book.douban.com/tag/' +tag + '?start=' + str(num_i)
        t_response = requests.get(tag_url, proxies=proxies, headers=headers)
        t_text = t_response.text
        tag_regix = '<h2 class="">.*?<a href="(.*?)".*?title="(.*?)".*?>'
        t_results = re.findall(tag_regix, t_text, re.S)
        for j in t_results:
            write_content = '' + tag +'\t'+ j[0] + '\t' + j[1] + '\n'
            print(write_content)
            writefile = codecs.open("rs1.txt", "a+", encoding="utf-8")
            writefile.write(write_content)
            writefile.close()
