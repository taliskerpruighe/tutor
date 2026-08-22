#!/usr/bin/env python3
"""fabricate_ids.py — identity-document exhibits: passports and the I-551.

Contract: RENDER-CONTRACT.md. Owns doc["id"] in HANDLES below (§7).

RENDER-CONTRACT §0.1/§0.4/§6 apply: no firm identity, no bare divider, no
datetime.now(), byte-identical output for identical input.

Field-name landmine (not in the contract prose, found by reading the actual
masterkeys): `normalize_masterkeys.py` only renames the top-level
`documents.*` alias (`passport` -> `applicant_passport`); it does NOT touch
the field spellings *inside* each document block. `almeida_paulo` spells its
applicant passport number `number`, `tran_daniel` spells the same fact
`passport_number` — both are required test clients. `_pick()` below resolves
a closed, explicit alias list per fact and raises loudly on a miss, per
RENDER-CONTRACT §7 ("a fact you need that is not in the masterkey is a
masterkey bug — report it, do not invent the value"). The alias lists are
deliberately closed: e.g. the A-number never falls through to a `card_number`
or `uscis_hash_number` key, both of which are card SERIAL numbers on at least
one real client (`nowak_agata` carries both a genuine `a_number` and a decoy
`uscis_hash_number` that looks like a USCIS# but is not one).
"""
from __future__ import annotations

import hashlib
import io
import os

import mklib

HANDLES = {"applicant_passport", "spouse_passport", "child_passport", "green_card"}

# ID-1 card size (a physical green card / driving-licence sized card), in points.
CARD_W = 3.370 * 72.0
CARD_H = 2.125 * 72.0

MRZ_FONT = "Courier"
MRZ_FONT_BOLD = "Courier-Bold"


# =====================================================================
# field alias resolution — closed lists only, raise loudly on a miss
# =====================================================================
def _pick(d: dict, keys: tuple, ctx: str):
    for k in keys:
        v = d.get(k)
        if v not in (None, ""):
            return v
    raise KeyError(f"{ctx}: none of {keys} present (have {sorted(d.keys())})")


def _passport_facts(pp: dict, ctx: str) -> dict:
    return {
        "passport_number": _pick(pp, ("passport_number", "number"), ctx),
        "surname": _pick(pp, ("surname_printed", "surname"), ctx),
        "given_names": _pick(pp, ("given_names_printed", "given_names"), ctx),
        "issuing_country": _pick(pp, ("issuing_country", "country"), ctx),
        "place_of_birth": _pick(pp, ("place_of_birth", "pob"), ctx),
        "nationality": _pick(pp, ("nationality",), ctx),
        "dob": _pick(pp, ("dob",), ctx),
        "sex": _pick(pp, ("sex",), ctx),
        "issue_date": _pick(pp, ("issue_date",), ctx),
        "expiry_date": _pick(pp, ("expiry_date",), ctx),
        "issuing_authority": _pick(pp, ("issuing_authority",), ctx),
        "mrz_line1": _pick(pp.get("mrz") or {}, ("line1",), ctx + ".mrz"),
        "mrz_line2": _pick(pp.get("mrz") or {}, ("line2",), ctx + ".mrz"),
    }


def _green_card_facts(gc: dict, ctx: str) -> dict:
    return {
        "surname": _pick(gc, ("surname_printed", "surname"), ctx),
        "given_name": _pick(gc, ("given_name_printed", "given_name"), ctx),
        # Closed list. Never card_number / card_number_back / uscis_hash_number
        # — those are card SERIAL numbers, not the USCIS A-number, and at
        # least one client (nowak_agata) carries both to make that trap real.
        "a_number": _pick(gc, ("a_number", "uscis_number"), ctx),
        "category": _pick(gc, ("category", "category_class_of_admission"), ctx),
        "country_of_birth": _pick(gc, ("country_of_birth", "cob"), ctx),
        "dob": _pick(gc, ("dob",), ctx),
        "sex": _pick(gc, ("sex",), ctx),
        "card_expiry": _pick(gc, ("card_expiry", "card_expires", "expires"), ctx),
        "resident_since": _pick(gc, ("resident_since",), ctx),
    }


_DOC_KEY = {
    "applicant_passport": "applicant_passport",
    "spouse_passport": "spouse_passport",
    "child_passport": "child_passport",
    "green_card": "green_card",
}


