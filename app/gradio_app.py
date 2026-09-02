from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/'src') not in sys.path: sys.path.insert(0,str(ROOT/'src'))
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
import gradio as gr
from filingsgraph.agents.planner import plan
from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository

DISCLAIMER="FilingsGraph is a research and financial-document intelligence tool. It summarizes and analyzes publicly available information and is not investment advice."

def list_companies():
    try:
        db=Database(); db.initialize(); rows=Repository(db).companies(); db.close(); return [r['ticker'] for r in rows]
    except Exception:
        return ['NVDA','AMD','INTC','AVGO','QCOM']

def research(question,ticker,years,full_mode):
    tickers=[ticker] if ticker and ticker!='ALL' else []
    ys=[]
    for x in (years or '').replace(',',' ').split():
        x=x.upper().replace('FY','')
        if x.isdigit(): ys.append(int(x))
    if full_mode:
        try:
            from app.runtime import full_engine
            r=full_engine().research(question,tickers,ys)
            evidence=[[e.get('ticker'),e.get('fiscal_year'),e.get('section'),e.get('citation_id'),e.get('source_excerpt','')[:500]] for e in r['evidence']]
            return r['answer'],json.dumps(r['plan'],indent=2),evidence,json.dumps(r['verification'],indent=2)
        except Exception as e:
            return f'Full runtime could not initialize: {e}',json.dumps(plan(question,tickers,ys).model_dump(),indent=2),[],json.dumps({'error':str(e)},indent=2)
    p=plan(question,tickers,ys)
    return 'Planning mode only. Enable Full local model/index after completing the build pipeline.',p.model_dump_json(indent=2),[],json.dumps({'mode':'planning-only'},indent=2)

def metric_history(ticker,metric):
    try:
        db=Database(); db.initialize(); rows=Repository(db).metric_history(ticker,metric); db.close(); return rows
    except Exception as e:
        return [{'error':str(e)}]

def risk_timeline(ticker):
    p=ROOT/'reports/temporal/temporal_evaluation.json'
    if not p.exists(): return {'status':'Run python -m scripts.evaluate_temporal first'}
    data=json.loads(p.read_text(encoding='utf-8'))
    return [r for r in data.get('rows',[]) if r.get('ticker')==ticker]

def graph_view(ticker):
    p=ROOT/'data/graph/filingsgraph.json'
    if not p.exists(): return {'status':'Run python -m scripts.build_graph first'}
    data=json.loads(p.read_text(encoding='utf-8')); nodes=data.get('nodes',[]); links=data.get('edges',data.get('links',[]))
    matches=[n for n in nodes if str(n.get('ticker','')).upper()==ticker.upper() or ticker.lower() in str(n.get('label','')).lower()]
    ids={n.get('id') for n in matches}; adj=[e for e in links if e.get('source') in ids or e.get('target') in ids]
    return {'seed_nodes':matches[:10],'adjacent_edges':adj[:50]}

companies=['ALL']+list_companies()
with gr.Blocks(title='FilingsGraph') as demo:
    gr.Markdown('# FilingsGraph — Temporal Financial Due-Diligence & Risk Intelligence Engine')
    gr.Markdown(DISCLAIMER)
    with gr.Tab('Ask Question'):
        with gr.Row():
            ticker=gr.Dropdown(companies,value=companies[0],label='Company')
            years=gr.Textbox(label='Fiscal years',placeholder='2023 2024 2025')
            full=gr.Checkbox(False,label='Full local model/index (loads GPU models)')
        q=gr.Textbox(lines=4,label='Research question',value='How has export-control risk language evolved across the selected annual filings?')
        run=gr.Button('Research',variant='primary')
        ans=gr.Markdown(); plan_box=gr.Code(label='Research plan',language='json')
        ev=gr.Dataframe(headers=['Ticker','FY','Section','Citation','Evidence'],label='Evidence')
        ver=gr.Code(label='Verification',language='json')
        run.click(research,[q,ticker,years,full],[ans,plan_box,ev,ver])
    with gr.Tab('Financial Facts'):
        t2=gr.Dropdown(companies[1:] or ['NVDA'],value=(companies[1:] or ['NVDA'])[0],label='Company')
        metric=gr.Dropdown(['revenue','net_income','operating_income','gross_profit','capex','assets','cash'],value='revenue',label='Metric')
        btn=gr.Button('Load history'); table=gr.Dataframe(); btn.click(metric_history,[t2,metric],table)
    with gr.Tab('Risk Timeline'):
        t3=gr.Dropdown(companies[1:] or ['NVDA'],value=(companies[1:] or ['NVDA'])[0],label='Company'); b3=gr.Button('Load timeline'); o3=gr.JSON(); b3.click(risk_timeline,t3,o3)
    with gr.Tab('Graph Explorer'):
        t4=gr.Dropdown(companies[1:] or ['NVDA'],value=(companies[1:] or ['NVDA'])[0],label='Company'); b4=gr.Button('Explore graph'); o4=gr.JSON(); b4.click(graph_view,t4,o4)
    with gr.Tab('Evaluation'):
        gr.Markdown('Evaluation artifacts are generated under `reports/`. Metrics remain TBD until the corresponding local script is actually run.')
if __name__=='__main__':
    demo.launch(server_name='127.0.0.1',server_port=7860,show_error=True)
