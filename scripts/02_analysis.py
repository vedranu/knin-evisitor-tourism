"""
02_analysis.py - descriptive statistics, seasonality, market concentration,
structural breaks, SARIMA/ETS forecasting with out-of-sample validation,
and scenario projections to 2030 for Knin (Croatia) e-Visitor data 2016-2026.
All results are written to outputs/ (tables, JSON) and figures/ (PNG, 300 dpi).
"""
import os, json, warnings
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import acorr_ljungbox
import statsmodels.api as sm
import ruptures as rpt
from scipy import stats, optimize
warnings.filterwarnings("ignore")

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = lambda *a: os.path.join(ROOT, *a)
BW = os.environ.get("BW") == "1"   # BW=1 renders black-and-white figures into figures/bw (journal requirement)
FIGDIR = "figures/bw" if BW else "figures"
os.makedirs(P(FIGDIR), exist_ok=True); os.makedirs(P("outputs"), exist_ok=True)

# ---------- palette (validated categorical palette, fixed order) ----------
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
if BW:
    CAT = ["#1a1a1a", "#8c8c8c", "#c4c4c4", "#4f4f4f", "#a8a8a8", "#2f2f2f", "#dcdcdc", "#6e6e6e"]
    SEQ = ["#f4f4f4", "#e6e6e6", "#d6d6d6", "#c4c4c4", "#b0b0b0", "#9a9a9a", "#828282", "#6a6a6a", "#525252", "#3c3c3c", "#282828", "#161616", "#000000"]
LS = ["-", "--", "-.", ":", (0, (5, 1, 1, 1))] if BW else ["-"] * 5
_noop = lambda *a, **k: None   # in BW (journal) mode figure titles are given as captions in the text, not inside the figure
INK, INK2, GRID = "#1a1a19", "#5f5e5a", "#e6e5e1"
plt.rcParams.update({"font.family": "DejaVu Sans"}); plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight", "legend.frameon": False})
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
RES = {}

# ---------- data ----------
tot = pd.read_csv(P("data/processed/monthly_totals.csv"), parse_dates=["date"]).set_index("date").asfreq("MS")
lng = pd.read_csv(P("data/processed/evisitor_knin_long.csv"))
lng = lng[lng.span == "month"].copy()
lng["date"] = pd.to_datetime(dict(year=lng.year, month=lng.month, day=1))
y_arr, y_nig = tot.arrivals.astype(float), tot.nights.astype(float)

# ---------- 1. annual table ----------
ann = tot.groupby(tot.index.year).agg(arrivals=("arrivals", "sum"), nights=("nights", "sum"),
                                      domestic_arr=("domestic_arr", "sum"), foreign_arr=("foreign_arr", "sum"),
                                      domestic_nights=("domestic_nights", "sum"), foreign_nights=("foreign_nights", "sum"),
                                      months=("arrivals", "size"))
ann["ALOS"] = ann.nights / ann.arrivals
ann["foreign_share_arr"] = ann.foreign_arr / ann.arrivals
ann["foreign_share_nights"] = ann.foreign_nights / ann.nights
ann["yoy_arr"] = ann.arrivals.pct_change()
ann["yoy_nights"] = ann.nights.pct_change()
# Jan-Sep comparison for partial 2026
js = tot[tot.index.month <= 9].groupby(tot[tot.index.month <= 9].index.year)[["arrivals", "nights"]].sum()
ann["arr_JanSep"] = js.arrivals; ann["nights_JanSep"] = js.nights
ann["yoy_arr_JanSep"] = js.arrivals.pct_change(); ann["yoy_nights_JanSep"] = js.nights.pct_change()
ann.to_csv(P("outputs/table1_annual.csv"))
full = ann[ann.months == 12]
cagr_arr = (full.arrivals.loc[2025] / full.arrivals.loc[2016]) ** (1 / 9) - 1
cagr_nig = (full.nights.loc[2025] / full.nights.loc[2016]) ** (1 / 9) - 1
cagr_arr_post = (full.arrivals.loc[2025] / full.arrivals.loc[2021]) ** (1 / 4) - 1
RES["cagr"] = dict(arrivals_2016_2025=cagr_arr, nights_2016_2025=cagr_nig, arrivals_2021_2025=cagr_arr_post,
                   nights_2021_2025=(full.nights.loc[2025] / full.nights.loc[2021]) ** (1 / 4) - 1)
print(ann.round(3).to_string()); print(RES["cagr"])

