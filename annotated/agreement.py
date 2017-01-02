# coding: utf-8

f=open('bhargav_hi.csv')
g=open('shyam_hi.csv')
h=open('bhargav_hi.csv')
i=open('shyam_hi.csv')
j=open('shyam_hi.csv')
f.readline(),g.readline(),h.readline(),i.readline(),j.readline()
lines=[(l1.strip(),l2.strip(),l3.strip(),l4.strip(),l5.strip()) for
       l1,l2,l3,l4,l5 in zip(f,g,h,i,j)]
count=0
for line in lines:
    l1,l2,l3,l4,l5=line
    l1,l2,l3,l4,l5=l1.split(','),l2.split(','),l3.split(','),l4.split(','),l5.split(',')
    o1,o2,o3,o4,o5=l1[0],l2[0],l3[0],l4[0],l5[0]
    agree_cnt=[o1,o2,o3,o4,o5].count("yes")
    print(l1[1:],agree_cnt)
# print(count)
