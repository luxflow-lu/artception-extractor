# scripts/extract.py (extraits pertinents)
import argparse, pandas as pd
from pathlib import Path
from scripts.model import CORE_STYLES_COLS, ...  # inchangé

OUT = Path("out/csv"); CORE = OUT/"core"

def write_df(df, path, cols):
    path.parent.mkdir(parents=True, exist_ok=True)
    for c in cols:
        if c not in df.columns: df[c] = ""
    df[cols].to_csv(path, index=False)

def merge_styles(new_df, mode="isolate"):
    styles_path = CORE/"styles.csv"
    if mode == "merge" and styles_path.exists():
        old = pd.read_csv(styles_path)
        merged = pd.concat([old, new_df], ignore_index=True).drop_duplicates(subset=["slug"])
    else:
        merged = new_df
    write_df(merged, styles_path, CORE_STYLES_COLS)

def normalize_lang(s: str) -> str:
    parts = [p.strip() for p in (s or "").split(",") if p.strip()]
    return ",".join(parts) or "fr,en"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True)
    ap.add_argument("--lang", default="fr,en")
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--mode", choices=["isolate","merge"], default="isolate")
    args = ap.parse_args()
    args.lang = normalize_lang(args.lang)
    # init_categories() etc. (inchangé)
    # …
    if cat in ["all", "graphisme"]:
        styles, variants, palettes, couleurs = run_graphisme(lang=args.lang, limit=args.limit)
        merge_styles(styles, mode=args.mode)
        # ... (écriture des CSV graphisme)
    # idem pour les autres catégories (merge_styles(styles, mode=args.mode))
