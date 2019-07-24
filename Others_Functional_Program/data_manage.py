li = [];
with open('book_usr_info.txt','r',encoding='utf-8') as f:
    fr = f.readlines()
    for i in fr:
        if i == '\n': continue
        i = i.split('\t')
        li.append(i[1])
with open('usr_id_url.txt','a+',encoding='utf-8') as f:
    for i in li:
        i += '\n'
        f.write(i)
li = list(set(li))
print(len(li))