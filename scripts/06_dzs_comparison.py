"""
06_dzs_comparison.py - Knin vs Šibenik-Knin County vs Croatia, monthly arrivals and overnight stays.
Source: Croatian Bureau of Statistics, PxWeb table BS_TU12 "Dolasci i noćenja domaćih i stranih turista,
županije, mjesečno" (commercial accommodation, all tourists), retrieved 16 Oct 2026 through the PxWeb API
(query in data/external/dzs_tu12_query.json); saved as data/external/dzs_tu12.csv
(columns: county code 00 = Croatia, 15 = Šibenik-Knin; month; type 1 = arrivals, 2 = nights; year; value).
Outputs: outputs/dzs_comparison_annual.csv, outputs/dzs_comparison.json, figures/bw/rev_dzs_index.png
"""
import os, json
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import statsmodels.api as sm
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); P = lambda *a: os.path.join(ROOT, *a)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e5e1", "axes.axisbelow": True, "legend.frameon": False})
d = pd.read_csv(P("data/external/dzs_tu12.csv"), sep=";", dtype=str)
d["value"] = pd.to_numeric(d["value"], errors="coerce"); d = d.dropna(subset=["value"])
d["area"] = d.county.map({"00": "Croatia", "15": "County"}); d["type"] = d.type.map({"1": "arrivals", "2": "nights"})
d["date"] = pd.to_datetime(dict(year=d.year.astype(int), month=d.month.astype(int), day=1))
w = d.pivot_table(index="date", columns=["area", "type"], values="value").sort_index()
w.columns = [f"{a}_{t}" for a, t in w.columns]
knin = pd.read_csv(P("data/processed/monthly_totals.csv"), parse_dates=["date"]).set_index("date")[["arrivals", "nights"]].rename(columns=lambda c: f"Knin_{c}")
df = w.join(knin, how="inner")   # Jan 2016 - Aug 2026 (DZS 2026 available to August)
df.to_csv(P("outputs/dzs_comparison_monthly.csv"))
full = df[df.index.year <= 2025]
ann = full.groupby(full.index.year).sum()
idx = (ann.div(ann.loc[2019]) * 100).round(1)
R = {"index_2019_100": idx.to_dict(),
     "growth_2016_2019_pct": ((ann.loc[2019] / ann.loc[2016] - 1) * 100).round(1).to_dict(),
     "growth_2019_2025_pct": ((ann.loc[2025] / ann.loc[2019] - 1) * 100).round(1).to_dict(),
     "growth_2022_2025_pct": ((ann.loc[2025] / ann.loc[2022] - 1) * 100).round(1).to_dict(),
     "cagr_2021_2025_pct": (((ann.loc[2025] / ann.loc[2021]) ** 0.25 - 1) * 100).round(1).to_dict()}
# Jan-Aug 2026 vs Jan-Aug 2025
ja = df[(df.index.month <= 8) & (df.index.year >= 2025)]; ja = ja.groupby(ja.index.year).sum()
R["growth_JanAug_2026_vs_2025_pct"] = ((ja.loc[2026] / ja.loc[2025] - 1) * 100).round(1).to_dict()
# Knin share of county arrivals (%) by year
share = (ann["Knin_arrivals"] / ann["County_arrivals"] * 100).round(2); R["knin_share_of_county_arrivals_pct"] = share.to_dict()
share_n = (ann["Knin_nights"] / ann["County_nights"] * 100).round(2); R["knin_share_of_county_nights_pct"] = share_n.to_dict()
# relative growth regression: log(Knin/County) on time, pre (2016-2019) and post (2021-2025), annual
rel = np.log(ann["Knin_arrivals"] / ann["County_arrivals"])
for lab, yrs in [("pre_2016_2019", range(2016, 2020)), ("post_2021_2025", range(2021, 2026))]:
    y = rel.loc[list(yrs)]; X = sm.add_constant(np.arange(len(y))); m = sm.OLS(y.values, X).fit()
    R[f"relative_growth_{lab}_pct_per_year"] = float((np.exp(m.params[1]) - 1) * 100); R[f"relative_growth_{lab}_p"] = float(m.pvalues[1])
# monthly relative index 2019 = 100 (12-month rolling sums) for the figure
roll = df.rolling(12).sum().dropna()
base = roll.loc["2019-12-01"]; ri = roll.div(base) * 100
fig, ax = plt.subplots(figsize=(7.5, 3.6))
for col, ls, lab in [("Knin_arrivals", "-", "Knin (e-Visitor)"), ("County_arrivals", "--", "Šibenik-Knin County (CBS)"), ("Croatia_arrivals", ":", "Croatia (CBS)")]:
    ax.plot(ri.index, ri[col], color="#000000", ls=ls, lw=1.5, label=lab)
ax.axhline(100, color="#888888", lw=0.8); ax.set_ylabel("Rolling 12-month arrivals, Dec 2019 = 100"); ax.legend(fontsize=8, loc="upper left"); ax.margins(x=0.01)
fig.savefig(P("figures/bw/rev_dzs_index.png"), dpi=300, bbox_inches="tight"); plt.close()
tab = pd.DataFrame({"Knin arrivals": idx["Knin_arrivals"], "County arrivals": idx["County_arrivals"], "Croatia arrivals": idx["Croatia_arrivals"],
                    "Knin nights": idx["Knin_nights"], "County nights": idx["County_nights"], "Croatia nights": idx["Croatia_nights"], "Knin share of county arrivals (%)": share})
tab.to_csv(P("outputs/dzs_comparison_annual.csv")); print(tab)
json.dump(R, open(P("outputs/dzs_comparison.json"), "w"), indent=2, default=float); print(json.dumps(R, indent=1, default=float))
