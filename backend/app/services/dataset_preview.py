"""Allowlisted, bounded previews from public environmental data providers."""
import csv, io, json, urllib.request
from app.data.dataset_catalog import get_dataset_catalog

def preview_dataset(dataset_id: str, limit: int = 10):
    item=next((d for d in get_dataset_catalog() if d["id"]==dataset_id),None)
    if not item: return None
    request=urllib.request.Request(item["download_url"],headers={"User-Agent":"EcoScholar/0.3 (+https://github.com/charan-143/EcoScholar)"})
    with urllib.request.urlopen(request,timeout=20) as response:
        payload=response.read(3_000_000).decode("utf-8-sig")
    if item["download_url"].endswith(".csv"):
        reader=csv.DictReader(io.StringIO(payload))
        rows=[]
        for row in reader:
            rows.append(row)
            if len(rows)>=limit: break
    else:
        raw=json.loads(payload)
        records=raw[1] if isinstance(raw,list) and len(raw)>1 and isinstance(raw[1],list) else []
        rows=[{"country":r.get("country",{}).get("value"),"year":r.get("date"),"value":r.get("value"),"indicator":r.get("indicator",{}).get("value")} for r in records[:limit]]
    return {"dataset":item,"rows":rows,"row_count":len(rows),"note":"Live source preview; values retain the source provider's definitions and units. This response is not a validated analytical dataset."}
