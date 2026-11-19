"""Measure local retrieval latency; numbers describe this runner, not production."""
import json, statistics, time
from pathlib import Path
from app.services.rag import hybrid_retrieve

def run(repeats=10):
    cases=json.loads(Path("backend/evaluation/rag_queries.json").read_text())
    samples=[]
    for _ in range(repeats):
        for case in cases:
            start=time.perf_counter()
            hybrid_retrieve(case["query"],limit=5)
            samples.append((time.perf_counter()-start)*1000)
    ordered=sorted(samples)
    p95=ordered[min(len(ordered)-1,int(0.95*len(ordered)))]
    return {"environment":"GitHub Actions runner (runtime varies)","queries":len(cases),"repeats_per_query":repeats,"measurements":len(samples),"latency_ms":{"median":round(statistics.median(samples),3),"p95":round(p95,3),"mean":round(statistics.mean(samples),3)},"scope":"in-process retrieval only; excludes network, database, embedding API and LLM latency"}

if __name__=="__main__": print(json.dumps(run(),indent=2))
