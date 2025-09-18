# Artception Extractor

Pipeline GitHub Actions + Python qui génère des CSV **compatibles Webflow** pour:
- `core/categories.csv`
- `core/styles.csv`
- `graphisme/*` (variants, palettes, couleurs, typeface, font_pairing)
- `architecture/*`
- `musique/*` (variants, person)
- `cinema/*` (variants, work, variant_work)

## Utilisation
1. Crée un secret `TMDB_API_KEY` si tu utilises `cinema`.
2. Dans l'onglet **Actions** → `Extract Artception Data` → **Run workflow** :
   - `category`: graphisme | architecture | musique | cinema | all
   - `lang`: fr,en
   - `limit`: 200 (pour tests)
3. Récupère les **Artifacts** ou récupère la branche `data`.

## Import Webflow (ordre)
1. `core/categories.csv`
2. `core/styles.csv`
3. Variants par catégorie (ex. `graphisme/graphisme_variants.csv`)
4. Enfants (ex. `graphisme/palettes.csv`, puis `graphisme/couleurs.csv`)
5. Ressources (ex. `cinema/work.csv`, `cinema/variant_work.csv`, `musique/person.csv`)
6. (Éventuels `typeface.csv`, `font_pairing.csv` si tu en ajoutes)

## Références
- Les champs `*_ref_name` font correspondre les références CMS **par le champ “Name”**.
- Chaque item a aussi un `slug` pour robustesse (utile pour déduplications).

## Notes
- `gallery_urls_text` est une simple liste d’URLs séparées par “;” (Webflow n'importe pas les Multi-Image via CSV).
- Les **palettes & couleurs** sont prêtes pour un rendu **“click to copy”** (JS côté site).
