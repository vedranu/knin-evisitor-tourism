#!/usr/bin/env bash
# Builds the Word version of the manuscript from paper/paper.md (requires pandoc).
set -e
cd "$(dirname "$0")/../paper"
pandoc paper.md -o Knin_eVisitor_tourism_paper.docx --resource-path=. --columns=60
echo "written paper/Knin_eVisitor_tourism_paper.docx"