# Fig 1: monthly series arrivals & nights, domestic/foreign
fig, axes = plt.subplots(2, 1, figsize=(9, 5.6), sharex=True)
for ax, (a, b, lab) in zip(axes, [("domestic_arr", "foreign_arr", "Arrivals"), ("domestic_nights", "foreign_nights", "Overnight stays")]):
    ax.stackplot(tot.index, tot[a], tot[b], colors=[CAT[0], CAT[1]] if not BW else ["#5a5a5a", "#c8c8c8"], labels=["Domestic", "Foreign"], alpha=0.9)
    ax.set_ylabel(lab); ax.margins(x=0.01)
    for d, t in [("2020-03-01", "COVID-19"), ("2023-01-01", "Euro + Schengen")]:
        ax.axvline(pd.Timestamp(d), color=INK2, lw=0.8, ls="--")
        if lab == "Arrivals": ax.text(pd.Timestamp(d), ax.get_ylim()[1] * 0.97, " " + t, va="top", fontsize=8, color=INK2)
axes[0].legend(loc="upper left", ncol=2); axes[1].xaxis.set_major_locator(mdates.YearLocator()); axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
(_noop if BW else fig.suptitle)("Monthly tourist arrivals and overnight stays in Knin, Jan 2016 - Sep 2026 (e-Visitor)", x=0.01, ha="left", fontsize=10, color=INK)
fig.savefig(P(FIGDIR + "/fig1_monthly_series.png")); plt.close()

# ---------- 2. STL ----------
stl_a = STL(np.log1p(y_arr), period=12, robust=True).fit()
stl_n = STL(np.log1p(y_nig), period=12, robust=True).fit()
fig, axes = plt.subplots(4, 1, figsize=(9, 7.5), sharex=True)
for comp, name, ax in zip([np.log1p(y_arr), stl_a.trend, stl_a.seasonal, stl_a.resid], ["log(1+arrivals)", "Trend", "Seasonal", "Remainder"], axes):
    ax.plot(comp.index, comp.values, color=CAT[0], lw=1.6); ax.set_ylabel(name)
axes[-1].xaxis.set_major_locator(mdates.YearLocator()); axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
(_noop if BW else fig.suptitle)("STL decomposition of log monthly arrivals, Knin 2016-2026", x=0.01, ha="left", fontsize=10)
fig.savefig(P(FIGDIR + "/fig2_stl_arrivals.png")); plt.close()
# strength of trend / seasonality (Hyndman & Athanasopoulos)
def strength(stl):
    r, s, t = stl.resid, stl.seasonal, stl.trend
    return dict(F_T=max(0, 1 - r.var() / (t + r).var()), F_S=max(0, 1 - r.var() / (s + r).var()))
RES["stl_strength"] = dict(arrivals=strength(stl_a), nights=strength(stl_n))
# trend growth: annualised slope of STL trend post-2021
tr = stl_a.trend["2021-06":"2026-09"]; slope = np.polyfit(np.arange(len(tr)), tr.values, 1)[0]
RES["stl_trend_annual_growth_post2021"] = float(np.exp(slope * 12) - 1)
RES["stl_seasonal_amplitude_ratio"] = float(np.exp(stl_a.seasonal.max() - stl_a.seasonal.min()))

# ---------- 3. seasonality: Gini, seasonality ratio, peak share ----------
def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if x.sum() == 0: return np.nan
    return (2 * np.sum((np.arange(1, n + 1)) * x) / (n * x.sum())) - (n + 1) / n
seas = []
for yr, g in tot.groupby(tot.index.year):
    if len(g) < 12: continue
    for var in ["arrivals", "nights", "foreign_arr", "domestic_arr"]:
        v = g[var].values
        seas.append(dict(year=yr, variable=var, gini=gini(v), seasonality_ratio=v.max() / v.mean(),
                         peak_share_JulAug=v[6:8].sum() / v.sum(), share_JunSep=v[5:9].sum() / v.sum(),
                         winter_share_NovMar=(v[[0, 1, 2, 10, 11]].sum()) / v.sum(), cv=v.std(ddof=1) / v.mean()))
seas = pd.DataFrame(seas); seas.to_csv(P("outputs/table2_seasonality.csv"), index=False)
sg = seas[seas.variable == "arrivals"]
tau, p_tau = stats.kendalltau(sg.year, sg.gini); sl, ic, r, p_sl, se = stats.linregress(sg.year, sg.gini)
RES["gini_trend"] = dict(kendall_tau=tau, p=p_tau, ols_slope_per_year=sl, ols_p=p_sl, gini_2016=float(sg.gini.iloc[0]), gini_2025=float(sg.gini.iloc[-1]))
sgn = seas[seas.variable == "nights"]; tau2, p2 = stats.kendalltau(sgn.year, sgn.gini)
RES["gini_trend_nights"] = dict(kendall_tau=tau2, p=p2, gini_2016=float(sgn.gini.iloc[0]), gini_2025=float(sgn.gini.iloc[-1]))
print(seas.pivot(index="year", columns="variable", values="gini").round(3))

