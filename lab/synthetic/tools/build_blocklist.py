#!/usr/bin/env python3
"""build_blocklist.py — harvest the real-client leakage blocklist from lab/.

Phase 1 artefact. Reproducible: re-running it on an unchanged lab/ tree
produces a byte-identical blocklist.txt.

WHAT IT HARVESTS
  Every .txt sidecar (extracted document text), every email body .txt, every
  .md report, and every file and directory NAME under lab/ -- for all five
  client folders, not just the two format sources.
    - proper nouns (capitalised runs, emitted whole and per component)
    - number-strings (A-numbers, receipt numbers, case/docket numbers, phone
      numbers, ZIPs, SSNs, passport numbers, any digit run of 5+)
    - street addresses and address tokens
    - employer names (via the proper-noun pass; the reports name them)
    - email addresses and mail domains

WHAT IT DELIBERATELY EXCLUDES  (see STYLE-SPEC "SHARED STRINGS - NOT LEAKAGE")
  The Phase 5 leakage scan greps this list against the synthetic output in
  both directions and allows zero hits. So any string the synthetic packets
  must contain BY DESIGN has to stay off the list, or the gate fails by
  construction on all six clients:
    - the four USCIS lockbox blocks (both USPS and courier variants)
    - USCIS / DHS / form names / statutory citations / the fee
    - US state names and abbreviations, month names, country names
    - generic address nouns (Street, Apt, Suite, ...)
    - ordinary English words and cover-letter boilerplate

SOURCES EXCLUDED FROM THE HARVEST
    - lab/synthetic/       (self-poisoning on re-run)
    - lab/BUILD-PLAN.md    (it names the SIX SYNTHETIC clients; blocklisting
                            Almeida/Kavanagh/Nowak/Tran/Stavros/Adeyemi would
                            fail the leakage scan on every packet)
  lab/reports/ IS harvested: it is the only place the OCR variants of
  scan-derived proper nouns are recorded (FILE-MAP s7).

USAGE
    python3 build_blocklist.py [--lab LAB_DIR] [--out OUT_FILE]
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

# --------------------------------------------------------------------------
# 1. MANDATORY ENTRIES -- always emitted, never filtered.
#    The firm's real reference identity, plus every OCR variant the correction
#    reports recorded for a proper noun lifted from a scan.
# --------------------------------------------------------------------------
KEEP_ALWAYS = [
    # firm identity (real reference facts; the synthetic firm is invented)
    "SYMPLE", "Symple", "Sympla", "SYMPLA",
    "trysymple.com", "contact@trysymple.com", "marcel@trysymple.com",
    "Marcel Oliveira", "Marcel S. Oliveira", "Marcel", "Oliveira",
    "Petition Preparer",
    "26 Broadway", "31 Hudson Yards", "66 Hudson Blvd E",
    "26 Broadway Fl 8", "31 Hudson Yards Fl 11", "31 Hudson Yards Fl. 11",
    # OCR variants recorded in lab/reports/ -- scan-derived, unreliable, so
    # every reading goes on the list (FILE-MAP s7)
    "Malone", "Ma Lone", "MaLone",
    "Comerio", "Commerico",
    "Nery & Richardson", "Nery & Richardson LLC", "Nery", "Richardson",
    "Griffin & Gallagher", "Griffin", "Gallagher",
    "Coconautsand", "CoconautSand", "Coconautsand LLC",
    "DLC Tax Services", "DLC Tax Services and Accounting Inc",
    "Ensomo", "E W Scrippa", "EW Scrippa",
    # read visually from image-only scans during Phase 1 -- these exist on no
    # text layer anywhere in the corpus, so the sidecar pass cannot see them
    # and the OCR pass may or may not recover them cleanly
    "206854142", "A-206854142", "206-854-142",      # jacobs/N-400 p.1
    "1900013028", "CR-240591", "24D591",            # zhu/courts, docket + case
    "Greenwich Police", "Hudock", "Comerford", "Nemec",
    "123 Hoyt Street", "37 Putnam Avenue", "37 Putnam Green",
    "Stamford GA1/PART A",
    "2124647255", "(212) 464-7255",                 # zhu/merged p.9, G-1450
    "9333",
]

# --------------------------------------------------------------------------
# 2. EXCLUSIONS -- strings the synthetic packets are REQUIRED to contain.
# --------------------------------------------------------------------------

# 2a. The four live N-400 paper-filing lockboxes, both carrier variants.
#     Fetched 2026-08-21 from uscis.gov (page last reviewed 01/24/2025).
LOCKBOX_STRINGS = """
USCIS Elgin Lockbox   USCIS Phoenix Lockbox   USCIS Dallas Lockbox
USCIS Chicago Lockbox
Elgin Phoenix Dallas Chicago Tempe Lewisville  Carol Stream
P.O. Box 4060   P.O. Box 21251   P.O. Box 660060   P.O. Box 4380
P.O. Box 4446   Box 4060 Box 21251 Box 660060 Box 4380 Box 4446
2500 Westfield Drive   2108 E. Elliot Rd.   131 S. Dearborn
2501 S State Hwy 121 Business
Westfield Elliot Dearborn Business Suite
60197-4060 60124-7836 85036-1251 85284-1806 75266-0060 75067-8003
60680-4380 60603-5517 60680-4446
4060 21251 660060 4380 4446 60197 60124 85036 85284 75266 75067 60680 60603
Carol Stream, IL  Elgin, IL  Tempe, AZ  Phoenix, AZ  Dallas, TX
Lewisville, TX  Chicago, IL
"""

# 2b. Agency, form, statute and fee vocabulary.
FORM_STRINGS = """
USCIS DHS Department of Homeland Security
United States Citizenship and Immigration Services
U.S. Department of Homeland Security
Department Homeland Security United States Citizenship Immigration Services
Form Forms N-400 N400 N-600 N-336 I-551 I-751 I-797 I-797C I-824 I-130 I-485
G-1450 G-1145 G-28 G-1151 DS-260 AR-11 1040 8879 W-2 1099 1099-B 8949 8995-A
Application for Naturalization  Permanent Resident Card
Alien Registration Number  A-Number  Lawful Permanent Resident
Table of Contents  Index of Documents  Cover Letter  Travel Addendum
Court Records  Written Explanation  Classification Basis
INA USC CFR C.F.R. U.S.C. Section 316 319 1430 1427 1445 316.2 319.1
760 710 380 680 Superior Court  Certified Copy
"""

# 2c. Geography that any client may legitimately share.
GEO_STRINGS = """
Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware
Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana
Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana
Nebraska Nevada Hampshire Jersey Mexico York Carolina Dakota Ohio Oklahoma
Oregon Pennsylvania Rhode Island Tennessee Texas Utah Vermont Virginia
Washington West Wisconsin Wyoming Columbia Guam Samoa Puerto Rico Palau
Micronesia Marshall Mariana Northern Commonwealth Virgin Islands Armed Forces
AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS
MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY
USA United States America American
Australia Australian Brazil Brazilian China Chinese Italy Italian Ireland
Irish Poland Polish Vietnam Vietnamese Greece Greek Nigeria Nigerian
Philippines Filipina Filipino Mexican Malaysia Indonesia Maldives Singapore
Argentina Canada Canadian France French Germany German India Indian Japan
Japanese Korea Spain Spanish Portugal Portuguese Netherlands Belgium Sweden
Norway Denmark Finland Switzerland Austria Greece Turkey Egypt Kenya Ghana
Colombia Peru Chile Ecuador Venezuela Guatemala Honduras Salvador Panama
Dominican Haiti Jamaica Cuba Taiwan Thailand Vietnam Cambodia Laos Nepal
Pakistan Bangladesh Lanka Russia Ukraine Romania Hungary Czech Slovakia
Croatia Serbia Bulgaria Israel Lebanon Jordan Emirates Arabia Qatar Kuwait
Morocco Tunisia Algeria Ethiopia Uganda Tanzania Zambia Zimbabwe Africa
Europe Asia Kingdom Britain England Scotland Wales Zealand
January February March April May June July August September October November
December Monday Tuesday Wednesday Thursday Friday Saturday Sunday
Jan Feb Mar Apr Jun Jul Aug Sep Sept Oct Nov Dec
Mon Tue Tues Wed Thu Thur Thurs Fri Sat Sun GMT UTC EST EDT CST CDT PST PDT
"""

# 2d. Generic address / document nouns.
GENERIC_STRINGS = """
Street St Avenue Ave Road Rd Boulevard Blvd Drive Dr Lane Ln Court Ct Place
Pl Way Circle Cir Terrace Ter Highway Hwy Parkway Pkwy Square Sq Trail Trl
Loop Run Row Walk Plaza Broadway Yards Green Park Hill View Ridge Creek
Apt Apartment Ste Suite Unit Flr Floor Fl Number No Box PO POB
City Town State ZIP Code Country Province Postal Care
Attn Attention VIA Via FedEx UPS DHL USPS Federal Express
U.S. US America Postal Service
Mr Mrs Ms Miss Dr Jr Sr II III IV LLC LLP Inc Corp Co Ltd PC PA JD Esq
"""

# 2e. Ordinary English, correspondence and cover-letter boilerplate.
COMMON_WORDS = """
The A An And Or But If Of To In On At By For From With Without As Is Are Was
Were Be Been Being Have Has Had Do Does Did Will Would Can Could Shall Should
May Might Must This That These Those There Here It Its He She They We You I
His Her Their Our Your My Me Him Them Us Who Whom Whose Which What When Where
Why How All Any Some Each Every Both Either Neither Not No Nor Only Also Just
More Most Less Least Very Much Many Few Other Another Same Such Than Then
Now Yet Still Again Once Twice First Second Third Fourth Fifth Next Last
Please Thank Thanks Dear Hello Best Regards Sincerely Kind Warm Hope Hoping
Good Great Morning Afternoon Evening Night Today Tomorrow Yesterday Week
Month Year Day Days Weeks Months Years Time Times Date Dates Enclosed
Enclosure Encls Attached Attachment Attachments Copy Copies Original
Originals Photocopy Photocopies Document Documents Documentation Evidence
Supporting Information Applicant Applicants Application Applications
Naturalization Citizenship Resident Residence Residency Permanent Conditional
Spouse Spouses Marriage Married Marital Child Children Parent Parents Family
Employer Employment Employed Employee Occupation Title Job Work Working
Travel Trips Trip Departure Return Returned Abroad Outside Inside
Passport Visa Card Green Birth Born Country Nationality Citizen Eligible
Eligibility Basis Pursuant Accordingly Provision General Adjudication
Adjudicate Speedy Favorable Concern Whom Look Looking Forward Present
Adjudicating Process Processing Packet Packets Tab Tabs Summary Summaries
Biographical Contents Content Cover Letter Letters Page Pages Part Parts Item
Items Question Questions Answer Answers Yes No None Name Names Full Legal
Given Middle Last Family Signature Signed Sign Date Signature Preparer
Interpreter Certification Certify Under Penalty Perjury True Correct Complete
Note Notes Please Provide Provided Providing Send Sent Sending Receive
Received Receiving Reply Replying Follow Following Update Updated Updates
Confirm Confirmed Confirmation Confirming Check Checking Question Regarding
Subject Message Email Emails Phone Telephone Mobile Cell Contact Address
Addresses Home Office Firm Client Clients Matter Matters File Files Folder
New Old Current Latest Previous Prior Former Recent Final Draft Version
Sorry Apologies Attach Attaching Let Know Need Needed Needs Want Wanted Would
Get Got Getting Make Made Making Take Taken Taking Give Given Giving Go Going
Come Coming See Seen Seeing Say Said Saying Tell Told Telling Ask Asked
Asking Think Thought Feel Felt Find Found Look Looked Use Used Using Help
Helped Helping Start Started Starting Finish Finished Sure Fine Okay OK Yes
Thanks Cheers Talk Speak Spoken Call Called Calling Meet Meeting Met Wait
Waiting Waited Send Attached Hi Hey Morning Everyone Team Sir Madam
Fwd Fw Re RE FW FWD CC BCC Sent To From Subject Message ID Content Type
Outlook Gmail Google Docs Word Excel PDF JPEG JPG PNG Drive Dropbox iOS
iPhone Android Mac Windows Adobe Reader Acrobat Jotform Airtable
One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Twenty Thirty
Forty Fifty Sixty Seventy Eighty Ninety Hundred Thousand Million
"""


def _split(blob):
    """Split an exclusion blob into single tokens and multi-word phrases."""
    out = set()
    for line in blob.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # phrases separated by 2+ spaces on the geo/lockbox blobs
        for phrase in re.split(r"\s{2,}", line):
            phrase = phrase.strip()
            if not phrase:
                continue
            out.add(phrase.lower())
            for tok in phrase.split():
                out.add(tok.strip(".,;:()").lower())
    return out


EXCLUDE = set()
for _blob in (LOCKBOX_STRINGS, FORM_STRINGS, GEO_STRINGS, GENERIC_STRINGS,
              COMMON_WORDS):
    EXCLUDE |= _split(_blob)

# 2f. Vocabulary of the exhibits the synthetic build itself renders
#     (1040, joint deed, auto policy, I-797C receipt notice, court records,
#     travel addendum, resume). These words appear in synthetic output by
#     design, so they cannot be leakage markers.
EXHIBIT_STRINGS = """
Income Tax Return Returns Taxable Adjusted Gross Deduction Deductions
Standard Itemized Refund Refunds Withheld Withholding Wages Salary Salaries
Interest Dividends Capital Gains Loss Schedule Schedules Internal Revenue
Service Treasury Filing Status Single Joint Separately Household Qualifying
Surviving Exemption Credit Credits Payments Payment Amount Total Subtotal
Balance Due Owed Preparer Preparation Client Copy Do Not File Signature
Authorization Electronic Direct Deposit Routing Account Bank
Deed Warranty Quitclaim Grantor Grantee Recorder Recorded Recording Parcel
Legal Description Lot Block Consideration Conveys Convey Conveyed Property
Real Estate Title Insurance Insured Insurer Policy Policies Declarations
Coverage Coverages Premium Premiums Vehicle Vehicles Auto Automobile Liability
Collision Comprehensive Deductible Effective Expiration Named Insureds Term
Notice Notices Receipt Receipts Action Case Type Petition Remove Conditions
Removal Approved Pending Priority Sent Beneficiary Petitioner Applicant
Superior Court Courts Docket Disposition Dismissed Nolle Dismissal Judge
Clerk Certified Plea Verdict Count Counts Offense Charges Charged Arrest
Arrested Police Department Agency Information Allegation Prosecuting Authority
General Statute Statutes Violation Continued Purpose Reason Bond Surety
Resume Curriculum Vitae Experience Education Skills Summary Professional
References Available Request
Travel Addendum Trips Departed Returned Excluding Day Combines Listed
Table Contents Cover Page Document Documents Tab Tabs
"""
EXCLUDE |= _split(EXHIBIT_STRINGS)

KEEP_LOWER = {k.lower() for k in KEEP_ALWAYS}

# --------------------------------------------------------------------------
# 3. EXTRACTION PATTERNS
# --------------------------------------------------------------------------
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
RE_DOMAIN = re.compile(r"\b(?:[\w-]+\.)+(?:com|org|net|gov|edu|io|co|us)\b",
                       re.I)

NUMBER_PATTERNS = [
    re.compile(r"\bA-?\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}\b"),      # A-number
    re.compile(r"\b[A-Z]{3}\d{10}\b"),                          # receipt no
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),                       # SSN
    re.compile(r"\(\d{3}\)\s?\d{3}-?\d{4}\b"),                  # phone
    re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),                       # phone
    re.compile(r"\b\d{5}-\d{4}\b"),                             # ZIP+4
    re.compile(r"\b[A-Z]{1,2}\d{7,9}\b"),                       # passport
    re.compile(r"\b[A-Z]{2,4}-?\d{6,}\b"),                      # docket/case
    re.compile(r"\b\d{5,}\b"),                                  # any long run
]

STREET_SUFFIX = (r"St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|"
                 r"Lane|Ct|Court|Pl|Place|Way|Cir|Circle|Ter|Terrace|Hwy|"
                 r"Highway|Pkwy|Parkway|Sq|Square|Trl|Trail|Loop|Row|Walk|"
                 r"Plaza|Broadway|Yards|Green|Park")
RE_STREET = re.compile(
    r"\b\d{1,6}\s+(?:[A-Z0-9][\w.'’-]*\s+){0,4}(?:" + STREET_SUFFIX +
    r")\b\.?")

# a capitalised run: Xuying Zhu, Blazing Star Road, Long Bridge Securities
RE_PROPER = re.compile(
    r"\b[A-Z][\w'’-]*(?:\s+(?:of|de|del|da|von|van|la|le|&)\s+)?"
    r"(?:\s+[A-Z][\w'’-]*){0,4}\b")

RE_HEADER_NAME = re.compile(
    r"^(?:From|To|CC|BCC|Reply-To):\s*(.+)$", re.M | re.I)
RE_HONORIFIC = re.compile(
    r"\b(?:Mr|Mrs|Ms|Miss|Dr|Prof)\.?\s+((?:[A-Z][\w'’-]*\s*){1,4})")

TEXT_SUFFIXES = (".txt", ".md")
NO_TEXT_MARKER = "[NO TEXT LAYER"
OCR_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         ".ocr-cache")
SKIP_DIR_NAMES = {"synthetic"}
SKIP_FILE_NAMES = {"BUILD-PLAN.md"}


def ocr_pdf(path):
    """Rasterise an image-only PDF and OCR it, with an on-disk cache.

    54 of the 185 corpus PDFs have no text layer, and their sidecars are the
    stub '[NO TEXT LAYER - ...]'. Every identifier that lives ONLY on a scan
    (jacobs' A-number, zhu's police case number, the deed and tax preparers)
    is invisible to the sidecar pass. OCR closes that hole -- and its noise is
    a feature here, because the OCR variants of a scan-derived proper noun are
    exactly what FILE-MAP s7 says must go on the list in every reading.

    The cache is keyed on the PDF's own bytes, so a rerun is offline and
    deterministic even though tesseract itself is not pinned.
    """
    with open(path, "rb") as fh:
        key = hashlib.sha1(fh.read()).hexdigest()
    cached = os.path.join(OCR_CACHE, key + ".txt")
    if os.path.exists(cached):
        with open(cached, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    if not shutil.which("tesseract") or not shutil.which("pdftoppm"):
        return ""
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        stem = os.path.join(tmp, "pg")
        try:
            subprocess.run(["pdftoppm", "-r", "200", "-gray", "-png",
                            path, stem], check=True, timeout=600,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        except (subprocess.SubprocessError, OSError):
            return ""
        for png in sorted(os.listdir(tmp)):
            if not png.endswith(".png"):
                continue
            try:
                r = subprocess.run(
                    ["tesseract", os.path.join(tmp, png), "stdout"],
                    check=True, timeout=180, capture_output=True)
                out.append(r.stdout.decode("utf-8", errors="replace"))
            except (subprocess.SubprocessError, OSError):
                continue
    text = "\n".join(out)
    os.makedirs(OCR_CACHE, exist_ok=True)
    with open(cached, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


def emit(bag, value, forced=False):
    v = " ".join(str(value).split()).strip(" .,;:'\"()[]")
    if not v:
        return
    low = v.lower()
    if forced or low in KEEP_LOWER:
        bag.add(v)
        return
    if low in EXCLUDE:
        return
    if len(v) < 3:
        return
    if v.isdigit() and len(v) < 5:
        return
    # a multi-word phrase survives only if at least one component is novel
    parts = [p for p in re.split(r"[\s/]+", low) if p]
    if len(parts) > 1 and all(p.strip(".,;:") in EXCLUDE for p in parts):
        return
    bag.add(v)


RE_COMB = re.compile(r"\b(?:\d\s){4,}\d\b")


def normalise_combs(text):
    """PDF comb fields (A-number, SSN, ZIP) extract as '2 1 4 8 6 6 4 5 6'.
    Collapse them so the number patterns can see them."""
    return RE_COMB.sub(lambda m: re.sub(r"\s+", "", m.group(0)), text)


def harvest_text(bag, text):
    text = normalise_combs(text)
    for m in RE_EMAIL.finditer(text):
        emit(bag, m.group(0), forced=True)
    for m in RE_DOMAIN.finditer(text):
        emit(bag, m.group(0))
    for pat in NUMBER_PATTERNS:
        for m in pat.finditer(text):
            emit(bag, m.group(0), forced=True)
            digits = re.sub(r"\D", "", m.group(0))
            if len(digits) >= 5:
                emit(bag, digits, forced=True)
    for m in RE_STREET.finditer(text):
        emit(bag, m.group(0), forced=True)
    # names in an unambiguous name context are never filtered
    for m in RE_HEADER_NAME.finditer(text):
        raw = m.group(1)
        raw = re.sub(r"<[^>]*>", " ", raw)
        for chunk in re.split(r"[,;]", raw):
            chunk = chunk.strip().strip('"')
            if chunk and RE_PROPER.fullmatch(chunk or ""):
                emit(bag, chunk, forced=True)
                for tok in chunk.split():
                    emit(bag, tok, forced=True)
    for m in RE_HONORIFIC.finditer(text):
        emit(bag, m.group(1).strip(), forced=True)
    for m in RE_PROPER.finditer(text):
        phrase = m.group(0)
        emit(bag, phrase)
        toks = phrase.split()
        if len(toks) > 1:
            for tok in toks:
                emit(bag, tok)


def harvest_pathname(bag, name):
    stem = re.sub(r"\.[A-Za-z0-9]{1,5}$", "", name)
    # corpus folder convention: surname_forename
    if re.fullmatch(r"[a-z]+_[a-z]+", stem):
        for part in stem.split("_"):
            emit(bag, part.capitalize(), forced=True)
        return
    # email export convention: NNNNNN_YYYY-MM-DD_slug
    stem = re.sub(r"^\d{6}_\d{4}-\d{2}-\d{2}_", "", stem)
    for tok in re.split(r"[^\w'’-]+", stem):
        if not tok:
            continue
        if tok[:1].isupper():
            emit(bag, tok)
        elif re.fullmatch(r"\d{5,}", tok):
            emit(bag, tok, forced=True)


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--lab", default=os.path.abspath(
        os.path.join(here, "..", "..")))
    ap.add_argument("--out", default=os.path.abspath(
        os.path.join(here, "..", "blocklist.txt")))
    ap.add_argument("--no-ocr", action="store_true",
                    help="skip the OCR pass over image-only PDFs "
                         "(the cache in .ocr-cache/ is still used)")
    args = ap.parse_args()

    bag = set()
    n_files = n_names = n_ocr = 0
    for root, dirs, files in os.walk(args.lab):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIR_NAMES)
        for d in dirs:
            harvest_pathname(bag, d)
            n_names += 1
        for fn in sorted(files):
            if fn in SKIP_FILE_NAMES:
                continue
            harvest_pathname(bag, fn)
            n_names += 1
            if fn.endswith(TEXT_SUFFIXES):
                path = os.path.join(root, fn)
                try:
                    with open(path, encoding="utf-8", errors="replace") as fh:
                        body = fh.read()
                except OSError as exc:            # pragma: no cover
                    print(f"warn: {path}: {exc}", file=sys.stderr)
                    continue
                harvest_text(bag, body)
                n_files += 1
                # image-only PDF: the sidecar is a stub, so OCR the page
                if NO_TEXT_MARKER in body and fn.endswith(".pdf.txt"):
                    pdf = path[:-4]
                    if os.path.exists(pdf) and not args.no_ocr:
                        text = ocr_pdf(pdf)
                        if text:
                            harvest_text(bag, text)
                            n_ocr += 1

    for k in KEEP_ALWAYS:
        bag.add(k)

    tokens = sorted(bag, key=lambda s: (s.lower(), s))
    with open(args.out, "w", encoding="utf-8") as fh:
        for t in tokens:
            fh.write(t + "\n")

    print(f"read {n_files} text files, {n_names} path names, "
          f"{n_ocr} image-only PDFs via OCR")
    print(f"wrote {len(tokens)} tokens -> {args.out}")


if __name__ == "__main__":
    main()
