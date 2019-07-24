def func(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]
f = open('rs.txt','r',encoding='utf-8')
fr = f.readlines()
rr = func(fr,500)
num = 0
for i in rr:
    with open('r{}.txt'.format(num),'a+',encoding='utf-8') as wf:
        num += 1
        for j in i:
            wf.write(j)