# Fig 3: seasonal profile heatmap (month x year, share of annual arrivals) + Gini line
piv = tot.assign(y=tot.index.year, m=tot.index.month).pivot(index="y", columns="m", values="arrivals")
piv = piv[piv.index < 2026]
share = piv.div(piv.sum(axis=1), axis=0)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw=dict(width_ratios=[2.2, 1]))
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("seq", SEQ)
im = ax1.imshow(share.values, cmap=cmap, aspect="auto", vmin=0, vmax=np.nanmax(share.values))
ax1.set_xticks(range(12)); ax1.set_xticklabels(MONTHS); ax1.set_yticks(range(len(share))); ax1.set_yticklabels(share.index); ax1.grid(False)
for i in range(share.shape[0]):
    for j in range(12):
        v = share.values[i, j]
        if not np.isnan(v): ax1.text(j, i, f"{v*100:.0f}", ha="center", va="center", fontsize=7, color="white" if v > 0.12 else INK)
ax1.set_title("Share of annual arrivals by month (%)", loc="left", fontsize=9)
ax2.plot(sg.year, sg.gini, "-o", color=CAT[0], ms=5, label="Arrivals"); ax2.plot(sgn.year, sgn.gini, "--s", color=CAT[1] if not BW else "#6e6e6e", ms=5, label="Nights")
ax2.set_ylim(0.25, 0.6); ax2.set_title("Gini coefficient of seasonality", loc="left", fontsize=9); ax2.legend(); ax2.set_xticks(sg.year); ax2.tick_params(axis="x", rotation=45)
fig.savefig(P(FIGDIR + "/fig3_seasonality.png")); plt.close()

# ---------- 4. source-market structure: HHI, top markets, chord diagram ----------
cy = lng.groupby(["year", "country"])[["arrivals", "nights"]].sum().reset_index()
def hhi(s):
    s = s / s.sum(); return float((s ** 2).sum())
mk = []
for yr, g in cy.groupby("year"):
    g = g.sort_values("arrivals", ascending=False)
    gf = g[g.country != "Hrvatska"]
    mk.append(dict(year=yr, HHI_arrivals=hhi(g.arrivals), HHI_nights=hhi(g.nights), HHI_foreign_arrivals=hhi(gf.arrivals),
                   n_markets_arr_gt0=int((g.arrivals > 0).sum()), top5_share=g.arrivals.head(5).sum() / g.arrivals.sum(),
                   top5_foreign_share=gf.arrivals.head(5).sum() / gf.arrivals.sum(), eff_n_markets=1 / hhi(g.arrivals),
                   eff_n_foreign=1 / hhi(gf.arrivals), top5=", ".join(g.country.head(5))))
mk = pd.DataFrame(mk); mk.to_csv(P("outputs/table3_market_concentration.csv"), index=False); print(mk.round(3).to_string())
tauh, ph = stats.kendalltau(mk.year[mk.year < 2026], mk.HHI_foreign_arrivals[mk.year < 2026])
RES["hhi_trend_foreign"] = dict(kendall_tau=tauh, p=ph, hhi_2016=float(mk.HHI_foreign_arrivals.iloc[0]), hhi_2025=float(mk.HHI_foreign_arrivals[mk.year == 2025].iloc[0]))
# top-15 markets table: arrivals 2016, 2019, 2025 and CAGR 2019-2025 and share
top = cy.pivot(index="country", columns="year", values="arrivals").fillna(0)
topn = cy.pivot(index="country", columns="year", values="nights").fillna(0)
t15 = top.sort_values(2025, ascending=False).head(15).copy()
t15["share_2025"] = t15[2025] / top[2025].sum(); t15["share_2016"] = t15[2016] / top[2016].sum()
t15["CAGR_2019_2025"] = (t15[2025] / t15[2019].replace(0, np.nan)) ** (1 / 6) - 1
t15["ALOS_2025"] = topn.loc[t15.index, 2025] / t15[2025]
t15[[2016, 2019, 2022, 2025, "share_2016", "share_2025", "CAGR_2019_2025", "ALOS_2025"]].to_csv(P("outputs/table4_top_markets.csv"))
print(t15[[2016, 2019, 2025, "share_2016", "share_2025", "CAGR_2019_2025", "ALOS_2025"]].round(3))

