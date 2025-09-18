CORE_CATEGORIES_COLS = [
    "name","slug","icon_img_url","accent_hex"
]

CORE_STYLES_COLS = [
    "name","slug","qid","era_from","era_to","origin",
    "summary_rte","principles_rte","mood_tags_text",
    "cover_img_url","sources_text","extra_json"
]

# Commun à tous les Variants (chaque collection aura en plus ses champs spécifiques)
VARIANT_BASE_COLS = [
    "name","slug","style_ref_name","category_ref_name",
    "intro_rte","gallery_urls_text","featured","order",
    "sources_text","extra_json"
]

# Spécifiques par catégorie
GRAPHISME_COLS = VARIANT_BASE_COLS + [
    "use_cases","shapes_motifs_rte","web_tokens_json"
]
ARCHITECTURE_COLS = VARIANT_BASE_COLS + [
    "materials_text","geometry_opts","facade_pattern","voids_solids_ratio"
]
MUSIQUE_COLS = VARIANT_BASE_COLS + [
    "bpm_min","bpm_max","tonalities","instruments_text","playlist_embed"
]
CINEMA_COLS = VARIANT_BASE_COLS + [
    "movements_text","shot_techniques","aspect_ratios","lut_notes_rte"
]
PHOTO_COLS = VARIANT_BASE_COLS + [
    "processes_text","lenses_text","light_schemes_text"
]
MODE_COLS = VARIANT_BASE_COLS + [
    "silhouettes_text","fabrics_text","patterns_text"
]
DESIGN_COLS = VARIANT_BASE_COLS + [
    "object_types_text","manufacturing_text","ergo_notes_rte"
]
PEINTURE_COLS = VARIANT_BASE_COLS + [
    "techniques_text","supports_text"
]
CUISINE_COLS = VARIANT_BASE_COLS + [
    "regions_text","techniques_text","flavor_profile_opts"
]

# Enfants Graphisme
PALETTE_COLS = [
    "name","slug","variant_ref_name","role","notes_text"
]

COULEUR_COLS = [
    "name","slug","palette_ref_name","hex","hex_2","is_gradient","gradient_angle",
    "contrast_on_light","contrast_on_dark","usage_tags_text","order"
]

TYPEFACE_COLS = [
    "name","slug","foundry","link_url","is_variable"
]

FONT_PAIRING_COLS = [
    "name","variant_ref_name","typeface_ref_name","role","weights_text","notes"
]

# Works & Person
WORK_COLS = [
    "name","slug","year","thumb_img_url","type_opts",
    "persons_names_text","ext_ids_text","source_url"
]

VARIANT_WORK_COLS = [
    "name","variant_ref_name","work_ref_name","role"
]

PERSON_COLS = [
    "name","slug","role_opts","bio_short","links_text","portrait_img_url"
]
