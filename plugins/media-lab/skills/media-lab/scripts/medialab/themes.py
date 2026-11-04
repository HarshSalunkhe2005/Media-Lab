"""Themes: the drawable half of each world (src/worlds.ts holds the taste rules).

A theme is fonts + colours + one surface treatment. Keep ids in step with src/worlds.ts;
tools/test_medialab.py fails if a world has no theme.
"""
THEMES: dict[str, dict] = {
    "quiet-poetry": dict(head="serif", body="serif", num="serif", bg="#f0ebe1", fg="#1c1a17", muted="#6d665c",
                         accent="#8a5a3b", surface="paper", case="sentence"),
    "tech-launch": dict(head="sans-bold", body="sans", num="sans-black", bg="#0e0f12", fg="#f4f5f7", muted="#9aa0aa",
                        accent="#5b8cff", surface="flat", case="sentence"),
    "campus-event": dict(head="condensed", body="sans", num="condensed", bg="#101820", fg="#ffffff", muted="#b8c2cc",
                         accent="#ffcc33", surface="photo-dark", case="upper-head"),
    "explainer": dict(head="sans-bold", body="sans", num="sans-black", bg="#f7f6f2", fg="#17181a", muted="#5d6066",
                      accent="#ff5a36", surface="flat", case="sentence"),
    "data-story": dict(head="sans-semibold", body="sans", num="sans-black", bg="#ffffff", fg="#111111", muted="#6b6b6b",
                       accent="#0057ff", surface="flat", case="sentence"),
    "build-log": dict(head="mono-bold", body="mono", num="mono-bold", bg="#16181d", fg="#e6e6e6", muted="#8b919c",
                      accent="#7ee787", surface="flat", case="lower"),
    "warm-local": dict(head="display-serif", body="sans", num="display-serif", bg="#f3e7d6", fg="#2b1d14", muted="#7a6555",
                       accent="#c2562b", surface="paper", case="sentence"),
    "faceless-story": dict(head="serif-bold", body="serif", num="serif-bold", bg="#0b0b0c", fg="#f2efe8", muted="#a39e94",
                           accent="#d9b26f", surface="photo-dark", case="sentence"),
    "editorial": dict(head="display-serif", body="serif", num="display-serif", bg="#fbfaf7", fg="#121212", muted="#6e6a64",
                      accent="#b3261e", surface="flat", case="sentence"),
    "retro-print": dict(head="display", body="sans-semibold", num="display", bg="#efe4cc", fg="#1d2a44", muted="#5a5f6b",
                        accent="#e2462f", surface="paper", case="upper-head"),
    "brutalist-mono": dict(head="sans-black", body="mono", num="sans-black", bg="#ffffff", fg="#000000", muted="#444444",
                           accent="#ff3b00", surface="flat", case="upper-head"),
    "soft-pastel": dict(head="sans-semibold", body="sans", num="sans-bold", bg="#f6efff", fg="#2a2540", muted="#6e678a",
                        accent="#7c5cff", surface="flat", case="sentence"),
}

SIZES = {"4:5": (1080, 1350), "1:1": (1080, 1080), "9:16": (1080, 1920), "16:9": (1280, 720),
         "x": (1200, 675), "linkedin": (1080, 1350), "og": (1200, 630)}


def theme(tid: str, **override) -> dict:
    if tid not in THEMES:
        raise KeyError(f"unknown theme {tid!r}; one of {', '.join(THEMES)}")
    t = dict(THEMES[tid])
    t.update({k: v for k, v in override.items() if v is not None})
    t["id"] = tid
    return t


def cased(text: str, t: dict, role: str = "head") -> str:
    c = t.get("case", "sentence")
    if c == "lower":
        return text.lower()
    if c == "upper-head" and role == "head":
        return text.upper()
    return text
