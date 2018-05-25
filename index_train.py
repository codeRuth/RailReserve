fo = open('train.txt')
t = fo.read().split("\n")
x = list()
c=0
for i in t :
    s = i.split("|")
    z = [s[1]+s[2],c]
    x.append(z)
    c = c + 1
data = sorted(x, key=lambda y: y[0])
fo.close()
fo=open('train_index.txt','w')
for i in  data:
    for j in i :
        fo.write(str(j))
        fo.write('|')
    fo.write('\n')
fo.close()