# Fig 4: stacked share area of top-8 markets + other, annual arrivals
sel = top.sort_values(2025, ascending=False).head(8).index.tolist()
sh = top.loc[sel].T.copy(); sh["Other"] = top.drop(sel).sum().values; sh = sh.div(sh.sum(axis=1), axis=0)
labels = [("Croatia" if c == "Hrvatska" else {"Njemačka": "Germany", "Srbija": "Serbia", "Bosna i Hercegovina": "Bosnia and Herz.", "Poljska": "Poland", "Francuska": "France", "Austrija": "Austria", "Češka": "Czechia", "Slovenija": "Slovenia", "Italija": "Italy"}.get(c, c)) for c in sh.columns]
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.stackplot(sh.index, sh.T.values * 100, labels=labels, colors=CAT[:8] + ["#b8b7b1"], alpha=0.92, **(dict(hatch=["", "//", "", "\\\\", "", "xx", "", "..", ""], edgecolor="white", linewidth=0.3) if BW else {}))
ax.set_ylim(0, 100); ax.set_ylabel("Share of arrivals (%)"); ax.set_xticks(sh.index); ax.margins(x=0)
ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=8)
(_noop if BW else ax.set_title)("Source-market structure of arrivals in Knin, 2016-2026 (2026 = Jan-Sep)", loc="left", fontsize=10)
fig.savefig(P(FIGDIR + "/fig4_market_shares.png")); plt.close()

# Fig 5: chord diagram market x month (2023-2026 pooled, arrivals), top-10 markets + other
from pycirclize import Circos
recent = lng[lng.year >= 2023]
cm = recent.groupby(["country", "month"]).arrivals.sum().unstack(fill_value=0)
top10 = cm.sum(axis=1).sort_values(ascending=False).head(10).index
cm2 = cm.loc[top10].copy(); cm2.loc["Other"] = cm.drop(top10).sum()
en = {"Hrvatska": "Croatia", "Njemačka": "Germany", "Srbija": "Serbia", "Bosna i Hercegovina": "BiH", "Poljska": "Poland", "Francuska": "France", "Austrija": "Austria", "Češka": "Czechia", "Slovenija": "Slovenia", "Italija": "Italy", "Nizozemska": "Netherlands", "SAD": "USA", "Ujedinjena Kraljevina": "UK"}
cm2.index = [en.get(c, c) for c in cm2.index]; cm2.columns = MONTHS
# season groups to reduce clutter: Winter(Nov-Mar), Spring(Apr-May), Summer(Jun-Aug), Autumn(Sep-Oct)
grp = {"Nov-Mar": ["Nov", "Dec", "Jan", "Feb", "Mar"], "Apr-May": ["Apr", "May"], "Jun-Aug": ["Jun", "Jul", "Aug"], "Sep-Oct": ["Sep", "Oct"]}
cms = pd.DataFrame({k: cm2[v].sum(axis=1) for k, v in grp.items()})
cms.to_csv(P("outputs/table5_market_season_matrix_2023_2026.csv"))
colors = {n: c for n, c in zip(cms.index, CAT[:8] + ["#9c8f7a", "#7a8c9c", "#b8b7b1"])}
if BW: colors = {n: c for n, c in zip(cms.index, ["#111111", "#3a3a3a", "#5c5c5c", "#7a7a7a", "#969696", "#adadad", "#c3c3c3", "#d6d6d6", "#e4e4e4", "#efefef", "#f7f7f7"])}
colors.update({"Nov-Mar": "#cfcdc6", "Apr-May": "#a8a69f", "Jun-Aug": "#5f5e5a", "Sep-Oct": "#86847e"} if not BW else {"Nov-Mar": "#ffffff", "Apr-May": "#bfbfbf", "Jun-Aug": "#404040", "Sep-Oct": "#808080"})
circos = Circos.chord_diagram(cms, space=3, cmap=colors, label_kws=dict(size=8, r=108), link_kws=dict(ec="white" if not BW else "#777777", lw=0.3, alpha=0.75 if not BW else 0.9))
fig = circos.plotfig(figsize=(7, 7))
(_noop if BW else fig.suptitle)("Chord diagram: source markets x season, arrivals in Knin 2023 - Sep 2026", fontsize=10, x=0.02, ha="left")
fig.savefig(P(FIGDIR + "/fig5_chord_market_season.png"), dpi=300, bbox_inches="tight"); plt.close()

# ---------- 5. structural breaks ----------
# (a) Bai-Perron style via ruptures (PELT / Dynp on log seasonally-adjusted series)
sa = (np.log1p(y_arr) - stl_a.seasonal)  # seasonally adjusted log arrivals
sig = sa.values.reshape(-1, 1)
algo = rpt.Dynp(model="l2", min_size=18, jump=1).fit(sig)
bp = {}
for k in [1, 2, 3]:
    bk = algo.predict(n_bkps=k)[:-1]
    bp[k] = [str(sa.index[i].date()) for i in bk]
# BIC selection
def bic_for(bks):
    segs = np.split(sig.ravel(), bks); rss = sum(((s - s.mean()) ** 2).sum() for s in segs); n = len(sig)
    return n * np.log(rss / n) + (2 * len(bks) + 1) * np.log(n)
