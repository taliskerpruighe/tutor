# Phase 5 — Layer-2 Client Review — `stavros_daphne`

**Verdict: FAIL**

T2 is the acceptance gate for the whole spike, and Document 8 — the C6
written explanation, "the whole reason this client exists in this shape" —
ships broken in two independent ways. Both are in the one document the brief
asked me to scrutinize most closely. Everything else in the packet is clean,
and the input side (the part a solver actually works from) is sufficient and
well constructed; the failure is entirely in the build pipeline's rendering
of the masterkey, not in the client's story or its emails.

---

## Findings

### 1. [blocking] Written explanation does not lead with Item 20 — paragraph order is scrambled, and the defect is systemic, not client-specific

**File:** `output/Tab B (Biographical Info)/B-8. Written Explanation.pdf` (and
the merged `output/N-400 Packet.pdf`)

The rendered order is **Item 12, then Item 20, then Item 8.a**. The brief is
explicit that the explanation must lead with the removal-proceedings
narrative (Item 20) "FIRST and at length," with the military service as "a
closing formality." `masterkey.norm.yaml` agrees with itself on this three
separate times:

- `immigration.written_explanation_structure.order: [q20, q8a, q12]`
- `immigration.written_explanation_structure.lead_paragraph_is: q20`
- `immigration.written_explanation_structure.render_note`: *"render_docs.py
  must emit the paragraphs in `order`. The Item 20 narrative is the substance
  of the document; the military-service paragraph is a closing formality and
  must not open it."*

None of that is honored. I traced the mechanism: `render_written_explanation()`
in `lab/synthetic/tools/render_docs.py` (line 210) iterates
`rule_inputs.part14_items_yes`, and that list is built by
`normalize_masterkeys.py` line 447:

```python
part14 = sorted(i for i, v in ((v["item"], v) for v in mc.values())
                 if v["classification"] == "part14" and is_yes(v))
```

`sorted()` on the raw item-label strings gives lexicographic order —
`"12" < "20" < "8a"` — which is exactly the (wrong) order that ships. The
`written_explanation_structure.order` field the masterkey author wrote for
this exact purpose is never read by either script. **This is a build-pipeline
defect, not a stavros_daphne-specific one**: any client with more than one
`part14`-classified item Yes will get its written explanation scrambled by
this same lexicographic sort, and narrative lead order will be wrong whenever
the intended order isn't already alphabetical. I hold only this one client's
full packet, so I can't confirm which other clients are affected, but the
mechanism guarantees it isn't limited to this one — flagging for whoever owns
cross-client triage.

**What to change:** `normalize_masterkeys.py` (or `render_docs.py`) must read
`immigration.written_explanation_structure.order` when it exists and use it
to sequence `part14_items_yes`, instead of `sorted()` on the label strings.

### 2. [blocking] The Item 20 paragraph ends in a raw, unresolved internal key path instead of the narrative

**File:** same as above.

The Item 20 paragraph as shipped:

> "Placed in removal proceedings 2015-09-14 following the 2015-02-11 denial
> of a Form I-485 filed on his behalf (notices went to a superseded address);
> proceedings TERMINATED 2018-11-06 without any order of removal. **Full
> narrative in `immigration.history_for_the_written_explanation`.**"