def _mk_slug(mk: dict) -> str:
    # matter.slug is not guaranteed; fall back to the applicant's SSN-free
    # full legal name, which is stable per masterkey and never touches the
    # filesystem — this is only used to seed cosmetic, non-content noise.
    m = mk.get("matter") or {}
    return str(m.get("slug") or mklib.full_legal_name(mk))


def _noise_bytes(slug: str, doc_id: str, n: int = 32) -> bytes:
    """Deterministic noise source for the photo finish. No random, no hash()."""
    return hashlib.sha256(f"{slug}::{doc_id}".encode("utf-8")).digest()[:n]


# =====================================================================
# PIL artwork helpers — background/portrait/texture ONLY; all data is text
# =====================================================================
def _portrait_placeholder(w_px: int, h_px: int) -> "object":
    """A generic silhouette placeholder. No real photo exists for a synthetic
    client, so this is deliberately abstract furniture, never invented facial
    data."""
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (w_px, h_px), (222, 224, 227))
    d = ImageDraw.Draw(img)
    cx, cy = w_px // 2, int(h_px * 0.38)
    r = int(w_px * 0.28)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(178, 182, 188))
    d.ellipse((int(w_px * 0.08), int(h_px * 0.72),
               int(w_px * 0.92), int(h_px * 1.35)), fill=(178, 182, 188))
    d.rectangle((0, 0, w_px - 1, h_px - 1), outline=(150, 150, 150), width=2)
    return img


def _tint_bg(w_px: int, h_px: int, rgb: tuple) -> "object":
    from PIL import Image
    return Image.new("RGB", (w_px, h_px), rgb)


def _pil_to_reader(img) -> "object":
    from reportlab.lib.utils import ImageReader
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def _apply_photo_finish(img, seed: bytes) -> "object":
    """Modest phone-photo look: desk-toned backdrop the page sits on, a small
    rotation and a mild perspective warp, a soft shadow, JPEG recompression.
    Deterministic: every parameter is arithmetic on `seed`, never `random`.
    """
    from PIL import Image, ImageFilter

    b = seed
    angle = ((b[0] / 255.0) - 0.5) * 6.0            # +/- 3 degrees
    dx = int(((b[1] / 255.0) - 0.5) * 10)            # small perspective jitter
    dy = int(((b[2] / 255.0) - 0.5) * 10)

    w, h = img.size
    pad = max(w, h) // 6
    desk = Image.new("RGB", (w + 2 * pad, h + 2 * pad), (86, 74, 61))
    # subtle desk-toned gradient, computed arithmetically (no randomness)
    px = desk.load()
    for y in range(0, desk.size[1], 4):
        shade = 70 + int(24 * (y / desk.size[1]))
        for x in range(0, desk.size[0], 4):
            px[x, y] = (shade + 10, shade, shade - 10)

    card = img.convert("RGB")
    # mild perspective: shift the four corners by (dx, dy)-derived offsets
    coeffs = _perspective_coeffs(card.size, dx, dy)
    card = card.transform(card.size, Image.PERSPECTIVE, coeffs,
                          resample=Image.BICUBIC, fillcolor=(255, 255, 255))
    card = card.rotate(angle, resample=Image.BICUBIC, expand=True,
                       fillcolor=(255, 255, 255))

    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    shadow_layer = Image.new("L", card.size, 60)
    shadow.putalpha(shadow_layer)
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))

    ox = pad + (desk.size[0] - card.size[0]) // 2
    oy = pad + (desk.size[1] - card.size[1]) // 2
    desk.paste((0, 0, 0), (ox + 4, oy + 6, ox + 4 + card.size[0], oy + 6 + card.size[1]))
    desk.paste(card, (ox, oy))
    return desk


def _perspective_coeffs(size, dx, dy):
    w, h = size
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    dst = [(0, 0), (w - dx, dy), (w - dx, h - dy), (dx, h)]
    return _find_coeffs(dst, src)


def _find_coeffs(pa, pb):
    # Standard 8-coefficient perspective solve without external deps.
    a = []
    for (x, y), (X, Y) in zip(pa, pb):
        a.append([x, y, 1, 0, 0, 0, -X * x, -X * y])
        a.append([0, 0, 0, x, y, 1, -Y * x, -Y * y])
    bvec = []
    for (X, Y) in pb:
        bvec.append(X)
        bvec.append(Y)
    # Solve the 8x8 linear system with plain Gaussian elimination (no numpy
    # dependency, fully deterministic).
    return _solve_linear(a, bvec)


