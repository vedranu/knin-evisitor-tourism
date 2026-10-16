"""04_build_thm.py - builds the Tourism and Hospitality Management (THM) submission file:
pandoc renders paper/paper_thm_body.md with the THM reference styles, then python-docx adds the
title, the author/abstract block and the author biographies required by the journal template."""
import subprocess, os, copy
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "..", "paper")
os.chdir(P)
subprocess.run(["pandoc", "paper_thm_body.md", "-o", "_thm_body.docx", "--resource-path=.", "--columns=60", "--reference-doc=thm_reference.docx"], check=True)

TITLE = 'FROM TRANSIT STOP TO DESTINATION? A DECADE OF E-VISITOR DATA ON TOURISM GROWTH, SEASONALITY, SOURCE MARKETS AND PROJECTIONS FOR KNIN, CROATIA'
AUTHORS = [
    dict(name="Vedran UROŠ", corr=True, orcid="https://orcid.org/0009-0007-6568-0827",
         inst=['University of Applied Sciences "Marko Marulić" in Knin', 'Faculty of Organization and Informatics, University of Zagreb'], country="Croatia", email="vuros@veleknin.hr"),
    dict(name="[Name SURNAME of co-author Sorić]", corr=False, orcid="https://orcid.org/[to be added]", inst=["[Institution]"], country="Croatia", email="[e-mail address]"),
]
ABSTRACT = [
    ("Purpose", "The paper examines how tourism in Knin, a small town in the Dalmatian hinterland, developed during the first decade of Croatia's e-Visitor system, whether growth changed its seasonality and source-market structure, and what the data imply for 2030."),
    ("Methodology/Design/Approach", "The complete monthly e-Visitor record (January 2016 to September 2026, 129 months, 75 markets) is analysed with STL decomposition, Gini coefficients of seasonality, Herfindahl-Hirschman indices, Bai-Perron break estimation, Chow tests, and SARIMA, ETS and Holt-Winters models validated on a 21-month hold-out and projected to 2030."),
    ("Findings", "Arrivals grew from 1,404 (2016) to 6,178 (2025) and overnight stays from 3,456 to 12,558, with the regime shift dated to 2022-2023 rather than the pandemic. Seasonality did not fall; the summer peak flattened into a longer summer. Foreign demand diversified across 12-17 effective markets, but average stay fell to two nights. Growth stalled in 2026, so projections to 2030 range from a plateau of 5,800 arrivals to 12,200."),
    ("Originality of the research", "First decade-long monthly analysis of a single Croatian inland destination, with open data and code."),
]
KEYWORDS = "tourism demand, seasonality, source markets, structural break, forecasting, Croatia"
BIOS = [
    'Vedran Uroš is a senior lecturer at the University of Applied Sciences "Marko Marulić" in Knin, where he is acting vice-dean for research and international cooperation, and a doctoral candidate at the Faculty of Organization and Informatics, University of Zagreb. His research covers energy-efficient wireless sensor networks and UAV-assisted data collection, as well as applied data analysis in tourism and regional development. [complete to max. 100 words]',
    '[Co-author Sorić: professional biography of no more than 100 words to be added]',
]

doc = Document("_thm_body.docx")
body = doc.element.body
first = body[0]

def para_before(ref, text="", style=None, bold=False, italic=False, size=None, align=None, font="Times New Roman"):
    p = doc.add_paragraph(); ref.addprevious(p._p)
    if style: p.style = doc.styles[style]
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.name = font
        if size: r.font.size = Pt(size)
    if align is not None: p.alignment = align
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.space_before = Pt(0)
    return p

def set_cell_borders(cell, val="nil"):
    tcPr = cell._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders")
    for e in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{e}"); el.set(qn("w:val"), val); b.append(el)
    tcPr.append(b)

# title
tp = para_before(first, TITLE, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.LEFT, font="Arial"); tp.paragraph_format.space_after = Pt(12)
# author / abstract table
tbl = doc.add_table(rows=1, cols=2); first.addprevious(tbl._tbl)
tbl.autofit = False
left, right = tbl.rows[0].cells
left.width = Cm(5.2); right.width = Cm(12.4)
for c in (left, right): set_cell_borders(c)
left.paragraphs[0].text = ""
def add_p(cell, text, bold=False, italic=False, size=9, after=2, prefix_italic=None):
    p = cell.add_paragraph(); p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(0)
    if prefix_italic:
        r = p.add_run(prefix_italic); r.italic = True; r.font.size = Pt(size); r.font.name = "Times New Roman"
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size); r.font.name = "Times New Roman"
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if cell is right else WD_ALIGN_PARAGRAPH.LEFT
    return p
for a in AUTHORS:
    add_p(left, a["name"] + (", " if a["corr"] else ""), bold=True, size=10, after=0)
    if a["corr"]: add_p(left, "Corresponding Author", size=9, after=0)
    add_p(left, a["orcid"], size=9, after=0)
    for i in a["inst"]: add_p(left, i, size=9, after=0)
    add_p(left, a["country"], size=9, after=0)
    add_p(left, a["email"], size=9, after=8)
right.paragraphs[0].text = ""
add_p(right, "Abstract", bold=True, size=10, after=4)
for k, v in ABSTRACT: add_p(right, " - " + v, size=9, after=4, prefix_italic=k)
kp = add_p(right, KEYWORDS, size=9, after=0); r0 = kp.runs[0]; r0.text = " " + KEYWORDS; rk = copy.deepcopy(r0._r); kp._p.insert(list(kp._p).index(r0._r), rk); kp.runs[0].text = "Keywords"; kp.runs[0].bold = True
# empty paragraph after table
para_before(first, "")

# biographies at end: one-column bordered table
bt = doc.add_table(rows=len(BIOS), cols=1); bt.style = doc.styles["Table Grid"] if "Table Grid" in [s.name for s in doc.styles] else bt.style
for i, b in enumerate(BIOS):
    c = bt.rows[i].cells[0]; c.paragraphs[0].text = ""
    p = c.paragraphs[0]; r = p.add_run(b); r.font.size = Pt(9); r.font.name = "Times New Roman"; p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
# keep table/figure captions with the following element
for p in doc.paragraphs:
    t = p.text.strip()
    if (t.startswith("Table ") or t.startswith("Figure ")) and ":" in t[:12]:
        p.paragraph_format.keep_with_next = True
# remove page numbers if any (none in reference) and save
doc.save("Knin_THM_submission.docx"); os.remove("_thm_body.docx")
print("written paper/Knin_THM_submission.docx")
