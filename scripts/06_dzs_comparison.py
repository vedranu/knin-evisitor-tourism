"""
06_dzs_comparison.py - Knin vs Šibenik-Knin County vs Croatia, monthly arrivals and overnight stays.
Data source: Croatian Bureau of Statistics PxWeb table BS_TU12 ("Dolasci i noćenja domaćih i stranih turista,
županije, mjesečno"). The script first tries to download the table through the PxWeb API (POST); if the
network is not available it reads data/external/dzs_tu12.csv (the same query exported manually from
https://web.dzs.hr/PXWeb/ -> Turizam -> Dolasci i noćenja ... -> Tablica 1.2, format CSV).
Outputs: outputs/dzs_comparison.csv, outputs/dzs_comparison.json, figures/bw/rev_dzs_index.png
"""
import os, json, io, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); P = lambda *a: os.path.join(ROOT, *a)
URL = "https://web.dzs.hr/PXWeb/api/v1/hr/Turizam/Dolasci%20i%20no%C4%87enja%20turista%20u%20komercijalnim%20smje%C5%A1tajnim%20objektima/BS_TU12.px"
QUERY = {"query": [
    {"code": "Županije", "selection": {"filter": "item", "values": ["00", "15"]}},
    {"code": "Mjesec", "selection": {"filter": "item", "values": [f"{m:02d}" for m in range(1, 13)]}},
    {"code": "Tip", "selection": {"filter": "item", "values": ["1", "2"]}},
    {"code": "Godina", "selection": {"filter": "item", "values": [str(y) for y in range(2016, 2027)]}},
    {"code": "Turisti", "selection": {"filter": "item", "values": ["0"]}}],
    "response": {"format": "csv"}}
dst = P("data/external/dzs_tu12.csv"); os.makedirs(P("data/external"), exist_ok=True)
if not os.path.exists(dst):
    try:
        import requests
        r = requests.post(URL, json=QUERY, timeout=60); r.raise_for_status()
        open(dst, "wb").write(r.content); print("downloaded", dst)
    except Exception as e:
        sys.exit(f"DZS data not available: {e}\nExport the table manually to {dst} (see docstring).")
raw = pd.read_csv(dst, encoding="utf-8-sig")
print(raw.head()); print(raw.columns.tolist())
# PxWeb CSV layout: first columns are the row dimensions, remaining columns the pivoted dimension(s).
# Normalise into long format: county, year, month, type, value.
id_cols = [c for c in raw.columns if raw[c].dtype == object][:4]
long = raw.melt(id_vars=id_cols, var_name="col", value_name="value")
long["value"] = pd.to_numeric(long["value"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")
long.to_csv(P("outputs/dzs_tu12_long.csv"), index=False)
print("Long table written; adapt the column mapping below to the exported layout if needed.")
# ---- mapping (adjust if the export layout differs) ----
col_map = {c: c for c in long.columns}
try:
    cty = [c for c in long.columns if "upanij" in c][0]; mon = [c for c in long.columns if "jesec" in c][0]
    typ = [c for c in long.columns if c.lower().startswith("tip")][0]
    yr = [c for c in long.columns if "odina" in c][0] if any("odina" in c for c in long.columns) else "col"
except IndexError:
    sys.exit("Could not identify columns automatically; edit col_map in the script.")
roman = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12}
long["month"] = long[mon].map(roman).fillna(pd.to_numeric(long[mon], errors="coerce"))
long["year"] = pd.to_numeric(long[yr].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
long = long.dropna(subset=["month", "year"])
long["area"] = np.where(long[cty].str.contains("HRVATSKA"), "Croatia", "Sibenik-Knin County")
long["type"] = np.where(long[typ].str.lower().str.startswith("dol"), "arrivals", "nights")
piv = long.pivot_table(index=["year", "month"], columns=["area", "type"], values="value", aggfunc="sum")
piv.columns = [f"{a}_{t}" for a, t in piv.columns]; piv = piv.reset_index()
piv["date"] = pd.to_datetime(dict(year=piv.year, month=piv.month, day=1))
knin = pd.read_csv(P("data/processed/monthly_totals.csv"), parse_dates=["date"])[["date", "arrivals", "nights"]].rename(columns={"arrivals": "Knin_arrivals", "nights": "Knin_nights"})
df = piv.merge(knin, on="date", how="inner").set_index("date").sort_index()
df.to_csv(P("outputs/dzs_comparison.csv"))
# annual indices 2019 = 100 and growth 2019->2025, 2022->2025
ann = df.groupby(df.index.year).sum(numeric_only=True).drop(columns=["year", "month"], errors="ignore")
idx = ann.div(ann.loc[2019]) * 100
res = {"index_2019_100": idx.round(1).to_dict(), "growth_2019_2025_pct": ((ann.loc[2025] / ann.loc[2019] - 1) * 100).round(1).to_dict(),
       "growth_2022_2025_pct": ((ann.loc[2025] / ann.loc[2022] - 1) * 100).round(1).to_dict()}
json.dump(res, open(P("outputs/dzs_comparison.json"), "w"), indent=2); print(json.dumps(res, indent=1))
fig, ax = plt.subplots(figsize=(7, 3.5))
for col, ls, mk in [("Knin_arrivals", "-", "o"), ("Sibenik-Knin County_arrivals", "--", "s"), ("Croatia_arrivals", ":", "^")]:
    ax.plot(idx.index, idx[col], color="#000000", ls=ls, marker=mk, ms=4, label=col.replace("_arrivals", "").replace("Sibenik", "Šibenik"))
ax.axhline(100, color="#888888", lw=0.8); ax.set_ylabel("Arrivals, index 2019 = 100"); ax.legend(fontsize=8)
fig.savefig(P("figures/bw/rev_dzs_index.png"), dpi=300, bbox_inches="tight"); print("DONE")