bics = {k: bic_for(algo.predict(n_bkps=k)[:-1]) for k in [0, 1, 2, 3]} if True else None
bics[0] = bic_for([])
RES["breaks"] = dict(dates_by_k=bp, bic=bics, selected_k=int(min(bics, key=bics.get)))
print("breaks", RES["breaks"])
# (b) Chow test for COVID (Mar 2020) and Jan 2023 on log SA series with linear trend
def chow(y, idx):
    X = sm.add_constant(np.arange(len(y))); n = len(y)
    r = sm.OLS(y, X).fit().ssr; r1 = sm.OLS(y[:idx], X[:idx]).fit().ssr; r2 = sm.OLS(y[idx:], X[idx:]).fit().ssr
    k = 2; F = ((r - r1 - r2) / k) / ((r1 + r2) / (n - 2 * k)); return float(F), float(1 - stats.f.cdf(F, k, n - 2 * k))
RES["chow"] = {d: dict(zip(["F", "p"], chow(sa.values, sa.index.get_loc(pd.Timestamp(d))))) for d in ["2020-03-01", "2021-06-01", "2023-01-01"]}
print("chow", RES["chow"])
# (c) counterfactual: pre-COVID trend (2016-2019) extrapolated vs actual, annual
pre = sa["2016":"2019"]; X = sm.add_constant(np.arange(len(pre))); m = sm.OLS(pre.values, X).fit()
RES["pre_covid_trend_annual_growth"] = float(np.exp(m.params[1] * 12) - 1)
# post-covid trend 2021-06 onward
post = sa["2021-06":]; Xp = sm.add_constant(np.arange(len(post))); mp = sm.OLS(post.values, Xp).fit()
RES["post_covid_trend_annual_growth"] = float(np.exp(mp.params[1] * 12) - 1)
RES["post_covid_trend_se_annual"] = float(mp.bse[1] * 12)

# Fig 6: SA log series with segment means and break dates
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(sa.index, np.expm1(sa), color=CAT[0], lw=1.5, label="Seasonally adjusted arrivals (STL)")
ax.plot(tot.index, y_arr.rolling(12, center=True).mean(), color=CAT[1], lw=1.5, ls="--" if BW else "-", label="12-month centred moving average")
for d in bp[RES["breaks"]["selected_k"]]:
    ax.axvline(pd.Timestamp(d), color=INK2, ls="--", lw=0.9); ax.text(pd.Timestamp(d), ax.get_ylim()[1] * 0.95, " " + d[:7], fontsize=8, color=INK2)
ax.set_ylabel("Arrivals per month"); ax.legend(loc="upper left"); ax.margins(x=0.01)
(_noop if BW else ax.set_title)("Seasonally adjusted arrivals and estimated structural breaks (Bai-Perron / dynamic programming, BIC)", loc="left", fontsize=10)
fig.savefig(P(FIGDIR + "/fig6_structural_breaks.png")); plt.close()

# ---------- 6. unit root tests ----------
ly = np.log1p(y_arr)
RES["adf_log"] = dict(zip(["stat", "p"], adfuller(ly, regression="ct", autolag="AIC")[:2]))
RES["kpss_log"] = dict(zip(["stat", "p"], kpss(ly, regression="ct", nlags="auto")[:2]))
RES["adf_d1D12"] = dict(zip(["stat", "p"], adfuller(ly.diff().diff(12).dropna(), regression="c", autolag="AIC")[:2]))

# ---------- 7. forecasting: train 2016-01..2024-12, test 2025-01..2026-09 (21 months) ----------
def fit_sarima(y, order, sorder):
    return SARIMAX(y, order=order, seasonal_order=sorder, trend="n", enforce_stationarity=True, enforce_invertibility=True).fit(disp=False)
def mape(a, f): return float(np.mean(np.abs((a - f) / a)) * 100)
def mase(a, f, train, m=12):
    d = np.mean(np.abs(train[m:] - train[:-m])); return float(np.mean(np.abs(a - f)) / d)
def rmse(a, f): return float(np.sqrt(np.mean((a - f) ** 2)))

