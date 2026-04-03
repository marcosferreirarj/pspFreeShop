#!/usr/bin/env python3
"""
rename_covers.py
Fuzzy-matches cover filenames in CoversCompressed/ against psp_games.tsv
and renames them to [TitleID]-NN.ext format.
Generates mapping_report.txt with full results.
"""

import re
import sys
import csv
import unicodedata
from pathlib import Path
from thefuzz import process, fuzz

# ── Config ────────────────────────────────────────────────────────────────────
COVERS_DIR   = Path("c:/estudos/psp/CoversCompressed")
TSV_FILE     = Path("c:/estudos/psp/psp_games.tsv")
REPORT_FILE  = Path("c:/estudos/psp/mapping_report.txt")
FUZZY_CUTOFF = 82   # minimum score (0-100)
DRY_RUN      = False

# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    text = text.replace("_", " ").replace(":", " ")
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def strip_cover_suffix(stem: str) -> str:
    """Remove trailing -01 / -02 from the stem (cover sequence number)."""
    return re.sub(r"\s*-\d+$", "", stem)


def extract_year(text: str):
    """Return the last 4-digit year found in text, or None."""
    m = re.findall(r"\b(19|20)\d{2}\b", text)
    return m[-1] if m else None


def year_penalty(cover_name: str, tsv_name: str) -> int:
    """Return a score penalty when cover has a year but TSV has a different year."""
    cy = extract_year(cover_name)
    ty = extract_year(tsv_name)
    if cy and ty and cy != ty:
        return 30   # big penalty for mismatched years
    if cy and not ty:
        return 10   # small penalty: cover has year, TSV doesn't
    return 0


def load_tsv(path: Path):
    """Return list of (title_id, name, norm_name) from TSV, PSP only."""
    games = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            tid  = row["Title ID"].strip()
            name = row["Name"].strip()
            game_type = row.get("Type", "").strip()
            if tid and name and game_type == "PSP":
                games.append((tid, name, normalize(name)))
    return games


def preferred_tid(candidates: list[tuple]) -> tuple:
    """From a list of (tid, name) pick the preferred region."""
    order = ("UCUS", "ULUS", "ULES", "NPUG", "NPUE", "UCAS", "ULJM")
    for prefix in order:
        for c in candidates:
            if c[0].startswith(prefix):
                return c
    return candidates[0]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    games = load_tsv(TSV_FILE)

    # Build dedup corpus: normalized_name → [(tid, original_name), ...]
    norm_to_games: dict[str, list[tuple]] = {}
    for tid, name, norm in games:
        norm_to_games.setdefault(norm, []).append((tid, name))

    corpus = list(norm_to_games.keys())

    cover_files = sorted(COVERS_DIR.iterdir())

    # ── Phase 1: score every file ────────────────────────────────────────────
    # result_map: fpath → (new_path, tid, tsv_name, score) | None
    result_map: dict[Path, tuple | None] = {}

    for fpath in cover_files:
        if not fpath.is_file():
            continue

        stem     = fpath.stem
        suffix_m = re.search(r"-(\d+)$", stem)
        seq      = suffix_m.group(1) if suffix_m else "01"
        game_stem = strip_cover_suffix(stem)
        norm_stem = normalize(game_stem)

        candidates = process.extractBests(
            norm_stem, corpus,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=FUZZY_CUTOFF,
            limit=5,
        )

        if not candidates:
            result_map[fpath] = None
            continue

        # Apply year penalty to each candidate
        best_norm, best_score, *_ = max(
            ((n, s - year_penalty(game_stem, n)) for n, s in candidates),
            key=lambda x: x[1],
        )

        if best_score < FUZZY_CUTOFF:
            result_map[fpath] = None
            continue

        tsv_candidates = norm_to_games[best_norm]
        chosen_tid, chosen_name = preferred_tid(tsv_candidates)

        ext      = fpath.suffix.lower()
        new_name = f"{chosen_tid}-{seq}{ext}"
        new_path = COVERS_DIR / new_name
        result_map[fpath] = (new_path, chosen_tid, chosen_name, best_score)

    # ── Phase 2: resolve target collisions ───────────────────────────────────
    # If two DIFFERENT source stems map to the same target path, keep the one
    # with the higher score; mark the lower-score ones as collisions.
    target_to_sources: dict[str, list[tuple]] = {}
    for fpath, info in result_map.items():
        if info is None:
            continue
        new_path, tid, name, score = info
        target_to_sources.setdefault(str(new_path), []).append((score, fpath, tid, name))

    # For each target, sort by score desc; first entry wins, rest are collisions
    collision_files: set[Path] = set()
    for target, entries in target_to_sources.items():
        entries.sort(key=lambda x: x[0], reverse=True)
        # The best-scoring entry keeps the target
        for _, fpath, _, _ in entries[1:]:
            collision_files.add(fpath)

    # ── Phase 3: rename ───────────────────────────────────────────────────────
    renamed, skipped_collision, unmatched = [], [], []
    for fpath in cover_files:
        if not fpath.is_file():
            continue
        info = result_map.get(fpath)
        if info is None:
            unmatched.append(fpath)
            continue
        new_path, tid, name, score = info
        if fpath in collision_files:
            skipped_collision.append((fpath, new_path, tid, name, score))
            continue
        if fpath == new_path:
            renamed.append((fpath, new_path, tid, name, score, "ALREADY_NAMED"))
        elif new_path.exists():
            skipped_collision.append((fpath, new_path, tid, name, score))
        else:
            if not DRY_RUN:
                fpath.rename(new_path)
            renamed.append((fpath, new_path, tid, name, score, "DRY" if DRY_RUN else "OK"))

    # ── Phase 4: report ───────────────────────────────────────────────────────
    lines = []
    lines.append("=" * 72)
    lines.append("  COVER MAPPING REPORT")
    lines.append(f"  DRY_RUN = {DRY_RUN}  |  FUZZY_CUTOFF = {FUZZY_CUTOFF}")
    lines.append("=" * 72)
    lines.append(f"\nTotal cover files      : {sum(1 for f in cover_files if f.is_file())}")
    lines.append(f"Renamed (or dry-run)   : {len(renamed)}")
    lines.append(f"Skipped (collision)    : {len(skipped_collision)}")
    lines.append(f"Unmatched              : {len(unmatched)}")

    lines.append("\n" + "─" * 72)
    lines.append("RENAMED FILES")
    lines.append("─" * 72)
    for orig, new, tid, tsv_name, score, status in renamed:
        lines.append(f"[{status}] score={score:3d}  {orig.name}")
        lines.append(f"         → {new.name}  ({tsv_name}  {tid})")

    if skipped_collision:
        lines.append("\n" + "─" * 72)
        lines.append("SKIPPED — COLLISIONS (lower-score duplicate targets)")
        lines.append("─" * 72)
        for orig, new, tid, tsv_name, score in skipped_collision:
            lines.append(f"  score={score:3d}  {orig.name}  →  {new.name}  [{tsv_name} / {tid}]")

    if unmatched:
        lines.append("\n" + "─" * 72)
        lines.append(f"UNMATCHED FILES ({len(unmatched)} — not found in TSV above cutoff {FUZZY_CUTOFF})")
        lines.append("─" * 72)
        for fpath in unmatched:
            lines.append(f"  {fpath.name}")

    report = "\n".join(lines) + "\n"
    REPORT_FILE.write_text(report, encoding="utf-8")
    sys.stdout.buffer.write(report.encode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