That last sentence is not text — it's an unresolved authoring reference to a
YAML path, printed verbatim into a document that ships to USCIS. It's baked
into `masterkey.norm.yaml` itself, at the `moral_character.q20.explanation`
field (~line 875), so it isn't a template artifact; whoever wrote that field
left a note-to-self ("full narrative lives in that other field, expand it
here") and it was never expanded. The dated narrative it's pointing at
already exists, fully written, five entries long, right there in
`immigration.history_for_the_written_explanation` (I-130 filed 2013-06-18 →
I-485 denied 2015-02-11 on a superseded address → NTA/removal proceedings
2015-09-14 → terminated 2018-11-06, no removal order → LPR 2020-01-23). None
of that made it into the actual paragraph. The brief calls for the narrative
"at length"; what ships is one compressed sentence plus a broken reference.

This also has a visible look-and-feel cost I confirmed by rendering the page:
because the backtick-quoted token is unbreakable, the justified paragraph
stretches unnaturally around it ("...06　without　any　order　of　removal.
Full　narrative　in `immigration.history_for_the_written_explanation`.") —
the one ugly line break on an otherwise clean page. Fixing the content also
fixes the visual defect.

**What to change:** replace the `Full narrative in ...` sentence in
`moral_character.q20.explanation` with the actual expanded narrative drawn
from `immigration.history_for_the_written_explanation` (or have the renderer
pull that list programmatically instead of relying on a hand-written
paragraph that references it by name).

### 3. [note, likely systemic, does not affect verdict] Part 6 Item 1 asks for children "under 18," entered as 1, against an adult daughter

**File:** `output/Tab B (Biographical Info)/B-3. Form N-400...pdf`, page 5.

Part 6 Item 1 reads "Indicate your total number of children under 18 years of
age," filled in as `1`; Item 2 then lists the only child, Daphne Stavros, DOB
02/27/1984 — 41 years old at filing. I checked the blank template
(`lab/synthetic/blanks/n-400.pdf`) and confirmed "under 18 years of age" is
the genuine boilerplate text on the official form, not a rendering error —
so this isn't a stavros-specific defect and it isn't something the masterkey
author introduced; the `1` came from the masterkey and passed the
differential field-coverage sweep. Whether an adult child belongs in this
count/table at all is a cross-client form-interpretation question (i.e., does
the real N-400 mean "list all your children, but only count minors in Item
1," and is `1` therefore simply the wrong count regardless of who's listed).
I'm flagging it because it's visibly odd on the page, but it isn't
stavros_daphne's story that's wrong here, and it doesn't move the verdict.

### 4. [note] N-400 Part 14 is left entirely blank with no cross-reference to Document 8

Items 8.a, 12, and 20 all instruct the applicant to explain in "Part 14.
Additional Information," but the rendered Part 14 (page 12) is blank, and
nothing on the N-400 itself points a reader to the standalone written
explanation. This is evidently the intended packet convention (the exhibit
set and TOC/divider lock are machine-verified, and the written explanation
exists specifically to carry what Part 14 can't), so I'm not asking for it to
be fixed — just noting that a first-time reader of the form alone, without
the tab structure in hand, has no textual signpost to Document 8.

---

## What's clean — confirmed by direct inspection, not re-derivation

- **The Items 8.a/12 narrative fix (email `000004`) reads naturally and a
  solver would catch it.** The transition — "One more thing while I'm
  thinking about it, and I don't want to bury it under everything above" —
  is in voice: it matches the established pattern of Daphne circling back
  with things she's realized might matter, not a bolted-on compliance line.
  "He served in the Hellenic Army, Infantry, as a Private" maps directly to
  Item 8.a; "they did give him ordinary weapons and basic infantry training"
  maps directly to Item 12. Critically, this narrated surface is
  **independently sufficient** — a solver who correctly applies W1's
  over-delivery rule and treats the discharge-paper scan in email `000002`
  as inert (per the brief's own instruction) still lands both items correctly
  from email `000004` alone. The scan remains genuine, redundant
  corroboration, not the only route to the answer.
- **Nothing implies an arrest; C5 correctly does not fire.** Email `000004`
  forecloses the misreading explicitly ("he was never arrested, never
  detained, never charged with anything"); the input table answers 15.a/15.b
  `No`; the rendered N-400 shows 15.a = No, 15.b = No, and the crime/offense
  table (page 8) is empty. Confirmed by direct inspection of the rendered
  page.
- **The day trip is handled correctly.** Present in the input (CSV/XLSX row
  "Travel Trip 9," 08/12/2023, same-day Niagara Falls crossing into Canada),
  absent from both the N-400 Part 8 table (six rows, all Greece,
  11/02/2025→10/10/2022) and the travel addendum (eight trips, all Greece).
- **Superseded address resolved correctly and chronologically.** Current
  address on the N-400 is 74 Fern Hollow Road, Montclair (since 2024-08-15);
  231 Ridgeline Avenue, Bloomfield appears as the prior address
  (2011-05-20–2024-08-14), matching the correction in email `000003`.
- **Over-delivery and unrelated-matter noise correctly excluded.** The two
  expired passports, military discharge scan, death certificate, utility
  bill (email `000002`), and the LLC tax question (email `000005`) produce no
  exhibits and no packet facts. TOC confirms exactly 8 documents, matching
  the brief's C4+C6 set.
- **No firm identity anywhere; N-400 correctly unsigned.** Cover letter and
  signature block read "Petition Preparer" only — no firm name, address,
  phone, or email anywhere in the rendered output. N-400 Part 11 is filled
  with the applicant's own phone/email; Part 13 (preparer block) is entirely
  blank; the applicant's signature and date fields on page 11 are blank.
  Confirmed by direct visual inspection of the rendered pages.
- **Look and feel is otherwise clean.** Tab dividers ("TAB A / SUMMARY," "TAB
  B / BIOGRAPHICAL INFORMATION") are large, centered, legible. TOC, cover
  letter, and travel addendum render cleanly at 150 dpi with no layout
  breakage other than the one justification artifact noted in Finding 2.
- **Timeline is plausible throughout:** born 1957, first entered 2011 at 54
  (Item 22.a correctly No), I-130/I-485 filed 2013, denial 2015, NTA and
  removal proceedings 2015, terminated 2018, LPR 2020, retired 2023 at 66 —
  internally consistent, no arithmetic contradictions.

---

## Answers to the specific questions asked

**Is the input sufficient for a solver to rebuild the packet?** Yes. The
input side — the five emails and attachments — is complete, well-organized,
and unambiguous once read in full (including the narrated paragraph in
`000004`, not just the attachment pile). Every mess type (superseded address,
day trip, over-delivery, unrelated-matter noise, the buried 8.a/12 fact) is
resolvable from the input alone using the rules the worked pairs teach. The
failure identified here is entirely downstream, in how the build pipeline
rendered the masterkey into Document 8 — it is not a defect a solver reading
the input correctly would reproduce, and not a defect in the input itself.

**Items 8.a/12 fix — does it read naturally, and would a solver catch it?**
Yes to both, addressed in full above.

**Does anything imply an arrest?** No — confirmed clean, addressed in full
above.

**Any blocking finding, in full?** Findings 1 and 2, both against
`output/Tab B (Biographical Info)/B-8. Written Explanation.pdf` (and its copy
inside `N-400 Packet.pdf`): the written explanation opens with the military
paragraph instead of the removal-proceedings paragraph (order is 12/20/8a
instead of the masterkey-mandated 20/8a/12, traced to a lexicographic
`sorted()` in `normalize_masterkeys.py` line 447 that ignores
`written_explanation_structure.order`), and the Item 20 paragraph ends with
an unresolved internal key-path reference — `` `immigration.history_for_the_written_explanation` ``
— instead of the narrative that field actually contains.


---

## ADDENDUM — 2026-08-22, after the fixes

**This report's verdict above was FAIL. The two blocking findings it raised have since
been fixed and re-verified. The current state of this client is PASS.** The
original verdict is left standing rather than edited, because the finding was
correct when it was made and the record of it is the point.

### What was fixed

1. **Written explanation opened on the wrong paragraph** (Item 12 before Item 20),
   because `normalize_masterkeys.py` sorted the Part-14 item labels
   lexicographically — "12" < "20" < "8a". **Fixed**: the normaliser now sorts
   numerically and, where the masterkey pins an order, honours it. T2 pins
   `[q20, q8a, q12]`. Re-rendered and confirmed: the document now leads with
   Item 20, with the military-service paragraph as a closing formality.
2. **The Item 20 paragraph printed a raw internal key path**
   (`immigration.history_for_the_written_explanation`) instead of the narrative
   it named. **Fixed**: the narrative was written out in full. It was also
   deduplicated and its ISO dates converted to the house `Month D, YYYY` form.

### How the current state was verified
Re-rendered from the corrected toolchain, then: `verify_client.py` green;
`verify_coverage.py` green (a differential sweep of 325 N-400 fields across all
six clients, plus must-fill/must-be-empty controls proved to exist before being
asserted); `merge_packet.py`'s new text-layer and ink-coverage assertions pass on
every page; and the rendered pages the finding named were re-rasterised and
looked at. Determinism was re-confirmed after the toolchain changes: a full
re-render of a client is byte-identical across 26 components including the
merged packet.