def evaluate(series, name):
    ly = np.log1p(series); train, test = ly[:"2024-12"], ly["2025-01":]
    out = {}; fc = {}
    # SARIMA grid (small)
    best = None
    for p in [0, 1, 2, 3]:
        for q in [0, 1, 2, 3]:
            for Pp in [0, 1, 2]:
                for Q in [0, 1, 2]:
                    try:
                        m = fit_sarima(train, (p, 1, q), (Pp, 1, Q, 12))
                        if best is None or m.aic < best[0]: best = (m.aic, (p, 1, q), (Pp, 1, Q, 12))
                    except Exception: pass
    m_sar = fit_sarima(train, best[1], best[2]); f_sar = np.expm1(m_sar.get_forecast(len(test)).predicted_mean)
    lb = acorr_ljungbox(m_sar.resid[26:], lags=[12, 24], return_df=True)
    out["SARIMA"] = dict(order=best[1], seasonal_order=best[2], aic=float(m_sar.aic), ljungbox_p12=float(lb["lb_pvalue"].iloc[0]), ljungbox_p24=float(lb["lb_pvalue"].iloc[1]))
    fc["SARIMA"] = f_sar
    # ETS: additive trend (damped) + additive seasonal on log scale  (= multiplicative Holt-Winters on levels)
    m_ets = ExponentialSmoothing(train, trend="add", damped_trend=True, seasonal="add", seasonal_periods=12, initialization_method="estimated").fit(optimized=True)
    fc["ETS(A,Ad,A) on log"] = np.expm1(m_ets.forecast(len(test))); out["ETS"] = dict(aic=float(m_ets.aic), params={k: float(v) for k, v in m_ets.params.items() if k in ["smoothing_level", "smoothing_trend", "smoothing_seasonal", "damping_trend"]})
    # Holt-Winters multiplicative on levels
    m_hw = ExponentialSmoothing(series[:"2024-12"], trend="add", damped_trend=True, seasonal="mul", seasonal_periods=12, initialization_method="estimated").fit(optimized=True)
    fc["Holt-Winters (A,Ad,M)"] = m_hw.forecast(len(test))
    # Seasonal naive benchmark
    fc["Seasonal naive"] = pd.Series(np.expm1(train[-12:].values)[np.arange(len(test)) % 12], index=test.index)
    # STL + ETS? keep to 4. Combination
    fc["Combination (mean)"] = (fc["SARIMA"] + fc["ETS(A,Ad,A) on log"] + fc["Holt-Winters (A,Ad,M)"]) / 3
    actual = series["2025-01":].values; tr_lev = series[:"2024-12"].values
    acc = pd.DataFrame({k: dict(MAPE=mape(actual, v.values), RMSE=rmse(actual, v.values), MASE=mase(actual, v.values, tr_lev),
                                bias_pct=float((v.values.sum() - actual.sum()) / actual.sum() * 100)) for k, v in fc.items()}).T
    acc.to_csv(P(f"outputs/table6_forecast_accuracy_{name}.csv")); print(name); print(acc.round(2))
    return out, fc, acc, best

out_a, fc_a, acc_a, best_a = evaluate(y_arr, "arrivals")
out_n, fc_n, acc_n, best_n = evaluate(y_nig, "nights")
RES["models_arrivals"] = out_a; RES["models_nights"] = out_n
RES["accuracy_arrivals"] = acc_a.round(3).to_dict(); RES["accuracy_nights"] = acc_n.round(3).to_dict()

# Fig 7: out-of-sample validation plot (arrivals)
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.plot(y_arr["2022":].index, y_arr["2022":], color=INK, lw=1.8, label="Actual")
for (k, v), c, ls in zip(fc_a.items(), [CAT[0], CAT[1], CAT[2], "#b8b7b1", CAT[6]], LS):
    ax.plot(v.index, v.values, lw=1.4, color=c if not BW else "#555555", ls=ls if BW else ("-" if k != "Seasonal naive" else ":"), label=f"{k} (MAPE {acc_a.loc[k,'MAPE']:.0f}%)")
ax.axvspan(pd.Timestamp("2025-01-01"), pd.Timestamp("2026-09-01"), color=GRID, alpha=0.5, lw=0); ax.text(pd.Timestamp("2025-01-15"), ax.get_ylim()[1] * 0.95, "hold-out: Jan 2025 - Sep 2026", fontsize=8, color=INK2)
ax.legend(fontsize=8, loc="upper left"); ax.set_ylabel("Arrivals per month"); ax.margins(x=0.01)
(_noop if BW else ax.set_title)("Out-of-sample validation: models fitted on 2016-2024, forecast 21 months ahead", loc="left", fontsize=10)
fig.savefig(P(FIGDIR + "/fig7_validation.png")); plt.close()

