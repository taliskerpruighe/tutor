#!/usr/bin/env python3
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

BLANK = "/home/talisker/garage/tools/tutor/.claude/worktrees/challenges-spike-002/lab/synthetic/blanks/n-400.pdf"
OUT = "/home/talisker/garage/tools/tutor/.claude/worktrees/challenges-spike-002/lab/synthetic/dogfood/stavros_daphne/build/pdf/B-3. Form N-400, Application for Naturalization.pdf"

reader = PdfReader(BLANK)
writer = PdfWriter()
writer.append(reader)

P = "form1[0]."

values = {
    # Part 1 - eligibility basis: A = General Provision (5-year rule)
    f"{P}#subform[0].Part1_Eligibility[2]": "/A",
    f"{P}#subform[0].#area[0].Line1_AlienNumber[0]": "207115634",
    f"{P}#subform[0].P2_Line1_FamilyName[0]": "Stavros",
    f"{P}#subform[0].P2_Line1_GivenName[0]": "Konstantinos",

    # Part 2 - biographic
    f"{P}#subform[1].#area[1].Line1_AlienNumber[1]": "207115634",
    f"{P}#subform[1].P2_Line8_DateOfBirth[0]": "04/12/1957",
    f"{P}#subform[1].P2_Line7_Gender[0]": "/M",
    f"{P}#subform[1].P2_Line9_DateBecamePermanentResident[0]": "01/23/2020",
    f"{P}#subform[1].P2_Line11_CountryOfNationality[0]": "Greece",
    f"{P}#subform[1].P2_Line10_CountryOfBirth[0]": "Greece",
    f"{P}#subform[1].P2_Line10_claimdisability[0]": "/N",
    f"{P}#subform[1].P2_Line11_claimdisability[0]": "/N",
    f"{P}#subform[1].P2_Line34_NameChange[0]": "/N",
    f"{P}#subform[1].Line12a_Checkbox[1]": "/Y",
    f"{P}#subform[1].Line12b_SSN[0]": "148927350",
    f"{P}#subform[1].Line12\\.c_Checkbox[0]": "/N",

    # Part 3 - biographic (ethnicity/race/height/weight/eye/hair)
    f"{P}#subform[2].#area[2].Line1_AlienNumber[2]": "207115634",
    f"{P}#subform[2].P7_Line1_Ethnicity[0]": "/N",
    f"{P}#subform[2].P7_Line2_Race[4]": "/W",
    f"{P}#subform[2].P7_Line3_HeightFeet[0]": "5",
    f"{P}#subform[2].P7_Line3_HeightInches[0]": "8",
    f"{P}#subform[2].P7_Line4_Pounds1[0]": "1",
    f"{P}#subform[2].P7_Line4_Pounds2[0]": "7",
    f"{P}#subform[2].P7_Line4_Pounds3[0]": "6",
    f"{P}#subform[2].P7_Line5_Eye[0]": "/BRO",
    f"{P}#subform[2].P7_Line6_Hair[4]": "/GRY",

    # Part 4 - addresses (current first, then prior)
    f"{P}#subform[2].P4_Line1_Number[0]": "74",
    f"{P}#subform[2].P4_Line1_StreetName[0]": "Fern Hollow Road",
    f"{P}#subform[2].P4_Line1_City[0]": "Montclair",
    f"{P}#subform[2].P4_Line1_State[0]": " NJ",
    f"{P}#subform[2].P4_Line1_ZipCode[0]": "07042",
    f"{P}#subform[2].P4_Line1_Country[0]": "United States",
    f"{P}#subform[2].P4_Line1_DatesofResidence[0]": "PRESENT",
    f"{P}#subform[2].P4_Line1_DatesofResidence[1]": "08/15/2024",
    f"{P}#subform[2].Pt3_Line2a_Checkbox[1]": "/Y",

    f"{P}#subform[2].P4_Line3_PhysicalAddress1[0]": "231 Ridgeline Avenue",
    f"{P}#subform[2].P4_Line3_CityTown1[0]": "Bloomfield",
    f"{P}#subform[2].P4_Line3_State1[0]": "NJ",
    f"{P}#subform[2].P4_Line3_ZipCode1[0]": "07003",
    f"{P}#subform[2].P4_Line3_Country1[0]": "United States",
    f"{P}#subform[2].P4_Line3_From1[0]": "PRESENT",  # placeholder, overwritten below
    f"{P}#subform[2].P4_Line3_From1[1]": "08/14/2024",

    # Part 5/6 - marital status & employment
    f"{P}#subform[3].#area[3].Line1_AlienNumber[3]": "207115634",
    f"{P}#subform[3].Part9Line3_TimesMarried[0]": "1",
    f"{P}#subform[3].P10_Line1_MaritalStatus[2]": "/W",

    f"{P}#subform[4].#area[4].Line1_AlienNumber[4]": "207115634",
    f"{P}#subform[4].P11_Line1_TotalChildren[0]": "0",
    f"{P}#subform[4].P5_EmployerName1[0]": "Retired",
    f"{P}#subform[4].P5_EmployerName2[0]": "Bellwether Baking Company",
    f"{P}#subform[4].P7_City1[0]": "Montclair",
    f"{P}#subform[4].P7_City2[0]": "Bloomfield",
    f"{P}#subform[4].P7_State1[0]": "NJ",
    f"{P}#subform[4].P7_State2[0]": "NJ",
    f"{P}#subform[4].P7_ZipCode1[0]": "07042",
    f"{P}#subform[4].P7_ZipCode2[0]": "07003",
    f"{P}#subform[4].P7_Country1[0]": "United States",
    f"{P}#subform[4].P7_Country2[0]": "United States",
    f"{P}#subform[4].P7_From1[1]": "07/01/2023",
    f"{P}#subform[4].P7_From2[1]": "03/07/2016",
    f"{P}#subform[4].P7_To2[0]": "06/30/2023",
    f"{P}#subform[4].P7_OccupationFieldStudy1[2]": "Retired",
    f"{P}#subform[4].P7_OccupationFieldStudy2[2]": "Baker",

    # Part 8 - travel history (6 most recent non-day trips; full list of 8 in Travel Addendum)
    f"{P}#subform[5].#area[6].Line1_AlienNumber[5]": "207115634",
    f"{P}#subform[5].P8_Line1_DateLeft1[0]": "11/02/2025",
    f"{P}#subform[5].P8_Line1_DateReturn1[0]": "11/20/2025",
    f"{P}#subform[5].P9_Line1_Countries1[0]": "Greece",
    f"{P}#subform[5].P8_Line1_DateLeft2[0]": "04/10/2025",
    f"{P}#subform[5].P8_Line1_DateReturn2[0]": "04/28/2025",
    f"{P}#subform[5].P8_Line1_Countries2[0]": "Greece",
    f"{P}#subform[5].P8_Line1_DateLeft3[0]": "09/05/2024",
    f"{P}#subform[5].P8_Line1_DateReturn3[0]": "09/22/2024",
    f"{P}#subform[5].P8_Line1_Countries3[0]": "Greece",
    f"{P}#subform[5].P8_Line1_DateLeft4[0]": "01/15/2024",
    f"{P}#subform[5].P8_Line1_DateReturn4[0]": "01/30/2024",
    f"{P}#subform[5].P8_Line1_Countries4[0]": "Greece",
    f"{P}#subform[5].P8_Line1_DateLeft5[0]": "06/01/2023",
    f"{P}#subform[5].P8_Line1_DateReturn5[0]": "06/20/2023",
    f"{P}#subform[5].P8_Line1_Countries5[0]": "Greece",
    f"{P}#subform[5].P8_Line1_DateLeft6[0]": "10/10/2022",
    f"{P}#subform[5].P8_Line1_DateReturn6[0]": "10/25/2022",
    f"{P}#subform[5].P8_Line1_Countries6[0]": "Greece",

    # Part 9 items 1-14 (defaults No, except 8a and 12 = Yes)
    f"{P}#subform[5].P9_Line1[0]": "/N",
    f"{P}#subform[5].P9_Line2[0]": "/N",
    f"{P}#subform[5].P9_Line3[1]": "/N",
    f"{P}#subform[5].P9_Line4[1]": "/N",
    f"{P}#subform[5].P9_5a[1]": "/N",
    f"{P}#subform[5].P9_5b[1]": "/N",

    f"{P}#subform[6].#area[7].Line1_AlienNumber[6]": "207115634",
    f"{P}#subform[6].P12_6a[0]": "/N",
    f"{P}#subform[6].P12_6b[1]": "/N",
    f"{P}#subform[6].P12_6c[0]": "/N",
    f"{P}#subform[6].P9_Line7a[0]": "/N",
    f"{P}#subform[6].P9_Line7\\.b\\.[0]": "/N",
    f"{P}#subform[6].P9_Line7\\.c[0]": "/N",
    f"{P}#subform[6].P11_7d[0]": "/N",
    f"{P}#subform[6].P9_Line7\\.e[0]": "/N",
    f"{P}#subform[6].P9_Line7\\.f[0]": "/N",
    f"{P}#subform[6].P9_Line7\\.g[0]": "/N",
    f"{P}#subform[6].P9_Line8a[1]": "/Y",
    f"{P}#subform[6].P9_Line8b[0]": "/N",
    f"{P}#subform[6].P9_Line9[0]": "/N",
    f"{P}#subform[6].P9_Line10a[0]": "/N",
    f"{P}#subform[6].P9_Line10b[0]": "/N",
    f"{P}#subform[6].P9_Line10c[1]": "/N",
    f"{P}#subform[6].P9_Line11[0]": "/N",
    f"{P}#subform[6].P9_Line12[1]": "/Y",
    f"{P}#subform[6].P9_Line13[0]": "/N",
    f"{P}#subform[6].P9_Line14[0]": "/N",

    # Part 9 items 15-19 (no crime/arrest)
    f"{P}#subform[7].#area[8].Line1_AlienNumber[7]": "207115634",
    f"{P}#subform[7].P9_Line15a[0]": "/N",
    f"{P}#subform[7].P9_Line15b[0]": "/N",

    # Part 9 items 17-25 (removal proceedings = Yes at item 20)
    f"{P}#subform[8].#area[9].Line1_AlienNumber[8]": "207115634",
    f"{P}#subform[8].P11_Line17A[0]": "/N",
    f"{P}#subform[8].P11_Line17B[0]": "/N",
    f"{P}#subform[8].P11_Line17C[0]": "/N",
    f"{P}#subform[8].P12_Line17d[0]": "/N",
    f"{P}#subform[8].P12_Line17e[0]": "/N",
    f"{P}#subform[8].P12_Line17f[1]": "/N",
    f"{P}#subform[8].P12_Line17g[0]": "/N",
    f"{P}#subform[8].P12_Line17h[0]": "/N",
    f"{P}#subform[8].P12_Line18[1]": "/N",
    f"{P}#subform[8].P12_Line19[1]": "/N",
    f"{P}#subform[8].P12_Line20[1]": "/Y",
    f"{P}#subform[8].P12_Line21[0]": "/N",
    f"{P}#subform[8].P9_Line22a[0]": "/N",
    f"{P}#subform[8].P12_Line23[0]": "/N",
    f"{P}#subform[8].P12_Line24[0]": "/N",
    f"{P}#subform[8].P12_Line25[0]": "/N",

    # Part 9 items 26-37 (military/civic)
    f"{P}#subform[9].#area[10].Line1_AlienNumber[9]": "207115634",
    f"{P}#subform[9].P12_Line26a[0]": "/N",
    f"{P}#subform[9].P11_Line26d[0]": "/N",
    f"{P}#subform[9].P12_Line27[1]": "/N",
    f"{P}#subform[9].P12_Line28[1]": "/N",
    f"{P}#subform[9].P9_Line29[0]": "/N",
    f"{P}#subform[9].P12_Line30a[1]": "/N",
    f"{P}#subform[9].P12_Line30b[1]": "/N",
    f"{P}#subform[9].P12_Line31[1]": "/Y",
    f"{P}#subform[9].P12_Line32[0]": "/Y",
    f"{P}#subform[9].P12_Line33[1]": "/N",
    f"{P}#subform[9].P12_Line34[1]": "/Y",
    f"{P}#subform[9].P12_Line35[0]": "/Y",
    f"{P}#subform[9].P12_Line36[1]": "/Y",
    f"{P}#subform[9].P12_Line37[0]": "/Y",

    # Part 12 - contact info
    f"{P}#subform[10].#area[11].Line1_AlienNumber[10]": "207115634",
    f"{P}#subform[10].P12_Line3_Telephone[0]": "(973) 555-0155",
    f"{P}#subform[10].P12_Line3_Mobile[0]": "(973) 555-0155",
    f"{P}#subform[10].P12_Line5_Email[0]": "k.stavros@quillmail.com",
    f"{P}#subform[10].P10_Line1_Citizen[0]": "/N",

    f"{P}#subform[11].#area[12].Line1_AlienNumber[11]": "207115634",
    f"{P}#subform[12].#area[13].Line1_AlienNumber[12]": "207115634",
    f"{P}#subform[13].#area[14].Line1_AlienNumber[13]": "207115634",
}

# The 'From1[0]' placeholder above should not be set to PRESENT (that's the Line1 present-address
# field); the prior address doesn't need a from-placeholder here beyond the actual date value.
del values[f"{P}#subform[2].P4_Line3_From1[0]"]
values[f"{P}#subform[2].P4_Line3_From1[0]"] = "05/20/2011"

for page in writer.pages:
    writer.update_page_form_field_values(page, values, auto_regenerate=False)

# Ensure viewers regenerate field appearances
try:
    writer.set_need_appearances_writer(True)
except Exception:
    root = writer._root_object
    if "/AcroForm" in root:
        root["/AcroForm"][NameObject("/NeedAppearances")] = __import__("pypdf").generic.BooleanObject(True)

with open(OUT, "wb") as f:
    writer.write(f)

print("wrote", OUT)
