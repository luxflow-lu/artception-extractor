import requests, pandas as pd

WDQS = "https://query.wikidata.org/sparql"
UA = {"User-Agent": "ArtceptionExtractor/1.0 (https://github.com/you/repo)"}

def sparql(query: str, lang="fr,en"):
    headers = {"Accept": "application/sparql-results+json", **UA}
    q = query.replace("${LANG}", lang)
    r = requests.get(WDQS, params={"query": q}, headers=headers, timeout=60)
    r.raise_for_status()
    data = r.json()["results"]["bindings"]
    rows = []
    for b in data:
        row = {}
        for k,v in b.items():
            row[k] = v.get("value")
        rows.append(row)
    return pd.DataFrame(rows)

def art_movements_query(limit=200):
    # Q968159 = art movement
    return f"""
    SELECT ?style ?styleLabel ?start ?end ?image WHERE {{
      ?style wdt:P31/wdt:P279* wd:Q968159 .
      OPTIONAL {{ ?style wdt:P580 ?start. }}
      OPTIONAL {{ ?style wdt:P582 ?end. }}
      OPTIONAL {{ ?style wdt:P18  ?image. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "${{LANG}}". }}
    }} LIMIT {limit}
    """

def architectural_styles_query(limit=200):
    # Q32880 = architectural style
    return f"""
    SELECT ?style ?styleLabel ?start ?end ?image WHERE {{
      ?style wdt:P31/wdt:P279* wd:Q32880 .
      OPTIONAL {{ ?style wdt:P580 ?start. }}
      OPTIONAL {{ ?style wdt:P582 ?end. }}
      OPTIONAL {{ ?style wdt:P18  ?image. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "${{LANG}}". }}
    }} LIMIT {limit}
    """
