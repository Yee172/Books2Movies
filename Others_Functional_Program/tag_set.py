with open('topmovie_tag.txt','r',encoding='utf-8') as f :
    lines = f.read().strip().split('\n')
rs = []
for line in lines:
    line = line.split('\t')
    for j in line[1:]:
        rs.append(j)
uniquers = list(set(rs))
li = [0]*len(uniquers)
dict_rs = dict(zip(uniquers,li))
for tag in rs:
    dict_rs[tag] = dict_rs[tag] + 1
list_rs= sorted(dict_rs.items(),key=lambda x:x[1], reverse=True)
for i in list_rs:
    print(i)