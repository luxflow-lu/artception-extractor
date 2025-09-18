from pathlib import Path
import pandas as pd
from scripts.sources.tmdb import search_movies
from scripts.utils import slugify
from scripts.model import CORE_STYLES_COLS, CINEMA_COLS, WORK_COLS, VARIANT_WORK_COLS

def run(lang="fr,en", limit=200, outdir=Path("out/csv/cinema")):
    outdir.mkdir(parents=True, exist_ok=True)

    seed = pd.read_csv("data/seeds/styles_core.csv")
    seed = seed[seed["categories"].str.contains("Cinéma", case=False, na=False)].copy()

    # CORE styles depuis seed
    styles = pd.DataFrame({
        "name": seed["style"],
        "slug": seed["style"].apply(lambda x: slugify(x)),
        "qid": seed["qid"],
        "era_from": seed["era_from"],
        "era_to": seed["era_to"],
        "origin": seed["origin"],
        "summary_rte": "",
        "principles_rte": "",
        "mood_tags_text": "",
        "cover_img_url": "",
        "sources_text": "",
        "extra_json": ""
    })[CORE_STYLES_COLS].drop_duplicates(subset=["slug"])

    # Variants Cinéma
    variants = pd.DataFrame({
        "name": styles["name"] + " — Cinéma",
        "slug": styles["slug"] + "-cinema",
        "style_ref_name": styles["name"],
        "category_ref_name": "Cinéma",
        "intro_rte": "",
        "gallery_urls_text": "",
        "featured": "",
        "order": "",
        "sources_text": "",
        "extra_json": "",
        "movements_text": "",
        "shot_techniques": "",
        "aspect_ratios": "",
        "lut_notes_rte": ""
    })[CINEMA_COLS]

    # Films (Work) + Variant_Work à partir de keywords_cinema & période
    works, vworks = [], []
    for _, r in seed.iterrows():
        style = r["style"]; sslug = slugify(style)
        variant_name = f"{style} — Cinéma"
        kws = [k.strip() for k in str(r.get("keywords_cinema","")).split(";") if k.strip()]
        y0, y1 = int(r.get("era_from") or 1900), int(r.get("era_to") or 2025)
        years = list(range(y0, min(y1, y0+30)+1))
        count = 0
        for kw in kws[:3]:
            for y in years:
                if count >= int(limit): break
                data = search_movies(kw, year=y, page=1)
                for m in data.get("results", [])[:5]:
                    title = m.get("title") or ""
                    wslug = slugify(f"{title}-{m.get('id')}")
                    if not title: 
                        continue
                    works.append({
                        "name": title,
                        "slug": wslug,
                        "year": (m.get("release_date","")[:4] or ""),
                        "thumb_img_url": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}" if m.get("poster_path") else "",
                        "type_opts": "Film",
                        "persons_names_text": "",
                        "ext_ids_text": f"TMDB:{m.get('id')}",
                        "source_url": f"https://www.themoviedb.org/movie/{m.get('id')}"
                    })
                    vworks.append({
                        "name": f"{variant_name} × {title}",
                        "variant_ref_name": variant_name,
                        "work_ref_name": title,
                        "role": "Exemple"
                    })
                    count += 1
                if count >= int(limit): break

    work_df = pd.DataFrame(works).drop_duplicates(subset=["slug"])
    work_df = work_df.reindex(columns=WORK_COLS).fillna("")
    vwork_df = pd.DataFrame(vworks).reindex(columns=VARIANT_WORK_COLS).fillna("")

    return styles, variants, work_df, vwork_df
