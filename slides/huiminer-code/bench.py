from hui import *
import random,time,json,itertools
random.seed(7)
items=[chr(97+i) for i in range(22)]
prof={i:random.choice([1,1,2,2,3,5,8,12]) for i in items}
D=[]
for _ in range(400):
    L=random.randint(4,9);S=random.sample(items,L)
    D.append({i:random.randint(1,4) for i in S})
tot=sum(sum(q*prof[i] for i,q in t.items()) for t in D)
def twophase(D,prof,mu):
    tus=[sum(q*prof[i] for i,q in t.items()) for t in D]
    sets=[frozenset(t) for t in D]
    cand=0;ncand=[]
    twu={}
    for s,tu in zip(sets,tus):
        for i in s:twu[(i,)]=twu.get((i,),0)+tu
    L=sorted(k for k,v in twu.items() if v>=mu);allc=list(L);ncand.append(len(L))
    while L:
        nxt=set()
        Ls=set(L)
        for a in L:
            for b in L:
                if a[:-1]==a[:-1] and a[:-1]==b[:-1] and a[-1]<b[-1]:
                    c=a+(b[-1],)
                    if all(c[:j]+c[j+1:] in Ls for j in range(len(c))):nxt.add(c)
        cnt={}
        for s,tu in zip(sets,tus):
            for c in nxt:
                if s.issuperset(c):cnt[c]=cnt.get(c,0)+tu
        L=sorted(k for k,v in cnt.items() if v>=mu);allc+=L;ncand.append(len(L))
    res={}
    for c in allc:
        u=util(D,prof,c)
        if u>=mu:res[''.join(c)]=u
    return res,len(allc)
out=[]
for pct in (3.0,2.5,2.0,1.5,1.0):
    mu=int(tot*pct/100)
    t=time.time();r1,nc=twophase(D,prof,mu);t1=time.time()-t
    t=time.time();r2,st,_,_,_=huiminer(D,prof,mu);t2=time.time()-t
    assert r1==r2,(len(r1),len(r2))
    out.append(dict(pct=pct,mu=mu,hui=len(r2),cand=nc,tp_t=round(t1,2),joins=st['joins'],nodes=st['nodes'],hm_t=round(t2,2)))
    print(out[-1])
json.dump(out,open('bench.json','w'))
