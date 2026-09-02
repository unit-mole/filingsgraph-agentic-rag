def classification_scores(gold:list[str],pred:list[str])->dict:
    labels=sorted(set(gold)|set(pred)); tp=fp=fn=0
    per={}
    for l in labels:
        t=sum(g==l and p==l for g,p in zip(gold,pred)); f_p=sum(g!=l and p==l for g,p in zip(gold,pred)); f_n=sum(g==l and p!=l for g,p in zip(gold,pred))
        pr=t/(t+f_p) if t+f_p else 0; rc=t/(t+f_n) if t+f_n else 0; f1=2*pr*rc/(pr+rc) if pr+rc else 0
        per[l]={"precision":pr,"recall":rc,"f1":f1}; tp+=t;fp+=f_p;fn+=f_n
    return {"macro_f1":sum(x['f1'] for x in per.values())/len(per) if per else 0,"per_label":per}