# ---------- 8. final projections to 2030 (refit on full sample to 2026-09) ----------
H = 51  # Oct 2026 .. Dec 2030
fidx = pd.date_range("2026-10-01", periods=H, freq="MS")
proj = {}
for series, name, best in [(y_arr, "arrivals", best_a), (y_nig, "nights", best_n)]:
    ly = np.log1p(series)
    m_sar = fit_sarima(ly, best[1], best[2]); f = m_sar.get_forecast(H); ci = f.conf_int(alpha=0.2)
    s_sar = np.expm1(f.predicted_mean); s_lo = np.expm1(ci.iloc[:, 0]); s_hi = np.expm1(ci.iloc[:, 1])
    m_ets = ExponentialSmoothing(ly, trend="add", damped_trend=True, seasonal="add", seasonal_periods=12, initialization_method="estimated").fit(optimized=True)
    s_ets = np.expm1(m_ets.forecast(H))
    m_hw = ExponentialSmoothing(series, trend="add", damped_trend=True, seasonal="mul", seasonal_periods=12, initialization_method="estimated").fit(optimized=True)
    s_hw = m_hw.forecast(H)
    comb = (s_sar + s_ets + s_hw) / 3
    df = pd.DataFrame({"SARIMA": s_sar.values, "SARIMA_lo80": s_lo.values, "SARIMA_hi80": s_hi.values, "ETS_log": s_ets.values, "HoltWinters": s_hw.values, "Combination": comb.values}, index=fidx)
    df.to_csv(P(f"outputs/table7_projection_monthly_{name}.csv"))
    hist = series.copy(); ann_hist = hist.groupby(hist.index.year).sum()
    a26 = ann_hist.loc[2026] + df.loc["2026"].sum()
    yearly = df.groupby(df.index.year).sum(); yearly.loc[2026] = yearly.loc[2026] + ann_hist.loc[2026]
    yearly.to_csv(P(f"outputs/table8_projection_annual_{name}.csv"))
    proj[name] = dict(monthly=df, annual=yearly, model_order=best)
    print(name, "annual projections"); print(yearly.round(0))
RES["projection_annual_arrivals"] = proj["arrivals"]["annual"].round(0).to_dict()
RES["projection_annual_nights"] = proj["nights"]["annual"].round(0).to_dict()

# logistic (TALC) scenario on annual arrivals 2016-2025 (+2026 est.) -> carrying capacity
yrs = np.array(full.index.tolist() + [2026]); vals = np.array(full.arrivals.tolist() + [proj["arrivals"]["annual"].loc[2026, "Combination"]])
def logistic(t, K, r, t0): return K / (1 + np.exp(-r * (t - t0)))
try:
    popt, pcov = optimize.curve_fit(logistic, yrs - 2016, vals, p0=[15000, 0.4, 8], maxfev=20000, bounds=([3000, 0.01, 0], [60000, 2, 40]))
    RES["logistic"] = dict(K=float(popt[0]), r=float(popt[1]), t0=float(2016 + popt[2]), K_se=float(np.sqrt(pcov[0, 0])))
    lg = {int(y): float(logistic(y - 2016, *popt)) for y in range(2016, 2031)}
    RES["logistic_path"] = lg
except Exception as e:
    RES["logistic"] = str(e)
print("logistic", RES.get("logistic"))

# Fig 8: annual history + projections (3 model paths + 80% band of SARIMA) + logistic
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, name, lab in zip(axes, ["arrivals", "nights"], ["Arrivals", "Overnight stays"]):
    h = (y_arr if name == "arrivals" else y_nig); ah = h.groupby(h.index.year).sum()
    ax.bar(ah.index[ah.index < 2026], ah[ah.index < 2026], color=CAT[0] if not BW else "#9a9a9a", width=0.7, label="Actual")
    ax.bar([2026], [ah.loc[2026]], color=CAT[0] if not BW else "#9a9a9a", width=0.7, alpha=0.5, label="2026 actual Jan-Sep")
    yv = proj[name]["annual"]
    mo = proj[name]["monthly"]; lo = mo.groupby(mo.index.year).SARIMA_lo80.sum(); hi = mo.groupby(mo.index.year).SARIMA_hi80.sum()
    lo.loc[2026] += ah.loc[2026]; hi.loc[2026] += ah.loc[2026]
    ax.fill_between(yv.index, lo.values, hi.values, color=CAT[1], alpha=0.15, lw=0, label="SARIMA 80% interval (sum of monthly bounds)")
    ax.set_ylim(0, yv["SARIMA"].max() * 1.35)
    for col, c, ls in ([("SARIMA", CAT[1], "-"), ("ETS_log", CAT[2], "-"), ("HoltWinters", CAT[3], "-"), ("Combination", INK, "--")] if not BW else [("SARIMA", "#000000", "-"), ("ETS_log", "#000000", "--"), ("HoltWinters", "#000000", "-."), ("Combination", "#000000", (0, (5, 1, 1, 1)))]):
        ax.plot(yv.index, yv[col], color=c, lw=1.6, ls=ls, marker="o", ms=3.5, label=col.replace("_log", " (log)"))
    if name == "arrivals" and isinstance(RES.get("logistic"), dict):
        ax.plot(list(RES["logistic_path"].keys()), list(RES["logistic_path"].values()), color=CAT[6] if not BW else "#7a7a7a", lw=1.4, ls=":", label=f"Logistic (K={RES['logistic']['K']:,.0f})")
    ax.set_title(f"{lab}: actual 2016-2026 and projections to 2030", loc="left", fontsize=9); ax.set_xticks(range(2016, 2031)); ax.tick_params(axis="x", rotation=60)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k"))
axes[0].legend(fontsize=7.5, loc="upper left")
fig.savefig(P(FIGDIR + "/fig8_projections.png")); plt.close()

