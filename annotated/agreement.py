# coding: utf-8
import sys

def load_judgements(filepath):
    f=open(filepath)
    f.readline()
    judgements=[]
    for l in f:
        parts=l.strip().split(",")
        val=parts[0]
        key=(parts[1],parts[2])
        judgements.append((key,val))
    return dict(judgements)

# jj=load_judgements('shyam_hi.csv')
# print(jj)
# print(len(jj))
# sys.exit(0)

f=load_judgements('bhargav_hi.csv')
g=load_judgements('shyam_hi.csv')
h=load_judgements('vyas_hi.csv')
# i=load_judgements('shyam_hi.csv')
# j=load_judgements('shyam_hi.csv')

assert len(f.keys())==len(g.keys())
# f.readline(),g.readline(),h.readline(),i.readline(),j.readline()
# lines=[(l1.strip(),l2.strip(),l3.strip(),l4.strip(),l5.strip()) for
#        l1,l2,l3,l4,l5 in zip(f,g,h,i,j)]

key_counts=[]
for key in f.keys():
    # l1,l2,l3,l4,l5=line
    # l1,l2,l3,l4,l5=l1.split(','),l2.split(','),l3.split(','),l4.split(','),l5.split(',')
    # o1,o2,o3,o4,o5=f[key],g[key],h[key],i[key],j[key]
    # agree_cnt=[o1,o2,o3,o4,o5].count("yes")
    o1,o2,o3=f[key],g[key],h[key]
    agree_cnt=[o1,o2,o3].count("yes")
    print(key,agree_cnt)
    key_counts.append((key,agree_cnt))

key_counts=sorted(key_counts, key=lambda x: x[1])
print([k for k in key_counts if k[1]==3])
print(len([k for k in key_counts if k[1]==3]))
