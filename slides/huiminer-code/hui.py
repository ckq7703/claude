import itertools, json, random, time
profit={'a':5,'b':2,'c':1,'d':2,'e':3,'f':1,'g':1}
db=[{'a':1,'c':1,'d':1},{'a':2,'c':6,'e':2,'g':5},{'a':1,'b':2,'c':1,'d':6,'e':1,'f':5},{'b':4,'c':3,'d':3,'e':1},{'b':2,'c':2,'e':1,'g':2}]
def util(db,profit,X):
    return sum(sum(t[i]*profit[i] for i in X) for t in db if all(i in t for i in X))
def brute(db,profit,minutil):
    items=sorted(profit);res={}
    for k in range(1,len(items)+1):
        for X in itertools.combinations(items,k):
            u=util(db,profit,X)
            if u>=minutil:res[''.join(X)]=u
    return res
def huiminer(db,profit,minutil,log=None):
    twu={}
    for t in db:
        tu=sum(q*profit[i] for i,q in t.items())
        for i in t:twu[i]=twu.get(i,0)+tu
    keep=[i for i in twu if twu[i]>=minutil]
    order=sorted(keep,key=lambda i:(twu[i],i)); rank={i:k for k,i in enumerate(order)}
    UL={i:[] for i in order}
    for tid,t in enumerate(db,1):
        its=sorted([i for i in t if i in rank],key=lambda i:rank[i])
        rem=sum(t[i]*profit[i] for i in its)
        for i in its:
            u=t[i]*profit[i];rem-=u;UL[i].append((tid,u,rem))
    res={};stats={'joins':0,'nodes':0}
    def search(P,ULP,exts,depth):
        # exts: list of (itemset_tuple, ul)
        for k,(X,ulx) in enumerate(exts):
            stats['nodes']+=1
            su=sum(e[1] for e in ulx);sr=sum(e[2] for e in ulx)
            hui=su>=minutil;pr=su+sr<minutil
            if log is not None:log.append({'itemset':''.join(X),'u':su,'ub':su+sr,'hui':hui,'pruned':pr,'depth':depth,'ul':ulx})
            if hui:res[''.join(sorted(X))]=su
            if su+sr>=minutil:
                new=[]
                dx={e[0]:e for e in ulx}
                for (Y,uly) in exts[k+1:]:
                    stats['joins']+=1
                    dp={e[0]:e[1] for e in ULP} if ULP is not None else None
                    jl=[]
                    for (tid,uy,ry) in uly:
                        if tid in dx:
                            up=dp[tid] if dp else 0
                            jl.append((tid,dx[tid][1]+uy-up,ry))
                    if jl:new.append((X+(Y[-1],),jl))
                search(X,ulx,new,depth+1)
    search((),None,[((i,),UL[i]) for i in order],1)
    return res,stats,twu,order,UL
if __name__=='__main__':
    log=[];res,stats,twu,order,UL=huiminer(db,profit,30,log)
    bf=brute(db,profit,30)
    print('twu',twu,'order',order);print('ul',UL)
    print('res',res);print('bf',bf,res==bf,stats)
    for l in log:print(l['itemset'],l['u'],l['ub'],l['hui'],l['pruned'])
