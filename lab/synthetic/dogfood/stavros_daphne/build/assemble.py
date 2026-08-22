#!/usr/bin/env python3
import os
import shutil
from pypdf import PdfWriter, PdfReader

ROOT = "/home/talisker/garage/tools/tutor/.claude/worktrees/challenges-spike-002/lab/synthetic/dogfood/stavros_daphne"
BUILD_DOCX = f"{ROOT}/build/docx"
BUILD_PDF = f"{ROOT}/build/pdf"
OUT = f"{ROOT}/output"

TAB_A = f"{OUT}/Tab A (Content + Cover)"
TAB_B = f"{OUT}/Tab B (Biographical Info)"

for d in [OUT, TAB_A, TAB_B]:
    os.makedirs(d, exist_ok=True)

def cp(src_name, dst_dir, dst_name=None):
    dst_name = dst_name or src_name
    shutil.copy(f"{BUILD_PDF}/{src_name}", f"{dst_dir}/{dst_name}")

def cp_docx(name, dst_dir):
    shutil.copy(f"{BUILD_DOCX}/{name}", f"{dst_dir}/{name}")

# --- root: Applicant Cover Page ---
cp_docx("00. Applicant Cover Page.docx", OUT)
cp("00. Applicant Cover Page.pdf", OUT)

# --- Tab A ---
cp_docx("A-0. Tab Cover Page.docx", TAB_A)
cp("A-0. Tab Cover Page.pdf", TAB_A)

cp("A-1.pdf", TAB_A)
cp_docx("A-1. Table of Contents.docx", TAB_A)
cp("A-1. Table of Contents.pdf", TAB_A)

cp("A-2.pdf", TAB_A)
cp_docx("A-2. Cover Letter.docx", TAB_A)
cp("A-2. Cover Letter.pdf", TAB_A)

# --- Tab B ---
cp_docx("B-0. Tab Cover Page.docx", TAB_B)
cp("B-0. Tab Cover Page.pdf", TAB_B)

cp("B-3.pdf", TAB_B)
cp("B-3. Form N-400, Application for Naturalization.pdf", TAB_B)

cp("B-4.pdf", TAB_B)
cp("B-4. Bio Page of Passport.pdf", TAB_B)

cp("B-5.pdf", TAB_B)
cp("B-5. Permanent Resident Card.pdf", TAB_B)

cp("B-6.pdf", TAB_B)
cp("B-6. 2024 Income Tax Return.pdf", TAB_B)

cp("B-7.pdf", TAB_B)
cp_docx("B-7. Travel Addendum.docx", TAB_B)
cp("B-7. Travel Addendum.pdf", TAB_B)

cp("B-8.pdf", TAB_B)
cp_docx("B-8. Written Explanation.docx", TAB_B)
cp("B-8. Written Explanation.pdf", TAB_B)

# --- Merge the full packet ---
order = [
    f"{OUT}/00. Applicant Cover Page.pdf",
    f"{TAB_A}/A-0. Tab Cover Page.pdf",
    f"{TAB_A}/A-1.pdf",
    f"{TAB_A}/A-1. Table of Contents.pdf",
    f"{TAB_A}/A-2.pdf",
    f"{TAB_A}/A-2. Cover Letter.pdf",
    f"{TAB_B}/B-0. Tab Cover Page.pdf",
    f"{TAB_B}/B-3.pdf",
    f"{TAB_B}/B-3. Form N-400, Application for Naturalization.pdf",
    f"{TAB_B}/B-4.pdf",
    f"{TAB_B}/B-4. Bio Page of Passport.pdf",
    f"{TAB_B}/B-5.pdf",
    f"{TAB_B}/B-5. Permanent Resident Card.pdf",
    f"{TAB_B}/B-6.pdf",
    f"{TAB_B}/B-6. 2024 Income Tax Return.pdf",
    f"{TAB_B}/B-7.pdf",
    f"{TAB_B}/B-7. Travel Addendum.pdf",
    f"{TAB_B}/B-8.pdf",
    f"{TAB_B}/B-8. Written Explanation.pdf",
]

writer = PdfWriter()
for path in order:
    r = PdfReader(path)
    for page in r.pages:
        writer.add_page(page)

packet_path = f"{OUT}/N-400 Packet.pdf"
with open(packet_path, "wb") as f:
    writer.write(f)

print("Packet pages:", len(writer.pages))
print("wrote", packet_path)
