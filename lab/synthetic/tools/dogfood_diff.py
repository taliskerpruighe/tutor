#!/usr/bin/env python3
"""dogfood_diff.py — the scripted fact-level diff (BUILD-PLAN §6 layer 4).

Compares a solver's packet against the answer key on the two things the gate
actually measures: the DOCUMENT SET (with its conditional triggers) and the
LOCKED FACTS. Formatting is explicitly graded by eye, not byte, so nothing here
compares layout.

    python3 dogfood_diff.py <slug>
"""
import os, re, sys, glob, subprocess
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def text_of(pdf):
    return subprocess.run(["pdftotext", "-layout", pdf, "-"],
                          capture_output=True, text=True).stdout

def doc_list(outdir):
    """The DOCUMENT set, read off the component file names."""
    docs = {}
    for p in glob.glob(os.path.join(outdir, "**", "*.pdf"), recursive=True):
        b = os.path.basename(p)
        m = re.match(r"^([AB])-(\d+)\.\s+(.+)\.pdf$", b)
        if m:
            docs[int(m.group(2))] = m.group(3).strip()
    return docs

def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "stavros_daphne"
    key = os.path.join(ROOT, "answer-keys", slug, "output")
    sol = os.path.join(ROOT, "dogfood", slug, "output")
    if not os.path.isdir(key): sys.exit(f"no answer key at {key}")
    if not os.path.isdir(sol): sys.exit(f"no solver packet at {sol}")
    mk = yaml.safe_load(open(os.path.join(ROOT, "clients", slug, "masterkey.norm.yaml")))

    fails, oks = [], []
    kd, sd = doc_list(key), doc_list(sol)
    print(f"answer key : {len(kd)} documents")
    print(f"solver     : {len(sd)} documents\n")
    for n in sorted(set(kd) | set(sd)):
        k, s = kd.get(n), sd.get(n)
        if k and s and norm(k) == norm(s):
            oks.append(f"DOC {n}: {k}")
        elif k and s:
            oks.append(f"DOC {n}: key={k!r} solver={s!r} (same slot, different title)")
        elif k:
            fails.append(f"DOC {n} MISSING from solver: {k}")
        else:
            fails.append(f"DOC {n} EXTRA in solver: {s}")

    # locked facts, checked in the solver's merged packet text
    merged = os.path.join(sol, "N-400 Packet.pdf")
    body = text_of(merged) if os.path.exists(merged) else "\n".join(
        text_of(p) for p in glob.glob(os.path.join(sol, "**", "*.pdf"), recursive=True))
    nb = norm(body)
    ident, imm = mk.get("identity") or {}, mk.get("immigration") or {}
    pp = (mk.get("documents") or {}).get("applicant_passport") or {}
    checks = {
        "family name": ident.get("family_name"),
        "given name": ident.get("given_name"),
        "A-number": imm.get("a_number"),
        "passport number": pp.get("passport_number") or pp.get("number"),
        "classification basis": imm.get("classification_basis_string"),
    }
    for label, val in checks.items():
        if val in (None, ""): continue
        (oks if norm(val) in nb else fails).append(
            f"fact {label} = {val!r}: {'present' if norm(val) in nb else 'ABSENT'}")

    print("\n".join("  [ok]   " + o for o in oks))
    if fails:
        print("\n".join("  [FAIL] " + f for f in fails))
        print(f"\n=== DOGFOOD DIFF: {len(fails)} mismatch(es) ===")
        sys.exit(1)
    print(f"\n=== DOGFOOD DIFF GREEN: document set and locked facts match ===")

if __name__ == "__main__":
    main()
