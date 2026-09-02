from __future__ import annotations
from pathlib import Path
from filingsgraph.core.config import ROOT,load_yaml
from filingsgraph.schemas.filings import FilingMetadata
from filingsgraph.parsing.sections import extract_sections
from filingsgraph.parsing.chunking import section_aware_chunks
from filingsgraph.parsing.tables import extract_tables
from scripts._common import load_json,save_jsonl,save_json

def main():
    metas=[FilingMetadata(**x) for x in (load_json('data/processed/filings_metadata.json') or [])]
    if not metas: raise RuntimeError('No filing metadata. Run download_filings first.')
    targets=load_yaml('companies.yaml').get('sections'); chunks=[]; sections=[]; tables_all=[]; table_manifest=[]; failures=[]
    for m in metas:
        try:
            html=(ROOT/m.local_path).read_text(encoding='utf-8',errors='replace'); docid=m.accession_number
            secs=extract_sections(html,docid,targets)
            if not secs: failures.append({'accession':docid,'reason':'no target sections extracted'})
            sections.extend([s.model_dump() for s in secs])
            for s in secs: chunks.extend([c.model_dump() for c in section_aware_chunks(s,m)])
            tables=extract_tables(html)
            for t in tables:
                t.update({'accession_number':docid,'ticker':m.ticker,'fiscal_year':m.fiscal_year,'source_url':m.source_url})
                tables_all.append(t)
            table_manifest.append({'accession':docid,'table_count':len(tables)})
        except Exception as e: failures.append({'accession':m.accession_number,'reason':str(e)})
    save_jsonl('data/processed/sections.jsonl',sections);save_jsonl('data/processed/chunks.jsonl',chunks);save_jsonl('data/processed/tables.jsonl',tables_all);save_json('data/processed/table_manifest.json',table_manifest)
    report={'filings':len(metas),'sections':len(sections),'chunks':len(chunks),'tables':len(tables_all),'failures':failures};save_json('reports/final/parsing_report.json',report);print(report)
    if not chunks: raise SystemExit('No chunks were built; inspect parsing_report.json')
if __name__=='__main__': main()
