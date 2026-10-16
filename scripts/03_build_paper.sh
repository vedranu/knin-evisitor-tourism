#!/usr/bin/env bash
# Builds the Word version of the manuscript from paper/paper.md (requires pandoc).
set -e
cd "$(dirname "$0")/../paper"
pandoc paper.md -o Knin_eVisitor_tourism_paper.docx --resource-path=. --columns=60 --reference-doc=reference.docx
pandoc paper_hr.md -o Knin_eVisitor_turizam_rad_HR.docx --resource-path=. --columns=60 --reference-doc=reference.docx -M lang=hr
echo "written paper/Knin_eVisitor_tourism_paper.docx and paper/Knin_eVisitor_turizam_rad_HR.docx"
