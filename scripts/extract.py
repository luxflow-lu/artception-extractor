import argparse
from pathlib import Path
import pandas as pd
import re

from scripts.utils import CATEGORIES, slugify
from scripts.model import (
    CORE_CATEGORIES_COLS, CORE_STYLES_COLS,
    GRAPHISME_COLS, ARCHITECTURE_COLS, MUSIQUE_COLS, CINEMA_COLS,
    PALETTE_COLS, COULEUR_COLS, TYPEFACE_COLS, FONT_PAIRING_COLS,
    WORK_COLS, VARIANT_WORK_COLS, PERSON_COLS
)

from scripts.extract_graphisme import run as run_graphisme
from scripts.extract_architecture import run as run_architecture
from scripts.extract_musique import run as run_musique
from scripts.extract_cinema import run as run_cinema

OUT = Path("out/csv")
CORE = OUT / "core"

def write_df(df, path, cols):
    path.parent.mkdir(parents=True, exist_ok=True)
    for col in cols:
        if col not in df.columns:
            df[col] = ""
    df = df[cols]
    df.to_csv(path, index=False)

def init_categories():
    rows = [{"name": n, "slug": s, "icon_img_url":"", "accent_hex": ""} for (n,s) in CATEGORIES]
    cat_df = pd.DataFrame(rows)
    write_df(cat_df, CORE/"categories.csv", CORE_CATEGORIES_COLS)

def merge_styles(new_df):
    styles_path = CORE/"styles.csv"
    if styles_path.exists():
        old = pd.read_csv(styles_path)
        merged = pd.concat([old, new_df], ignore_index=True)
        merged = merged.drop_duplicates(subset=["slug"])
    else:
        merged = new_df
    write_df(merged, styles_path, CORE_STYLES_COLS)

def ensure_empty_graphisme_children():
    # Fichiers vides pour import Webflow, si non générés
    if not (OUT/"graphisme/palettes.csv").exists():
        write_df(pd.DataFrame(columns=PALETTE_COLS), OUT/"graphisme/palettes.csv", PALETTE_COLS)
    if not (OUT/"graphisme/couleurs.csv").exists():
        write_df(pd.DataFrame(columns=COULEUR_COLS), OUT/"graphisme/couleurs.csv", COULEUR_COLS)
    if not (OUT/"graphisme/typeface.csv").exists():
        write_df(pd.DataFrame(columns=TYPEFACE_COLS), OUT/"graphisme/typeface.csv", TYPEFACE_COLS)
    if not (OUT/"graphisme/font_pairing.csv").exists():
        write_df(pd.DataFrame(columns=FONT_PAIRING_COLS), OUT/"graphisme/font_pairing.csv", FONT_PAIRING_COLS)

def normalize_lang(s: str) -> str:
    # supprime espaces & virgules pendantes: "fr," -> "fr"
    parts = [p.strip() for p in (s or "").split(",") if p.strip()]
    return ",".join(parts) or "fr,en"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", required=True)
    ap.add_argument("--lang", default="fr,en")
    ap.add_argument("--limit", type=int, default=200)
    args = ap.parse_args()

    args.lang = normalize_lang(args.lang)

    init_categories()
    CORE.mkdir(parents=True, exist_ok=True)

    cat = args.category.lower()

    if cat in ["all", "graphisme"]:
        styles, variants, palettes, couleurs = run_graphisme(lang=args.lang, limit=args.limit)
        merge_styles(styles)
        write_df(variants, OUT/"graphisme/graphisme_variants.csv", GRAPHISME_COLS)
        write_df(palettes, OUT/"graphisme/palettes.csv", PALETTE_COLS)
        write_df(couleurs, OUT/"graphisme/couleurs.csv", COULEUR_COLS)
        ensure_empty_graphisme_children()

    if cat in ["all", "architecture"]:
        styles, variants = run_architecture(lang=args.lang, limit=args.limit)
        merge_styles(styles)
        write_df(variants, OUT/"architecture/architecture_variants.csv", ARCHITECTURE_COLS)

    if cat in ["all", "musique"]:
        styles, variants, persons = run_musique(lang=args.lang, limit=args.limit)
        merge_styles(styles)
        write_df(variants, OUT/"musique/musique_variants.csv", MUSIQUE_COLS)
        write_df(persons, OUT/"musique/person.csv", PERSON_COLS)

    if cat in ["all", "cinema", "cinéma"]:
        styles, variants, works, vworks = run_cinema(lang=args.lang, limit=args.limit)
        merge_styles(styles)
        write_df(variants, OUT/"cinema/cinema_variants.csv", CINEMA_COLS)
        write_df(works, OUT/"cinema/work.csv", WORK_COLS)
        write_df(vworks, OUT/"cinema/variant_work.csv", VARIANT_WORK_COLS)

    print("Done.")

if __name__ == "__main__":
    main()
