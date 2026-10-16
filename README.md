# Knin e-Visitor tourism data and analysis, 2016-2026

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23426318.svg)](https://doi.org/10.5281/zenodo.23426318)

Reproducible data set and code for the paper

> Uroš, V., Ćaćić, M., & Sorić, I. (2026). *From transit stop to destination? A decade of e-Visitor data on tourism growth, seasonality, source-market structure and projections for Knin, Croatia (2016-2026).* Manuscript.

The repository contains the complete monthly record of the Croatian e-Visitor registration system for the area of the Tourist Board of the Town of Knin (January 2016 to September 2026): tourist arrivals, overnight stays and number of tourists by country of origin (75 reported markets), together with the Python code that builds the consolidated data set, runs every statistical analysis and produces every table and figure in the paper.

## Repository structure

```
data/raw/EVISITOR GODINE/      original e-Visitor exports (xlsx), one file per month and per year, as received
data/processed/
    evisitor_knin_long.csv     long format: year, month, span (month|year), country, arrivals, nights, tourists, source file
    monthly_totals.csv         monthly totals: arrivals, nights, tourists, domestic/foreign split (129 months)
scripts/
    01_build_database.py       parses every xlsx by the date parameters stored inside the file, checks totals, imputes May 2017
    02_analysis.py             descriptive statistics, STL, Gini seasonality, HHI, structural breaks, SARIMA/ETS/Holt-Winters
                               with out-of-sample validation, projections to 2030, all figures
    03_build_paper.sh          builds the Word version of the paper from the manuscript sources (not distributed)
outputs/                       all tables (CSV) and results.json with every number quoted in the paper
figures/                       all figures (PNG, 300 dpi)
paper/
    reference.docx, thm_reference.docx   pandoc style templates; the manuscript sources are not distributed
```

## Reproduce

```bash
pip install -r requirements.txt
python scripts/01_build_database.py     # ~5 s
python scripts/02_analysis.py           # ~4 min (SARIMA grid search)
bash scripts/03_build_paper.sh          # needs pandoc
```

Python 3.11+ is required. Tested with Python 3.13, pandas 2.x, statsmodels 0.15, ruptures 1.1, pyCirclize 1.10.

## Data notes

* Source: e-Visitor (Hrvatska turistička zajednica), reports "DrzavaTurista" exported by the Tourist Board of the Town of Knin in September 2026. Level: Šibensko-kninska - Knin; all accommodation types; tourists only (no excursionists); all billing categories.
* The month of each file is taken from the `Od datuma / Do datuma` parameters inside the file, not from the file name, because several files are mislabelled (e.g. `2025/10. Listopad 2026.xlsx` contains October 2025; `2017/5.svibanj 2017.xlsx` contains an April 2017 export).
* No valid monthly export exists for May 2017. May 2017 is imputed per country as (2017 annual report) minus (sum of the other 11 months); the imputed rows are flagged in the `file` column of `evisitor_knin_long.csv`. Four small negative tourist counts produced by the subtraction were clipped to zero (arrivals and nights were unaffected).
* Monthly sums for every other year reproduce the annual reports exactly (see `outputs/01_build_log.txt`).
* 2026 covers January-September only and may be revised by late registrations.

## Licence

* Code (`scripts/`): MIT License.
* Processed data (`data/processed/`), outputs and figures: Creative Commons Attribution 4.0 (CC BY 4.0). Please cite the paper and acknowledge the Tourist Board of the Town of Knin and e-Visitor as the primary source.
* Raw e-Visitor exports (`data/raw/`) are redistributed with the permission of the Tourist Board of the Town of Knin for research purposes.

## Citation

Archived on Zenodo: version 1.0.1 DOI https://doi.org/10.5281/zenodo.23426318 (concept DOI for all versions: https://doi.org/10.5281/zenodo.23426164).

> Uroš, V., Ćaćić, M., & Sorić, I. (2026). *Knin e-Visitor tourism data and analysis, 2016-2026: data, code and figures* (Version 1.0.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23426318

See also `CITATION.cff`.

## Journal submission version

`scripts/05_revision.py` adds the review-stage analyses (segmented-trend breaks with bootstrap inference, simulated annual prediction intervals, rolling-origin cross-validation); `scripts/06_dzs_comparison.py` compares Knin with Šibenik-Knin County and Croatia using Croatian Bureau of Statistics table BS_TU12 (`data/external/`). `scripts/04_build_thm.py` builds the manuscript formatted for *Tourism and Hospitality Management* (Times New Roman 10 pt, A4, structured abstract, black-and-white figures from `figures/bw/`, APA 7; `ANON=1` builds the anonymised version for blind review). The black-and-white figures are produced by `BW=1 python scripts/02_analysis.py`. The manuscript text is under review and is not part of this repository.