def _solve_linear(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        pv = m[col][col]
        if pv == 0:
            continue
        for j in range(col, n + 1):
            m[col][j] /= pv
        for r in range(n):
            if r != col:
                factor = m[r][col]
                for j in range(col, n + 1):
                    m[r][j] -= factor * m[col][j]
    return [m[i][n] for i in range(n)]


# =====================================================================
# passport bio page
# =====================================================================
def _draw_passport(mk: dict, doc_id: str, outpath: str, finish: str) -> str:
    ctx = f"documents.{_DOC_KEY[doc_id]}"
    pp = (mk.get("documents") or {}).get(_DOC_KEY[doc_id])
    if not pp:
        raise KeyError(f"{ctx} missing from masterkey")
    f = _passport_facts(pp, ctx)

    problems = mklib.mrz_verify(f["mrz_line1"], f["mrz_line2"])
    if problems:
        raise ValueError(f"{ctx}.mrz fails validation: {problems}")

    c = mklib.new_canvas(outpath)

    page_bg_rgb = (245, 245, 245) if finish == "scan" else (255, 255, 255)
    slug = _mk_slug(mk)
    seed = _noise_bytes(slug, doc_id)

    # Full printable width so the longest field value (issuing authority)
    # never runs past the drawn border — verified against every client's
    # longest authority string, not just the two required test clients.
    biopage_w_pt = mklib.PAGE_W - 2 * mklib.MARGIN
    biopage_h_pt = 4.0 * 72.0
    bio_img = _tint_bg(int(biopage_w_pt), int(biopage_h_pt), (250, 249, 244))
    if finish == "photo":
        bio_img = _apply_photo_finish(bio_img, seed)
        img_w_pt = biopage_w_pt * (bio_img.size[0] / int(biopage_w_pt))
        img_h_pt = biopage_h_pt * (bio_img.size[1] / int(biopage_h_pt))
    else:
        img_w_pt, img_h_pt = biopage_w_pt, biopage_h_pt

    # page background — a very slight grey field for the "scan", per spec.
    c.setFillColorRGB(*[v / 255.0 for v in page_bg_rgb])
    c.rect(0, 0, mklib.PAGE_W, mklib.PAGE_H, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)

    x0 = (mklib.PAGE_W - img_w_pt) / 2.0
    y0 = mklib.PAGE_H - mklib.MARGIN - img_h_pt - 40
    c.drawImage(_pil_to_reader(bio_img), x0, y0, width=img_w_pt, height=img_h_pt,
               preserveAspectRatio=False, mask="auto")
    c.setLineWidth(1)
    c.rect(x0, y0, img_w_pt, img_h_pt, stroke=1, fill=0)

    mklib.frame_text(
        c, [("PASSPORT — BIOGRAPHIC DATA PAGE", {"bold": True, "size": 14})],
        align="center", top=mklib.PAGE_H - mklib.MARGIN)

    # portrait box, upper-left of the bio page image
    photo_w, photo_h = 1.2 * 72.0, 1.5 * 72.0
    photo = _portrait_placeholder(int(photo_w), int(photo_h))
    px, py = x0 + 14, y0 + img_h_pt - photo_h - 14
    c.drawImage(_pil_to_reader(photo), px, py, width=photo_w, height=photo_h)
    c.rect(px, py, photo_w, photo_h, stroke=1, fill=0)

    label_x = px + photo_w + 20
    label_top = y0 + img_h_pt - 24
    rows = [
        # MRZ-consistent: the "Code" half is the 3-letter issuing-state code
        # that line 1 of the MRZ actually carries, not the country's full
        # name (which is shown separately, below, and in the caption).
        ("Type / Code", f"P / {f['nationality']}"),
        ("Passport No.", f["passport_number"]),
        ("Surname", f["surname"]),
        ("Given Names", f["given_names"]),
        ("Nationality", f["nationality"]),
        ("Date of Birth", mklib.fmt_numeric(f["dob"])),
        ("Sex", f["sex"]),
        ("Place of Birth", f["place_of_birth"]),
        ("Date of Issue", mklib.fmt_numeric(f["issue_date"])),
        ("Date of Expiry", mklib.fmt_numeric(f["expiry_date"])),
        ("Authority", f["issuing_authority"]),
    ]
    yy = label_top
    lh = 15.0
    for label, value in rows:
        c.setFont(mklib.BODY_FONT_BOLD, 8)
        c.drawString(label_x, yy, f"{label}:")
        c.setFont(mklib.BODY_FONT, 9.5)
        c.drawString(label_x + 78, yy, str(value))
        yy -= lh
        if yy < y0 + 12:
            break

    mrz_y = y0 + 14
    c.setFont(MRZ_FONT, 10)
    c.drawString(x0 + 14, mrz_y + 13, f["mrz_line1"])
    c.drawString(x0 + 14, mrz_y, f["mrz_line2"])

    caption_y = y0 - 16
    mklib.frame_text(
        c, [f"Issuing Country: {f['issuing_country']}  |  "
            f"Passport No.: {f['passport_number']}"],
        align="center", top=caption_y, size=9)

    c.showPage()
    c.save()
    return outpath


# =====================================================================
# green card — Form I-551, front and back, one page
# =====================================================================
def _draw_card_face(c, x, y, facts, face: str, finish: str, seed: bytes):
    # 26pt header leaves a clean 10pt gap between the title and subtitle
    # baselines at these font sizes — a 20pt header let the two collide.
    header_h = 26.0
    c.setFillColorRGB(0.80, 0.86, 0.93)
    c.rect(x, y, CARD_W, CARD_H, stroke=0, fill=1)
    c.setFillColorRGB(0.55, 0.68, 0.80)
    c.rect(x, y + CARD_H - header_h, CARD_W, header_h, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    c.setLineWidth(1.2)
    c.rect(x, y, CARD_W, CARD_H, stroke=1, fill=0)

    c.setFont(mklib.BODY_FONT_BOLD, 8.0)
    c.drawCentredString(x + CARD_W / 2.0, y + CARD_H - 11,
                        "PERMANENT RESIDENT CARD")
    c.setFont(mklib.BODY_FONT, 6.0)
    c.drawCentredString(x + CARD_W / 2.0, y + CARD_H - header_h + 5,
                        "United States of America")

    if face == "front":
        photo_w, photo_h = 0.75 * 72.0, 0.95 * 72.0
        photo = _portrait_placeholder(int(photo_w), int(photo_h))
        px, py = x + 8, y + CARD_H - header_h - photo_h - 8
        c.drawImage(_pil_to_reader(photo), px, py, width=photo_w, height=photo_h)
        c.rect(px, py, photo_w, photo_h, stroke=1, fill=0)

        rows = [
            ("Surname", facts["surname"]),
            ("Given Name", facts["given_name"]),
            ("USCIS#", facts["a_number"]),
            ("Category", facts["category"]),
            ("Country of Birth", facts["country_of_birth"]),
            ("Date of Birth", mklib.fmt_numeric(facts["dob"])),
            ("Sex", facts["sex"]),
            ("Card Expires", mklib.fmt_numeric(facts["card_expiry"])),
        ]
        # 8 rows x 14.0pt pitch + 8pt top offset = 120pt, inside the 127pt
        # content height (CARD_H - header_h) with margin at the bottom edge.
        tx = px + photo_w + 8
        ty = y + CARD_H - header_h - 8
        for label, value in rows:
            c.setFont(mklib.BODY_FONT_BOLD, 5.4)
            c.drawString(tx, ty, f"{label}:")
            c.setFont(mklib.BODY_FONT, 6.2)
            c.drawString(tx, ty - 6.2, str(value))
            ty -= 14.0
    else:
        c.setFont(mklib.BODY_FONT_BOLD, 6.2)
        c.drawString(x + 10, y + CARD_H - header_h - 14, "Resident Since:")
        c.setFont(mklib.BODY_FONT, 7.2)
        c.drawString(x + 10, y + CARD_H - header_h - 24,
                    mklib.fmt_numeric(facts["resident_since"]))

        c.setFont(mklib.BODY_FONT_BOLD, 6.2)
        c.drawString(x + 10, y + CARD_H - header_h - 42, "USCIS#:")
        c.setFont(mklib.BODY_FONT, 7.2)
        c.drawString(x + 10, y + CARD_H - header_h - 52, facts["a_number"])

        c.setFont(mklib.BODY_FONT, 5.6)
        c.drawString(x + 10, y + 14,
                    "This card is the property of the U.S. Department of "
                    "Homeland Security.")


def _draw_green_card(mk: dict, outpath: str, finish: str) -> str:
    ctx = "documents.green_card"
    gc = (mk.get("documents") or {}).get("green_card")
    if not gc:
        raise KeyError(f"{ctx} missing from masterkey")
    facts = _green_card_facts(gc, ctx)

    c = mklib.new_canvas(outpath)
    page_bg_rgb = (245, 245, 245) if finish == "scan" else (255, 255, 255)
    c.setFillColorRGB(*[v / 255.0 for v in page_bg_rgb])
    c.rect(0, 0, mklib.PAGE_W, mklib.PAGE_H, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)

    mklib.frame_text(
        c, [("FORM I-551, PERMANENT RESIDENT CARD — FRONT AND BACK",
             {"bold": True, "size": 13})],
        align="center", top=mklib.PAGE_H - mklib.MARGIN)

    x = (mklib.PAGE_W - CARD_W) / 2.0
    y_front = mklib.PAGE_H - mklib.MARGIN - 60 - CARD_H
    y_back = y_front - 40 - CARD_H

    seed = _noise_bytes(_mk_slug(mk), "green_card")
    _draw_card_face(c, x, y_front, facts, "front", finish, seed)
    mklib.frame_text(c, ["Front"], align="center", top=y_front - 14, size=8)
    _draw_card_face(c, x, y_back, facts, "back", finish, seed)
    mklib.frame_text(c, ["Back"], align="center", top=y_back - 14, size=8)

    c.showPage()
    c.save()
    return outpath


# =====================================================================
# public API
# =====================================================================
def fabricate(masterkey: dict, which: str, outpath: str, finish: str = "scan") -> str:
    """Render ONE identity exhibit to `outpath`. Callable directly by Phase 4.

    which  -- "applicant_passport" | "spouse_passport" | "child_passport"
              | "green_card"
    finish -- "scan" (default; every OUTPUT packet) or "photo" (Phase 4
              INPUT-side synthesis for phone-photo clients only).
    Returns the absolute path written.
    """
    if which not in HANDLES:
        raise ValueError(f"fabricate_ids.py does not handle {which!r}; "
                         f"HANDLES = {sorted(HANDLES)}")
    if finish not in ("scan", "photo"):
        raise ValueError(f"finish must be 'scan' or 'photo', got {finish!r}")
    outpath = os.path.abspath(outpath)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    if which == "green_card":
        result = _draw_green_card(masterkey, outpath, finish)
    else:
        result = _draw_passport(masterkey, which, outpath, finish)
    # RENDER-CONTRACT §6: every component carries the house /CreationDate and
    # /Producer. reportlab's invariant=1 (mklib.new_canvas) already gives
    # byte-identical output across re-renders, but only stamping gives the
    # house metadata. This renderer previously skipped it (see
    # render_evidence.py's _finish() history comment for why that omission
    # was once load-bearing); mklib.stamp_deterministic is fixed now, so
    # re-enable it here too.
    mklib.stamp_deterministic(result)
    return result


def render(masterkey: dict, outdir: str, doc: dict) -> list:
    """RENDER-CONTRACT §1. One DOCUMENT per call; PDF only (§4.3, exhibit)."""
    if doc["id"] not in HANDLES:
        raise ValueError(f"fabricate_ids.py does not handle {doc['id']!r}; "
                         f"HANDLES = {sorted(HANDLES)}")
    outpath = mklib.component_path(outdir, doc, "pdf")
    fabricate(masterkey, doc["id"], outpath, finish="scan")
    return [outpath]


if __name__ == "__main__":
    import sys
    slug = sys.argv[1] if len(sys.argv) > 1 else "almeida_paulo"
    mk = mklib.load_masterkey(slug)
    outdir = mklib.ensure_outdir(os.path.join(mklib.CLIENTS, slug, "output"))
    for d in mklib.doc_entries(mk):
        if d["id"] in HANDLES:
            paths = render(mk, outdir, d)
            print(d["id"], "->", paths)
