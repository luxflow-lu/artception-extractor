from pathlib import Path
import pandas as pd
from scripts.sources.wikidata import sparql, art_movements_query
from scripts.utils import slugify
from scripts.model import CORE_STYLES_COLS, GRAPHISME_COLS, PALETTE_COLS, COULEUR_COLS
from scripts.utils import CATEGORIES

def run(lang="fr,en", limit=200, outdir=Path("out/csv/graphisme")):
    outdir.mkdir(parents=True, exist_ok=True)

    seed = pd.read_csv("data/seeds/styles_core.csv")
    seed = seed[seed["categories"].str.contains("Graphisme", case=False, na=False)].copy()

    df = sparql(art_movements_query(limit=limit), lang=lang)
    if df.empty:
        df = pd.DataFrame(columns=["style","styleLabel","start","end","image"])
    df["qid"] = df["style"].str.rsplit("/", n=1).str[-1]
    df.rename(columns={"styleLabel":"name","image":"cover_img_url"}, inplace=True)

    # Merge basic periods/origin from seed
    seed_basic = seed[["qid","style","era_from","era_to","origin"]].rename(columns={"style":"seed_name"})
    core = df.merge(seed_basic, on="qid", how="left")

    # CORE STYLES
    styles = pd.DataFrame({
        "name": core["name"].fillna(core["seed_name"]).fillna(core["qid"]),
        "slug": core["name"].fillna(core["seed_name"]).fillna(core["qid"]).apply(lambda x: slugify(x)),
        "qid": core["qid"],
        "era_from": core["era_from"],
        "era_to": core["era_to"],
        "origin": core["origin"],
        "summary_rte": "",
        "principles_rte": "",
        "mood_tags_text": "",
        "cover_img_url": core["cover_img_url"],
        "sources_text": "",
        "extra_json": ""
    })[CORE_STYLES_COLS].drop_duplicates(subset=["slug"])

    # VARIANTS (Graphisme)
    variants = pd.DataFrame({
        "name": styles["name"] + " — Graphisme",
        "slug": styles["slug"] + "-graphisme",
        "style_ref_name": styles["name"],
        "category_ref_name": "Graphisme",
        "intro_rte": "",
        "gallery_urls_text": "",
        "featured": "",
        "order": "",
        "sources_text": "",
        "extra_json": "",
        "use_cases": "UI;Branding;Affiche",
        "shapes_motifs_rte": "",
        "web_tokens_json": ""
    })[GRAPHISME_COLS]

    # PALETTES par défaut (Brand & UI) — vide mais structure prête
    palettes = []
    for vn, vs in zip(variants["name"], variants["slug"]):
        palettes.append({"name":"Brand","slug": slugify(f"{vs}-brand"), "variant_ref_name": vn, "role":"Brand", "notes_text":""})
        palettes.append({"name":"UI","slug": slugify(f"{vs}-ui"), "variant_ref_name": vn, "role":"UI", "notes_text":""})
    palettes = pd.DataFrame(palettes)[PALETTE_COLS]

    # COULEURS (aucune par défaut — tu peux importer plus tard sans casser le schéma)
    couleurs = pd.DataFrame(columns=COULEUR_COLS)

    return styles, variants, palettes, couleurs