# Fig 9: monthly projection fan (arrivals) 2022-2030
fig, ax = plt.subplots(figsize=(9, 3.8))
mo = proj["arrivals"]["monthly"]
ax.plot(y_arr["2022":].index, y_arr["2022":], color=INK, lw=1.5, label="Actual")
ax.fill_between(mo.index, mo.SARIMA_lo80, mo.SARIMA_hi80, color=CAT[1], alpha=0.18, lw=0, label="SARIMA 80% interval")
ax.plot(mo.index, mo.SARIMA, color=CAT[1], lw=1.3, ls=LS[0], label="SARIMA"); ax.plot(mo.index, mo.ETS_log, color=CAT[2] if not BW else "#000000", lw=1.3, ls=LS[1], label="ETS (log)"); ax.plot(mo.index, mo.HoltWinters, color=CAT[3] if not BW else "#000000", lw=1.3, ls=LS[2], label="Holt-Winters")
ax.legend(fontsize=8, loc="upper left"); ax.set_ylabel("Arrivals per month"); ax.margins(x=0.01)
(_noop if BW else ax.set_title)("Monthly projections of arrivals to December 2030", loc="left", fontsize=10)
fig.savefig(P(FIGDIR + "/fig9_monthly_projection.png")); plt.close()

# ---------- 9. ALOS by market and season; winter vs summer growth ----------
tot["ALOS"] = tot.nights / tot.arrivals
alos_y = ann[["ALOS"]].copy(); alos_y["ALOS_dom"] = ann.domestic_nights / ann.domestic_arr; alos_y["ALOS_for"] = ann.foreign_nights / ann.foreign_arr
alos_y.to_csv(P("outputs/table9_alos.csv")); print(alos_y.round(2))
# off-season growth: Nov-Mar arrivals CAGR vs Jun-Sep
off = tot[tot.index.month.isin([11, 12, 1, 2, 3])].groupby(tot[tot.index.month.isin([11, 12, 1, 2, 3])].index.year).arrivals.sum()
peak = tot[tot.index.month.isin([6, 7, 8, 9])].groupby(tot[tot.index.month.isin([6, 7, 8, 9])].index.year).arrivals.sum()
RES["offseason_cagr_2016_2025"] = float((off.loc[2025] / off.loc[2016]) ** (1 / 9) - 1); RES["peak_cagr_2016_2025"] = float((peak.loc[2025] / peak.loc[2016]) ** (1 / 9) - 1)
RES["offseason_share_2016"] = float(off.loc[2016] / full.arrivals.loc[2016]); RES["offseason_share_2025"] = float(off.loc[2025] / full.arrivals.loc[2025])

# Fig 10: small multiples - top 6 foreign markets monthly arrivals (12m rolling sum)
fig, axes = plt.subplots(2, 3, figsize=(10, 5), sharex=True)
for ax, c, col in zip(axes.ravel(), ["Njemačka", "Srbija", "Bosna i Hercegovina", "Poljska", "Francuska", "Austrija"], CAT[1:7]):
    s = lng[lng.country == c].set_index("date").arrivals.reindex(tot.index, fill_value=0).rolling(12).sum()
    ax.plot(s.index, s, color=col, lw=1.8); ax.set_title(en.get(c, c), loc="left", fontsize=9); ax.margins(x=0.01)
    ax.xaxis.set_major_locator(mdates.YearLocator(2)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
(_noop if BW else fig.suptitle)("Rolling 12-month arrivals by leading foreign market", x=0.01, ha="left", fontsize=10)
fig.savefig(P(FIGDIR + "/fig10_markets_small_multiples.png")); plt.close()

# ---------- 10. summary descriptive stats ----------
RES["totals"] = dict(months=int(len(tot)), arrivals_total=int(tot.arrivals.sum()), nights_total=int(tot.nights.sum()),
                     arrivals_2016=int(full.arrivals.loc[2016]), arrivals_2025=int(full.arrivals.loc[2025]),
                     nights_2016=int(full.nights.loc[2016]), nights_2025=int(full.nights.loc[2025]),
                     foreign_share_arr_2016=float(full.foreign_share_arr.loc[2016]), foreign_share_arr_2025=float(full.foreign_share_arr.loc[2025]),
                     alos_2016=float(full.ALOS.loc[2016]), alos_2025=float(full.ALOS.loc[2025]),
                     n_countries=int(lng.country.nunique()), countries_gt0_2025=int((top[2025] > 0).sum()))
RES["annual"] = ann.round(4).reset_index().to_dict(orient="records")
def conv(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.ndarray,)): return o.tolist()
    if isinstance(o, tuple): return list(o)
    return str(o)
json.dump(RES, open(P("outputs/results.json"), "w"), indent=2, default=conv, ensure_ascii=False)
print("DONE")
