from __future__ import annotations
import json
from pathlib import Path
from filingsgraph.core.config import ROOT, load_yaml

def load_json(path:str|Path,default=None):
    p=ROOT/path if not Path(path).is_absolute() else Path(path)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default

def save_json(path:str|Path,obj):
    p=ROOT/path if not Path(path).is_absolute() else Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,default=str),encoding='utf-8'); return p

def load_jsonl(path:str|Path):
    p=ROOT/path if not Path(path).is_absolute() else Path(path)
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] if p.exists() else []

def save_jsonl(path:str|Path,rows:list[dict]):
    p=ROOT/path if not Path(path).is_absolute() else Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(''.join(json.dumps(r,default=str)+'\n' for r in rows),encoding='utf-8'); return p

def require_file(path:str|Path):
    p=ROOT/path if not Path(path).is_absolute() else Path(path)
    if not p.exists(): raise FileNotFoundError(f'Required artifact missing: {p}')
    return p
