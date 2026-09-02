from __future__ import annotations
import difflib,re,hashlib
from dataclasses import dataclass,asdict

@dataclass
class RiskChange:
    risk_id:str; topic:str; change_type:str; old_excerpt:str|None; new_excerpt:str|None; similarity:float; evidence_span:str

def _sentences(text:str)->list[str]:
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if len(s.strip())>40]

def topic_passages(text:str,topic:str)->list[str]:
    terms=set(re.findall(r'[a-z]+',topic.lower()))
    return [s for s in _sentences(text) if terms and any(t in s.lower() for t in terms)]

def compare_risk_topic(old_text:str,new_text:str,topic:str)->RiskChange:
    old=' '.join(topic_passages(old_text,topic))[:4000]; new=' '.join(topic_passages(new_text,topic))[:4000]
    sim=difflib.SequenceMatcher(None,old.lower(),new.lower()).ratio() if old and new else 0.0
    if not old and new: ct='NEW'
    elif old and not new: ct='REMOVED'
    elif not old and not new: ct='UNCHANGED'
    else:
        ratio=(len(new)+1)/(len(old)+1)
        if sim>=0.90: ct='UNCHANGED'
        elif ratio>=1.20: ct='EXPANDED'
        elif ratio<=0.80: ct='REDUCED'
        else: ct='EXPANDED' if len(new)>len(old) else 'REDUCED'
    rid=hashlib.sha1(topic.lower().encode()).hexdigest()[:12]
    evidence=(new or old)[:1200]
    return RiskChange(rid,topic,ct,old[:1200] or None,new[:1200] or None,sim,evidence)

def compare_risk_disclosures(old_text:str,new_text:str,topics:list[str])->list[dict]:
    return [asdict(compare_risk_topic(old_text,new_text,t)) for t in topics]
