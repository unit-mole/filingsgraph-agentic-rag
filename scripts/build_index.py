from __future__ import annotations
import argparse
from pathlib import Path
from filingsgraph.core.config import ROOT
from filingsgraph.embeddings.bge import BGEEmbeddingProvider,HashEmbeddingProvider
from filingsgraph.retrieval.dense import QdrantDenseIndex,LocalDenseIndex
from filingsgraph.retrieval.sparse import BM25Index
from scripts._common import load_jsonl,save_json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--smoke',action='store_true',help='Use hash embeddings for an offline smoke index; never use its metrics as portfolio results.');ap.add_argument('--dense-backend',choices=['qdrant','numpy'],default='qdrant');args=ap.parse_args()
    chunks=load_jsonl('data/processed/chunks.jsonl');
    if not chunks: raise RuntimeError('Run build_documents first')
    texts=[c['text'] for c in chunks]; embed=HashEmbeddingProvider() if args.smoke else BGEEmbeddingProvider()
    dense=QdrantDenseIndex(embed) if args.dense_backend=='qdrant' else LocalDenseIndex(embed);dense.build(texts,chunks)
    if args.dense_backend=='numpy':dense.save(ROOT/'data/index/dense')
    sparse=BM25Index();sparse.build(texts,chunks);sparse.save(ROOT/'data/index/bm25.pkl')
    report={'chunks_indexed':len(chunks),'embedding_backend':'hash-smoke' if args.smoke else 'BAAI/bge-m3','dense_backend':args.dense_backend,'bm25':True};save_json('reports/final/index_report.json',report);print(report)
if __name__=='__main__': main()
