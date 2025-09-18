from pathlib import Path
import pandas as pd
from scripts.sources.musicbrainz import init, top_artists_by_tag
from scripts.utils import slugify
from scripts.model import CORE_STYLES_COLS, MUSIQUE_COLS, PERSON_COLS

def run(lang="fr,en", limit=200, outdir=Path("out/csv/musique")):
    outdir.mkdir(parents=True, exist_ok=True)

    seed = pd.read_csv("data/seeds/styles_core.csv")
    seed = seed[seed["categories"].str.contains("Musique", case=False, na=False)].copy()

    # CORE styles depuis seed (on peut les avoir déjà : on dédupliquera plus tard)
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

    # Variants Musique
    variants = pd.DataFrame({
        "name": styles["name"] + " — Musique",
        "slug": styles["slug"] + "-musique",
        "style_ref_name": styles["name"],
        "category_ref_name": "Musique",
        "intro_rte": "",
        "gallery_urls_text": "",
        "featured": "",
        "order": "",
        "sources_text": "",
        "extra_json": "",
        "bpm_min": "",
        "bpm_max": "",
        "tonalities": "",
        "instruments_text": "",
        "playlist_embed": ""
    })[MUSIQUE_COLS]

    # Persons (artistes) depuis tags MusicBrainz
    init()
    persons_rows = []
    for _, r in seed.iterrows():
        style_name = r["style"]
        genres = [g.strip() for g in str(r.get("genres_music","")).split(";") if g.strip()]
        for tag in genres[:3]:
            artists = top_artists_by_tag(tag=tag, limit=min(30, limit))
            for a in artists:
                nm = a["name"]
                persons_rows.append({
                    "name": nm,
                    "slug": slugify(nm),
                    "role_opts": "Musicien",
                    "bio_short": "",
                    "links_text": "",
                    "portrait_img_url": ""
                })
    persons = pd.DataFrame(persons_rows).drop_duplicates(subset=["slug"])
    persons = persons.reindex(columns=PERSON_COLS).fillna("")

    return styles, variants, persons
