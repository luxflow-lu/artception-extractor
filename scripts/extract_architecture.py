from pathlib import Path
import pandas as pd
from scripts.sources.wikidata import sparql, architectural_styles_query
from scripts.utils import slugify
from scripts.model import CORE_STYLES_COLS, ARCHITECTURE_COLS

def run(lang="fr,en", limit=200, outdir=Path("out/csv/architecture")):
    outdir.mkdir(parents=True, exist_ok=True)

    seed = pd.read_csv("data/seeds/styles_core.csv")
    seed = seed[seed["categories"].str.contains("Architecture", case=False, na=False)].copy()

    df = sparql(architectural_styles_query(limit=limit), lang=lang)
    if df.empty:
        df = pd.DataFrame(columns=["style","styleLabel","start","end","image"])
    df["qid"] = df["style"].str.rsplit("/", n=1).str[-1]
    df.rename(columns={"styleLabel":"name","image":"cover_img_url"}, inplace=True)

    seed_basic = seed[["qid","style","era_from","era_to","origin"]].rename(columns={"style":"seed_name"})
    core = df.merge(seed_basic, on="qid", how="left")

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

    variants = pd.DataFrame({
        "name": styles["name"] + " — Architecture",
        "slug": styles["slug"] + "-architecture",
        "style_ref_name": styles["name"],
        "category_ref_name": "Architecture",
        "intro_rte": "",
        "gallery_urls_text": "",
        "featured": "",
        "order": "",
        "sources_text": "",
        "extra_json": "",
        "materials_text": "",
        "geometry_opts": "Orthogonal",
        "facade_pattern": "",
        "voids_solids_ratio": ""
    })[ARCHITECTURE_COLS]

    return styles, variants
