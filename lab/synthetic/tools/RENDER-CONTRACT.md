# RENDER-CONTRACT.md — the interface every renderer implements

Phase 3. Written by the toolsmith **before** any renderer, because five
renderers are built concurrently against it.

**This file is the contract. If it disagrees with your memory of STYLE-SPEC,
this file wins for interface questions and STYLE-SPEC §16 wins for content
questions.** Authority order, highest first:

1. STYLE-SPEC **§16** (the user's binding rulings) and `spec/SPEC-DELTA.md`
   (decisions D-A..D-K, already made — **do not relitigate them**).
2. `tools/n400-part-map.md` — the only authority for the N-400 Part question.
3. `templates/document-catalog.yaml` — the only authority for a document's
   file name, divider title and TOC line.
4. This file — the only authority for signatures, paths and shared helpers.
5. The rest of STYLE-SPEC.

---

## 0. THE FOUR RULES THAT FAIL THE PHASE

Read these before you write a line. Each has already been broken once by
somebody reasoning from a sensible-looking default.

### 0.1 NO FIRM IDENTITY, ANYWHERE (§16 r7, UPHELD AND EXTENDED)

No firm name, no preparer name, no business address, no firm phone, no firm
email, on **any** rendered page of **any** document. Not on the cover letter,
not on the N-400, and — this is the one that gets missed — **not on an
exhibit.** A deed has a "prepared by" line in real life. An insurance
declarations page has an agency. A court record has a filing attorney. On
these packets those lines are **absent or generic**, never a firm.

The cover letter's signature block is exactly four lines and closes on an
unattributed role (SPEC-DELTA D-B):

```
Sincerely,
<blank>
<blank>
Petition Preparer
```

The only preparer name that may appear anywhere in the build is the 1040's own
`documents.tax_return.preparer_name`, which is the *client's* tax preparer, a
third party, and is explicitly exempted (see `validate_masterkeys.py` §10).

### 0.2 THE N-400 SHIPS UNSIGNED (§16 r10, r11)

- Printed **Part 11** (the applicant's own daytime phone, mobile, email) **IS
  FILLED** — items 3, 4, 5.
- Printed **Part 11 signature and signature date: EMPTY.** No cursive
  rendering. The Z003 font is not used and is not installed as far as this
  build is concerned.
- Printed **Part 13 (preparer block): ENTIRELY EMPTY.**
- Printed Part 12 (interpreter), Part 15 and Part 16: empty.

**Never infer a Part from an AcroForm `/TU` tooltip or from a field-name
prefix.** The tooltips on this blank are stale and mislabelled and the prefixes
lag the printed Parts by no constant offset. `n400-part-map.md` gives the exact
FILL list and the exact LEAVE-EMPTY list by literal field name. Use those lists
verbatim.

### 0.3 NEVER RUN `pdfunite`, NEVER RUN OCR

`pdfunite` corrupts the AcroForm ("Can't get Fields array"). Merging is
`merge_packet.py`'s job and it uses pypdf `PdfWriter.append`; flattening is
`gs -o out.pdf -sDEVICE=pdfwrite -dPreserveAnnots=false`. No renderer merges
anything. No tool in this phase invokes `tesseract`, `ocrmypdf`, or
`build_blocklist.py`.

### 0.4 RENDERERS DO NOT CREATE DIVIDERS

A divider is the **bare numbered PDF** — `A-1.pdf`, `B-8.pdf`. Every divider
for every document is written centrally by `render_docs.py`, from
`templates/divider.yaml` joined to `document-catalog.yaml`, so that fifteen
divider titles cannot drift across five renderers.

If you are writing `render_evidence.py` and you emit `B-8.pdf` next to your
`B-8. Joint Deed.pdf`, you have silently overwritten the divider with your
exhibit and the merged packet loses a page and gains a duplicate. **Emit only
the named content file.** `render_docs.py` owns the bare number.

### 0.5 NEVER CLEAR `outdir` — IT IS SHARED

`outdir` is one folder that **nine renderers write into**. It is not your
scratch directory.

- **Do not** `shutil.rmtree(outdir)`, `os.remove` a file you did not write,
  or "start clean" in any other way. This was observed live during Phase 3:
  a fabricator recreated `clients/almeida_paulo/output/` and deleted the
  already-rendered N-400 out from under the merge.
- Write **only** the files whose names `component_path()` gives you for your
  own `doc`. Overwriting your own output on a re-run is fine and expected.
- For your own testing, pass a private `outdir` (`/tmp/<yourname>-test`), not
  the client's real output folder.

---

## 1. THE SIGNATURE — every renderer, no exceptions

```python
def render(masterkey: dict, outdir: str, doc: dict) -> list[str]:
    """Render one DOCUMENT's content component(s).

    masterkey -- the parsed masterkey.norm.yaml (see §2). Never re-read
                 from disk inside a renderer; never yaml.safe_load a raw
                 masterkey.yaml.
    outdir    -- absolute path to <client>/output/. Already exists.
    doc       -- the joined catalog+masterkey entry for THIS document (§3).

    Returns the ABSOLUTE paths of every file written, in any order.
    Writes NO divider. Writes nothing outside outdir.
    """
```

- **One document per call.** `render_evidence.py` is called once for the deed
  and once for the auto policy; it dispatches on `doc["id"]`.
- **Return absolute paths.** `merge_packet.py` and `verify_client.py` consume
  the return value. A relative path is a bug.
- **Idempotent.** Calling twice with the same arguments produces the same
  bytes and returns the same list.
- Every module also exposes `HANDLES: set[str]` — the `doc["id"]` values it
  can render — so the driver can route without a hardcoded table:

```python
HANDLES = {"joint_deed", "auto_policy", "i797c"}
```

- A renderer given a `doc["id"]` not in its `HANDLES` raises `ValueError`. It
  does not silently no-op.

### 1.1 Driver

`render_docs.py` exposes `render_all(slug, outdir)` which resolves the client's
document list, calls each renderer, and writes every divider itself. Workers do
not write a driver.

---

## 2. THE MASTERKEY — `.norm.yaml` ONLY

```python
from mklib import load_masterkey
mk = load_masterkey("almeida_paulo")     # reads clients/<slug>/masterkey.norm.yaml
```

**`clients/<slug>/masterkey.yaml` is provenance and nothing reads it**
(SPEC-DELTA D-I). The six authored files are six different shapes; the
normaliser flattens them to one. A renderer that reads the raw file gets a
`{list: [...]}` where it expected a list, or `q_1` where it expected `q1`, and
fails silently on two clients out of six.

### 2.1 Do not re-derive the exhibit rule

`mk["rule_inputs"]` already carries `c1_fires` … `c6_fires`, plus
`arrest_items_yes`, `part14_items_yes`, `trip_count`, `trips_on_form`,
`part8_rows`, `evidence_types` and `evidence_declined`. **Consume them.** Two
independent derivations of one rule is how a verifier ends up agreeing with a
renderer's shared mistake (SPEC-DELTA D-I).

### 2.2 `exhibits` is the authority; `exhibits_derived` MAY BE ABSENT

**`mk["exhibits"]` — a list of `{doc, seq, trigger, why}` — is the document
set.** `mk["exhibits_derived"]` exists on some clients and **is absent on
`tran_daniel`**. Reading `mk["exhibits_derived"]["document_count"]` crashes on
T1. It is advisory only; never a source of truth.

Note the key spelling in the masterkey: the catalog id lives under **`doc`**,
not `id`. `mklib` renames it to `id` in the joined dict (§3), which is the only
shape a renderer ever sees.

### 2.3 Seven shape collisions were found and fixed IN THE NORMALISER

D-I normalised the containers. Building the spine surfaced seven more places where
the six masterkey authors spelled ONE fact in two or three ways. Each is now
canonicalised in `normalize_masterkeys.py` — **re-run it, then read only these
spellings.** Every one of these would have failed silently on two clients out of
six, which is the exact failure mode D-I exists to prevent.

| fact | shapes that were in play | canonical now |
|---|---|---|
| current address / job | `present: true`, `current: true`, neither (`to: null`) | **`present: true`** on every row of `addresses` and `employment` |
| the 319(a) spouse the §5.1 clause names | `family.spouse.{honorific,full_name}`, or the whole string at `immigration.eligibility_clause_spouse` | **`family.spouse.honorific`** + **`family.spouse.full_name`** |
| Part 9 item-15 arrest row | `arrest_detail{crime_or_offense, offence_date, conviction_or_plea_date}`, `detail_row{offense, date_of_offense, date_of_conviction_or_plea}` | **`arrest_detail`** with `{offense, offense_date, conviction_date, place, disposition, sentence}` |
| height | `height:{feet,inches}`, `height_ft`/`height_in`, `height_feet`/`height_inches` | **`identity.height.{feet,inches}`** |
| weight | `weight_lbs`, `weight_lb` | **`identity.weight_lbs`** |
| passport number | `number`, `passport_number` | **`number`** — `passport_number` is MIRRORED to the same value, so a fabricator already coded against either spelling keeps working |
| country of birth / citizenship | `cob`/`coc`, `country_of_birth`/`country_of_citizenship` | **`cob`** / **`coc`** — long spellings mirrored. This one was SILENT: it left printed Part 2 items 10 and 11 blank on two clients while the round trip still reported zero diffs |

If you find a seventh, **add an alias to `normalize_masterkeys.py` and re-run
it**. Do not add an `or` to your renderer: that is the shim D-I rejected, and it
only works if all nine renderers remember it.

---

## 3. THE `doc` DICT — exact shape

`mklib.doc_entries(mk)` returns the client's documents, **ordered by `seq`**,
each a dict with exactly these keys:

| key | type | source | notes |
|---|---|---|---|
| `id` | str | catalog `id` / masterkey `doc` | e.g. `"joint_deed"` |
| `seq` | int | masterkey `exhibits[].seq` | the DOCUMENT number |
| `tab` | `"A"` / `"B"` | catalog | |
| `trigger` | str | masterkey | `"core"`, `"C1"`…`"C6"` |
| `file_stem` | str | catalog | **template slots already resolved** |
| `divider_title` | str | catalog | **already resolved**; ALL CAPS |
| `toc_line` | str | catalog | sentence case |
| `ships` | list[str] | catalog | `["pdf"]` or `["docx","pdf"]` |
| `authored_by` | str | catalog | `firm` / `form` / `exhibit` |
| `renderer` | str | catalog | the owning module |
| `notes` | str \| None | catalog | |
| `why` | str | masterkey | the trigger's justification prose |

**`{TAX_YEAR}` is resolved by `mklib`, not by you.** The catalog's `tax_return`
entry ships `file_stem: "{TAX_YEAR} Income Tax Return"` and
`divider_title: "{TAX_YEAR} INCOME TAX RETURN"`. `doc_entries()` substitutes
`mk["documents"]["tax_return"]["year"]` before any renderer sees the dict, so
`doc["file_stem"]` is **always literal**. Do not run your own substitution; if
you find a `{` in a string from `doc`, that is a `mklib` bug — report it, do not
patch around it.

Worked examples:

```python
# almeida_paulo, DOCUMENT 6
{"id": "tax_return", "seq": 6, "tab": "B", "trigger": "core",
 "file_stem": "2024 Income Tax Return",
 "divider_title": "2024 INCOME TAX RETURN",
 "toc_line": "Latest tax return",
 "ships": ["pdf"], "authored_by": "exhibit", "renderer": "render_1040.py",
 "notes": "§9.3.1 — when the return is joint it IS the marriage evidence; ...",
 "why": "unconditional core — continuous residence / GMC evidence; ..."}

# tran_daniel, DOCUMENT 8
{"id": "joint_deed", "seq": 8, "tab": "B", "trigger": "C3a",
 "file_stem": "Joint Deed",
 "divider_title": "JOINT DEED",
 "toc_line": "Joint deed",
 "ships": ["pdf"], "authored_by": "exhibit", "renderer": "render_evidence.py",
 "notes": None,
 "why": "basis == 319(a) AND the joint deed to the Westerville house was supplied"}
```

---

## 4. WHERE FILES GO, AND WHAT THEY ARE CALLED

### 4.1 The tree (STYLE-SPEC §2, verbatim folder names)

```
<outdir>/                                   # == <client>/output/
  00. Applicant Cover Page.docx  / .pdf
  Tab A (Content + Cover)/
    A-0. Tab Cover Page.docx / .pdf
    A-1.pdf                                 <- DIVIDER for document 1
    A-1. Table of Contents.docx / .pdf      <- CONTENT of document 1
    A-2.pdf
    A-2. Cover Letter.docx / .pdf
  Tab B (Biographical Info)/
    B-0. Tab Cover Page.docx / .pdf
    B-3.pdf
    B-3. Form N-400, Application for Naturalization.pdf
    B-4.pdf
    B-4. Bio Page of Passport.pdf
    ...
  N-400 Packet.pdf                          <- merged, flattened, 0 fields
```

The two folder names are literal, including the spaces and parentheses:
`Tab A (Content + Cover)` and `Tab B (Biographical Info)`. **Never spell them
yourself** — call `mklib.tab_dir(outdir, doc["tab"])`, which returns the
absolute path and creates it. The string then exists in exactly one place, for
the same reason the dividers do.

### 4.2 The naming rule, and the collision (STYLE-SPEC §2 — STATED LOUDLY)

```
content:  <TAB>-<seq>. <file_stem>.<ext>      e.g.  B-8. Joint Deed.pdf
divider:  <TAB>-<seq>.pdf                     e.g.  B-8.pdf
```

The **bare numbered PDF is the divider.** The file with a title after the
number is the **content**. They differ by a `. ` and a title, and they sort
against each other in the wrong order:

```
A-1. Table of Contents.docx     sorts BEFORE     A-1.pdf
```

because `.` (0x2E) precedes `.pdf`'s position after the digit. **Therefore
merge order is TOC order — the `seq` sequence from `doc_entries()` — and NEVER
a directory sort.** `merge_packet.py` enforces this; no renderer should ever
call `sorted(os.listdir(...))` on a component folder for any reason.

Use the helpers, never an f-string:

```python
mklib.component_path(outdir, doc, "pdf")   # .../Tab B (Biographical Info)/B-8. Joint Deed.pdf
mklib.divider_path(outdir, doc)            # .../Tab B (Biographical Info)/B-8.pdf   (render_docs only)
```

### 4.3 What ships, per document (SPEC-DELTA D-D)

| `authored_by` | ships | who |
|---|---|---|
| `firm` | **docx + pdf** | `render_docs.py`, `render_addendum.py` |
| `form` | pdf only | `render_n400.py`, `render_1040.py` |
| `exhibit` | pdf only | `render_evidence.py`, `render_court_records.py`, `fabricate_ids.py` |

**Fabricators emit PDF only.** No `.docx`, no `.jpg`, no `.png` as a shipped
component — intermediate images are fine, but the component is a PDF and only a
PDF (STYLE-SPEC §2.1 normalises away zhu's stray JPEG). Do not call `soffice`.

Always render exactly `doc["ships"]`; do not decide for yourself.

---

## 5. `mklib.py` — THE SHARED HELPERS. USE THEM; DO NOT REIMPLEMENT.

`import mklib` (it sits beside you in `lab/synthetic/tools/`). Everything below
is provided. Re-implementing any of it is how six renderers end up with six
date formats.

### 5.1 Paths and loading

```python
ROOT, TOOLS, CLIENTS, BLANKS, TEMPLATES, SPEC   # absolute path constants
load_masterkey(slug)      -> dict     # .norm.yaml ONLY
load_catalog()            -> dict     # templates/document-catalog.yaml
load_template(name)       -> dict     # templates/<name>.yaml
doc_entries(mk)           -> list[dict]      # §3, ordered by seq, slots resolved
doc_by_id(mk, doc_id)     -> dict
tab_dir(outdir, tab)      -> str      # creates; the ONLY place the folder names live
component_path(outdir, doc, ext) -> str
divider_path(outdir, doc)        -> str
```

### 5.2 Page geometry and typography (STYLE-SPEC §3)

```python
PAGE_W, PAGE_H      # 612.0, 792.0 pt — US Letter portrait
MARGIN              # 72.0 pt — 1 inch, all four sides
BODY_FONT           # "Times-Roman"   (reportlab base-14)
BODY_FONT_BOLD      # "Times-Bold"
BODY_PT             # 12.0
LEADING             # 13.8 pt  (12 pt x 1.15)
DOCX_FONT           # "Times New Roman"

new_canvas(path) -> reportlab.pdfgen.canvas.Canvas
    # US Letter portrait, invariant=1, Times-Roman 12, deterministic
    # /CreationDate and /ModDate already stamped. Just draw and save().
frame_text(canvas, lines, align="left", top=None, size=BODY_PT,
           leading=None, font=None) -> float       # returns the next free y
    # lay out lines inside the 1-inch frame at 1.15 leading.
    # `lines` items are either a plain str, or a (str, opts) tuple where opts
    # may carry {"bold": True, "underline": True, "size": 14, "indent": 18.0}
```

`new_canvas` is the floor for every reportlab-drawn exhibit. An exhibit does
not have to *look* like a firm memo — a deed, a policy and a court record each
have their own furniture — but the page is US Letter with 1-inch margins and
the base face is Times, so a merged packet does not change trim size mid-way.

### 5.3 docx (only for `authored_by: firm`)

```python
new_docx()  -> docx.Document
    # Letter, 1" margins, Times New Roman 12, line spacing 1.15,
    # no header, no footer, no page number, core properties frozen
add_para(document, text, align="left", bold=False, underline=False,
         indent_in=0.0, size_pt=None, spacing_after=None,
         tab_stops_in=()) -> paragraph
add_blank(document, size_pt=None)   # an EMPTY PARAGRAPH — the only block gap
save_docx(document, path) -> str    # SAVE THROUGH THIS, NEVER document.save()
docx_to_pdf(docx_path, outdir) -> str
    # soffice --headless --convert-to pdf, then normalised deterministic
```

**`document.save(path)` directly is FORBIDDEN.** python-docx stamps
`docProps/core.xml` with `datetime.now()` *and* writes every zip member with the
current clock, so two identical documents produce two different `.docx` files —
and then two different PDFs, because soffice converts what it is given.
`save_docx()` freezes both. This cost three separate fixes to find; do not
rediscover it.

**Plain paragraphs only.** No text boxes, no tables, no headers, no footers, no
page numbers, no shapes, no images in a firm-authored docx (STYLE-SPEC §3).
Block gaps are an empty paragraph, never `spacing after`. Alignments are only
`left`, `center`, `both`. Decorations are only bold and underline — **no
italics anywhere.**

### 5.4 Dates — exactly two house formats

```python
as_date(v)        -> datetime.date    # accepts date, "YYYY-MM-DD", "MM/DD/YYYY", "Month D, YYYY"
fmt_numeric(v)    -> "03/22/1988"     # MM/DD/YYYY, zero-padded
fmt_long(v)       -> "March 22, 1988" # Month D, YYYY — no leading zero on the day
```

`fmt_numeric` for the applicant cover page's `DOB:` and every N-400 date field.
`fmt_long` for the cover letter's date line, its `DOB:` line, and the 316(a)
eligibility clause's LPR date. **No third format is legal.** Do not call
`strftime("%B %-d, %Y")` yourself; `%-d` is not portable.

### 5.5 PDF utilities

```python
pdf_pagecount(path)   -> int
pdf_text(path, first=None, last=None) -> str    # pdftotext -layout
field_names(path)     -> set[str]               # AcroForm fully-qualified names
field_values(path)    -> dict[str, str]
```

### 5.6 AcroForm filling — READ THIS IF YOU TOUCH THE 1040

```python
btn_on_states(path) -> dict[str, str]
    # field name -> its SINGLE "on" appearance-state name, e.g. "/Y", "/N", "/A", "/APT"
fill_acroform(src_pdf, dst_pdf, values) -> None
    # deletes /XFA, sets NeedAppearances, stamps the fixed date, writes dst
```

Two empirical facts about these blanks, established by round trip against
`blanks/n-400.pdf`, that will otherwise cost you an afternoon:

1. **Field names are fully qualified and some contain literal backslashes** —
   `form1[0].#subform[6].P9_Line7\.c[1]`. pypdf's `get_fields()` keys match
   `n400-field-dump.tsv` column 2 **exactly**, all 488, escapes included. Use
   the name as written. (Note the TSV has embedded newlines inside the tooltip
   column; a naive line-splitter mis-parses three rows. `field_names()` reads
   the PDF, which is authoritative — prefer it to parsing the TSV.)

2. **A `/Btn` field's value is its own per-widget appearance-state name, and
   there is exactly one.** These are not `"Yes"`/`"No"` checkboxes. Each widget's
   `/AP /N` dictionary holds a single key, and that key is the only value that
   checks the box; anything else silently stores as `/Off`.

   ```
   P2_Line10_claimdisability[0] -> "/N"     (the "No" box)
   P2_Line10_claimdisability[1] -> "/Y"     (the "Yes" box)
   Part1_Eligibility[2]         -> "/A"     (eligibility box A)
   P4_Line1_Unit[2]             -> "/APT"
   P7_Line5_Eye[0]              -> "/BRO"
   ```

   The Yes and No boxes are **separate fields**, not one field with two states.
   The index in the name is NOT the box letter — `Part1_Eligibility[2]` is box
   **A**. **Always look the state up with `btn_on_states()`; never hardcode
   `"Yes"`, `"On"`, or `"/1"`.** Verified: setting a plausible-but-wrong state
   reads back as `/Off` and the box prints blank while a field-value diff
   against a truthy value can still look fine.

   To clear a button, set `"/Off"`.

### 5.7 MRZ (ICAO 9303)

```python
mrz_check_digit(s)  -> int          # weights 7,3,1; A=10..Z=35; '<'=0
mrz_lines(surname, given_names, doc_number, nationality, dob, sex,
          expiry, personal_number="") -> (line1, line2)   # two 44-char lines
```

The masterkeys already carry `documents.<passport>.mrz.line1/.line2` with the
check digits precomputed and validated by `validate_masterkeys.py` §5.
**Print the masterkey's lines**; use `mrz_lines()` only to assert they
recompute, never to invent a different pair.

### 5.8 Lockbox (STYLE-SPEC §7)

```python
lockbox_block(state, carrier) -> list[str]
    # the full address block INCLUDING the two agency lines, in order.
    # Line 1 is "U.S. Department of Homeland Security" (§16 ruling 8 OVERTURNED
    # the shorter zhu form -- this is the one every template comment gets wrong).
```

---

## 6. DETERMINISM — same masterkey in, byte-identical PDF out

Phase 5 diffs re-renders. A renderer that is not deterministic makes that
diff meaningless and will be sent back.

**Forbidden, without exception:**

- `datetime.now()`, `date.today()`, `time.time()` — for *anything*, including a
  "generated on" line nobody reads. Every date on every page comes from the
  masterkey.
- `random`, `uuid`, `hash()` on a str (PYTHONHASHSEED is not pinned), or
  iteration over an unordered set where order reaches the page.
- Letting reportlab or LibreOffice stamp their own timestamps.

**Required:**

```python
mklib.FIXED_PDF_DATE          # "D:20260101000000Z" — the one creation date
mklib.stamp_deterministic(x)  # x = a PdfWriter, or a path to rewrite in place
```

`new_canvas()`, `fill_acroform()` and `docx_to_pdf()` already call it. If you
produce a PDF by any other route, call it yourself before returning.
`new_canvas()` additionally passes reportlab's `invariant=1`, which suppresses
its document ID and timestamp.

Self-check before you hand in:

```bash
python3 -c "import render_yours as r, mklib; r.render(...)" ; cp out.pdf a.pdf
python3 -c "import render_yours as r, mklib; r.render(...)" ; cmp a.pdf out.pdf
```

`cmp` must be silent.

---

## 7. WHO OWNS WHAT

| module | documents (`doc["id"]`) | owner |
|---|---|---|
| `mklib.py` | — shared helpers | toolsmith |
| `render_docs.py` | `table_of_contents`, `cover_letter`, `written_explanation`, the three pre-documents, **and every divider** | toolsmith |
| `render_n400.py` | `n400` | toolsmith |
| `merge_packet.py` | — the merged packet | toolsmith |
| `verify_client.py` | — layer-1 verification | toolsmith |
| `verify_set.py` | — set-level verification | toolsmith |
| `render_1040.py` | `tax_return` | worker |
| `render_evidence.py` | `i797c`, `joint_deed`, `auto_policy` | worker |
| `render_court_records.py` | `court_records` | worker |
| `fabricate_ids.py` | `applicant_passport`, `green_card`, `spouse_passport`, `child_passport` | worker |
| `render_addendum.py` | `travel_addendum` | worker |

`render_addendum.py` is the one worker-owned module that is `authored_by: firm`
and therefore ships **docx + pdf** via `new_docx()` / `docx_to_pdf()`. Its
format is a prose-and-list page (STYLE-SPEC §4.5), **not** a spreadsheet —
BUILD-PLAN §4's openpyxl suggestion is superseded; see `tools/README.md`.

Facts each renderer consumes are enumerated in STYLE-SPEC §12.10. If a fact you
need is not in the masterkey, that is a masterkey bug — report it; do not invent
the value, because an invented proper noun is exactly what the Phase 5 leakage
gate is looking for.

---

## 8. CHECKLIST BEFORE YOU HAND IN

- [ ] `render(masterkey, outdir, doc)` returns a list of **absolute** paths.
- [ ] `HANDLES` is defined and an unknown `doc["id"]` raises `ValueError`.
- [ ] Exactly the extensions in `doc["ships"]` were written — no more.
- [ ] **No bare `<TAB>-<seq>.pdf` was written.** You did not create a divider.
- [ ] You did not delete, clear or recreate `outdir` or anything in it
      that you did not write (§0.5).
- [ ] Paths came from `component_path()`; the tab folder name is never spelled
      in your source.
- [ ] Dates came from `fmt_numeric` / `fmt_long`. No `strftime` in your file.
- [ ] No `datetime.now()`, no `random`, no `uuid` anywhere in your file.
- [ ] Two consecutive renders are byte-identical (`cmp` silent).
- [ ] **No firm name, preparer name, business address, firm phone or firm
      email appears on any page you render.** Grep your own output:
      `pdftotext -layout out.pdf - | less`.
- [ ] Every `/Btn` value came from `btn_on_states()`, not a guess.
- [ ] `pdftotext -layout` on your output shows the values actually printed —
      a field-value round trip alone does not prove the page is not blank.
