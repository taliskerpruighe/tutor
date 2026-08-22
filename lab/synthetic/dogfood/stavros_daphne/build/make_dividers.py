#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

OUT = "/home/talisker/garage/tools/tutor/.claude/worktrees/challenges-spike-002/lab/synthetic/dogfood/stavros_daphne/build/pdf"
os.makedirs(OUT, exist_ok=True)

dividers = [
    ("A-1", 1, "TABLE OF CONTENTS"),
    ("A-2", 2, "COVER LETTER"),
    ("B-3", 3, "FORM N-400"),
    ("B-4", 4, "PASSPORT"),
    ("B-5", 5, "PERMANENT RESIDENT CARD"),
    ("B-6", 6, "2024 INCOME TAX RETURN"),
    ("B-7", 7, "TRAVEL ADDENDUM"),
    ("B-8", 8, "WRITTEN EXPLANATION"),
]

W, H = letter
for code, num, label in dividers:
    path = f"{OUT}/{code}.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Times-Bold", 16)
    c.drawCentredString(W / 2, H - 3.2 * 72, f"DOCUMENT {num}")
    c.setFont("Times-Bold", 22)
    c.drawCentredString(W / 2, H / 2, label)
    c.showPage()
    c.save()
    print("wrote", path)
