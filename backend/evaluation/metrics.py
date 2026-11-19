"""Offline retrieval evaluation: Recall@k, MRR and nDCG@k."""
import json, math
from pathlib import Path
from app.services.rag import hybrid_retrieve

def evaluate(path="backend/evaluation/rag_queries.json", k=5):
    cases=json.loads(Path(path).read_text())
    recalls=[]; reciprocal=[]; ndcgs=[]
    for case in cases:
        ranked=hybrid_retrieve(case["query"],limit=k)
        relevant=set(case["relevant_ids"])
        ids=[x["id"] for x in ranked]
        hits=[1 if item in relevant else 0 for item in ids]
        recalls.append(len(set(ids)&relevant)/len(relevant))
        reciprocal.append(1/next((i+1 for i,x in enumerate(ids) if x in relevant), math.inf))
        dcg=sum(hit/math.log2(i+2) for i,hit in enumerate(hits))
        ideal=sum(1/math.log2(i+2) for i in range(min(len(relevant),k)))
        ndcgs.append(dcg/ideal if ideal else 0)
    return {"queries":len(cases),"k":k,"recall_at_k":round(sum(recalls)/len(recalls),4),"mrr":round(sum(reciprocal)/len(reciprocal),4),"ndcg_at_k":round(sum(ndcgs)/len(ndcgs),4)}

if __name__=="__main__":
    print(json.dumps(evaluate(),indent=2))
