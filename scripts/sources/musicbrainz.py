import musicbrainzngs as mb

def init():
    mb.set_useragent("ArtceptionExtractor", "1.0", "https://github.com/you/repo")

def top_artists_by_tag(tag="minimal", limit=30):
    res = mb.search_artists(tag=tag, limit=limit)
    items = res.get("artist-list", [])
    out = []
    for a in items:
        out.append({
            "mbid": a.get("id"),
            "name": a.get("name"),
            "country": a.get("country"),
            "score": a.get("ext:score"),
        })
    return out
