from slugify import slugify as _slugify

def slugify(s: str, maxlen: int = 80) -> str:
    if not s:
        return ""
    return _slugify(str(s))[:maxlen]

def ensure_cols(df, cols):
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]

CATEGORIES = [
    ("Graphisme", "graphisme"),
    ("Musique", "musique"),
    ("Architecture", "architecture"),
    ("Cinéma", "cinema"),
    ("Photo", "photo"),
    ("Mode", "mode"),
    ("Design", "design"),
    ("Peinture", "peinture"),
    ("Cuisine", "cuisine"),
]
