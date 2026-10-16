"""
05_revision.py - additional analyses requested in review:
 (1) structural breaks in a segmented TREND model (intercept + slope) and in the GROWTH RATE of
     seasonally adjusted log arrivals, with bootstrap supF p-values and bootstrap 90% confidence
     intervals for break dates (instead of breaks in the mean of a trending series);
 (2) simulation-based 80% prediction intervals for ANNUAL sums (1,000 SARIMA sample paths);
 (3) rolling-origin (time-series cross-validation) evaluation, horizons 1-12 months;
 (4) market x season table (percentages) replacing the chord diagram in the B/W journal version;
 (5) DZS comparison (Knin vs Sibenik-Knin County vs Croatia) if data/external/dzs_tu12.csv exists.
Outputs go to outputs/rev_*.csv, outputs/revision.json and figures/bw/rev_*.png.
"""
import os, json, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
import statsmodels.api as sm
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import ruptures as rpt
warnings.filterwarnings("ignore")
rng = np.random.default_rng(2026)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); P = lambda *a: os.path.join(ROOT, *a)
os.makedirs(P("figures/bw"), exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#e6e5e1", "axes.axisbelow": True, "savefig.dpi": 300, "savefig.bbox": "tight", "legend.frameon": False})
R = {}
tot = pd.read_csv(P("data/processed/monthly_totals.csv"), parse_dates=["date"]).set_index("date").asfreq("MS")
y = tot.arrivals.astype(float); ly = np.log1p(y)
stl = STL(ly, period=12, robust=True).fit(); sa = (ly - stl.seasonal); n = len(sa); t = np.arange(n)
dates = sa.index

# ---------------- (1a) segmented trend: breaks in intercept and slope ----------------
def seg_rss(yv, bks):
    """RSS of a piecewise linear trend with breaks at indices bks (segment-specific intercept and slope)."""
    idx = [0] + list(bks) + [len(yv)]; rss = 0.0
    for a, b in zip(idx[:-1], idx[1:]):
        X = sm.add_constant(np.arange(a, b)); rss += sm.OLS(yv[a:b], X).fit().ssr
    return rss
def seg_fit(yv, bks):
    idx = [0] + list(bks) + [len(yv)]; fit = np.empty(len(yv)); slopes = []
    for a, b in zip(idx[:-1], idx[1:]):
        X = sm.add_constant(np.arange(a, b)); m = sm.OLS(yv[a:b], X).fit(); fit[a:b] = m.fittedvalues; slopes.append(float(m.params[1]))
    return fit, slopes
H = 18  # minimum segment length (months), 14% trimming
sig = np.column_stack([sa.values, t, np.ones(n)])
algo = rpt.Dynp(model="linear", min_size=H, jump=1).fit(sig)
res_seg = {}
for k in [0, 1, 2, 3]:
    bks = [] if k == 0 else algo.predict(n_bkps=k)[:-1]
    rss = seg_rss(sa.values, bks); npar = 2 * (k + 1) + k
    bic = n * np.log(rss / n) + npar * np.log(n)
    res_seg[k] = dict(breaks=[str(dates[b].date()) for b in bks], idx=bks, rss=rss, bic=bic)
k_sel = min(res_seg, key=lambda k: res_seg[k]["bic"])
print("segmented trend BIC:", {k: round(v["bic"], 1) for k, v in res_seg.items()}, "selected", k_sel, res_seg[k_sel]["breaks"])
# supF test for one break (trend model) with residual bootstrap under H0 (no break, AR(1) errors via sieve)
def supF(yv, h=H):
    X = sm.add_constant(np.arange(len(yv))); m0 = sm.OLS(yv, X).fit(); rss0 = m0.ssr; best = (-1, None)
    for b in range(h, len(yv) - h):
        rss1 = seg_rss(yv, [b]); F = ((rss0 - rss1) / 2) / (rss1 / (len(yv) - 4))
        if F > best[0]: best = (F, b)
    return best, m0
(F_obs, b_obs), m0 = supF(sa.values)
# sieve bootstrap: fit AR(p) to residuals of the no-break model, resample innovations
resid = m0.resid; p_ar = 2
ar = sm.OLS(resid[p_ar:], np.column_stack([resid[p_ar - i - 1:len(resid) - i - 1] for i in range(p_ar)])).fit()
innov = ar.resid - ar.resid.mean(); B = 499; Fb = np.empty(B)
for i in range(B):
    e = np.zeros(n); e[:p_ar] = resid[:p_ar]
    draw = rng.choice(innov, size=n, replace=True)
    for s in range(p_ar, n): e[s] = sum(ar.params[i] * e[s - 1 - i] for i in range(p_ar)) + draw[s]
    yb = m0.fittedvalues + e; Fb[i] = supF(yb)[0][0]
p_supF = float((Fb >= F_obs).mean())
R["supF_trend"] = dict(F=float(F_obs), break_date=str(dates[b_obs].date()), bootstrap_p=p_supF, B=B, crit95=float(np.quantile(Fb, 0.95)))
print("supF", R["supF_trend"])
# bootstrap 90% CI for break dates of the selected model (parametric: fitted segmented trend + sieve-AR residuals)
fit_sel, slopes_sel = seg_fit(sa.values, res_seg[k_sel]["idx"]); r_sel = sa.values - fit_sel
ar2 = sm.OLS(r_sel[p_ar:], np.column_stack([r_sel[p_ar - i - 1:len(r_sel) - i - 1] for i in range(p_ar)])).fit(); inn2 = ar2.resid - ar2.resid.mean()
Bc = 299; bk_boot = []
for i in range(Bc):
    e = np.zeros(n); e[:p_ar] = r_sel[:p_ar]; draw = rng.choice(inn2, size=n, replace=True)
    for s in range(p_ar, n): e[s] = sum(ar2.params[i] * e[s - 1 - i] for i in range(p_ar)) + draw[s]
    yb = fit_sel + e
    bb = rpt.Dynp(model="linear", min_size=H, jump=1).fit(np.column_stack([yb, t, np.ones(n)])).predict(n_bkps=k_sel)[:-1]
    bk_boot.append(bb)
bk_boot = np.array(bk_boot)
ci = [(str(dates[int(np.quantile(bk_boot[:, j], 0.05))].date()), str(dates[int(np.quantile(bk_boot[:, j], 0.95))].date())) for j in range(k_sel)]
R["segmented_trend"] = dict(bic={str(k): v["bic"] for k, v in res_seg.items()}, selected_k=k_sel, breaks=res_seg[k_sel]["breaks"], ci90=ci,
                            slopes_annual_pct=[float((np.exp(s * 12) - 1) * 100) for s in slopes_sel])
print("segmented", R["segmented_trend"])

# ---------------- (1b) breaks in the growth rate (differenced SA log series) ----------------
g = sa.diff().dropna().values; gd = dates[1:]
algo_g = rpt.Dynp(model="l2", min_size=H, jump=1).fit(g.reshape(-1, 1))
res_g = {}
for k in [0, 1, 2, 3]:
    bks = [] if k == 0 else algo_g.predict(n_bkps=k)[:-1]
    idx = [0] + list(bks) + [len(g)]; rss = sum(((g[a:b] - g[a:b].mean()) ** 2).sum() for a, b in zip(idx[:-1], idx[1:]))
    res_g[k] = dict(breaks=[str(gd[b].date()) for b in bks], bic=len(g) * np.log(rss / len(g)) + (2 * k + 1) * np.log(len(g)),
                    means_annual_pct=[float((np.exp(g[a:b].mean() * 12) - 1) * 100) for a, b in zip(idx[:-1], idx[1:])])
kg = min(res_g, key=lambda k: res_g[k]["bic"])
R["growth_rate_breaks"] = dict(bic={str(k): v["bic"] for k, v in res_g.items()}, selected_k=kg, breaks=res_g[kg]["breaks"], means_annual_pct=res_g[kg]["means_annual_pct"], all=res_g)
print("growth-rate breaks", R["growth_rate_breaks"])

# figure: SA series with segmented trend and CI bands
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.plot(dates, np.expm1(sa), color="#000000", lw=1.2, label="Seasonally adjusted arrivals")
ax.plot(dates, np.expm1(fit_sel), color="#000000", lw=1.6, ls="--", label=f"Segmented log-linear trend ({k_sel} breaks, BIC)")
for (lo, hi), d in zip(ci, res_seg[k_sel]["breaks"]):
    ax.axvspan(pd.Timestamp(lo), pd.Timestamp(hi), color="#bdbdbd", alpha=0.5, lw=0)
    ax.axvline(pd.Timestamp(d), color="#444444", ls=":", lw=1); ax.text(pd.Timestamp(d), 5, " " + d[:7], fontsize=8, va="bottom")
ax.set_ylabel("Arrivals per month"); ax.legend(loc="upper left", fontsize=8); ax.margins(x=0.01)
fig.savefig(P("figures/bw/rev_segmented_trend.png")); plt.close()

# ---------------- (2) simulated annual prediction intervals ----------------
best_a = (0, 1, 2), (0, 1, 1, 12); best_n = (1, 1, 1), (1, 1, 1, 12)
def sim_annual(series, order, sorder, Hh=51, reps=1000):
    ls = np.log1p(series.astype(float)); m = SARIMAX(ls, order=order, seasonal_order=sorder, enforce_stationarity=True, enforce_invertibility=True).fit(disp=False)
    np.random.seed(2026); sims = m.simulate(nsimulations=Hh, repetitions=reps, anchor="end")  # DataFrame Hh x reps
    sims = np.expm1(np.asarray(sims)); fidx = pd.date_range("2026-10-01", periods=Hh, freq="MS")
    ann_obs = series.groupby(series.index.year).sum()
    out = {}
    for yr in range(2026, 2031):
        mask = (fidx.year == yr); tot_y = sims[mask].sum(axis=0) + (ann_obs.loc[2026] if yr == 2026 else 0)
        out[yr] = dict(median=float(np.median(tot_y)), lo80=float(np.quantile(tot_y, 0.10)), hi80=float(np.quantile(tot_y, 0.90)), lo95=float(np.quantile(tot_y, 0.025)), hi95=float(np.quantile(tot_y, 0.975)))
    return pd.DataFrame(out).T
pi_a = sim_annual(tot.arrivals, *best_a); pi_n = sim_annual(tot.nights, *best_n)
pi_a.to_csv(P("outputs/rev_annual_PI_arrivals.csv")); pi_n.to_csv(P("outputs/rev_annual_PI_nights.csv"))
R["annual_PI_arrivals"] = pi_a.round(0).to_dict(); R["annual_PI_nights"] = pi_n.round(0).to_dict()
print(pi_a.round(0)); print(pi_n.round(0))


# ---------------- (2b) projection figure with simulated 80% band and distinct markers (journal version) ----------------
fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
for ax, name, lab, pi in zip(axes, ["arrivals", "nights"], ["Arrivals", "Overnight stays"], [pi_a, pi_n]):
    h = tot[name].astype(float); ah = h.groupby(h.index.year).sum()
    yv = pd.read_csv(P(f"outputs/table8_projection_annual_{name}.csv"), index_col=0)
    ax.bar(ah.index[ah.index < 2026], ah[ah.index < 2026], color="#9a9a9a", width=0.7, label="Actual")
    ax.bar([2026], [ah.loc[2026]], color="#d0d0d0", width=0.7, label="2026 actual Jan-Sep")
    ax.fill_between(pi.index, pi.lo80, pi.hi80, color="#c8c8c8", alpha=0.6, lw=0, label="SARIMA 80% interval (1,000 simulated paths)")
    for col, ls, mk, lb in [("SARIMA", "-", "o", "SARIMA"), ("ETS_log", "--", "s", "ETS (log)"), ("HoltWinters", "-.", "^", "Holt-Winters"), ("Combination", ":", "D", "Combination")]:
        ax.plot(yv.index, yv[col], color="#000000", lw=1.3, ls=ls, marker=mk, ms=4, label=lb)
    ax.set_title(lab, loc="left", fontsize=9); ax.set_xticks(range(2016, 2031)); ax.tick_params(axis="x", rotation=60)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k")); ax.set_ylim(0, pi.hi80.max() * 1.05)
axes[0].legend(fontsize=7.5, loc="upper left")
fig.savefig(P("figures/bw/rev_projections.png")); plt.close()

# ---------------- (3) rolling-origin cross-validation, horizons 1-12 ----------------
def ro_cv(series, order, sorder, origins):
    rows = []
    for o in origins:
        train = series[:o]; ltr = np.log1p(train.astype(float)); test = series[o:][:12]
        if len(test) < 1: continue
        h = len(test)
        f = {}
        f["SARIMA"] = np.expm1(SARIMAX(ltr, order=order, seasonal_order=sorder, enforce_stationarity=True, enforce_invertibility=True).fit(disp=False).forecast(h))
        f["ETS"] = np.expm1(ExponentialSmoothing(ltr, trend="add", damped_trend=True, seasonal="add", seasonal_periods=12, initialization_method="estimated").fit(optimized=True).forecast(h))
        f["HoltWinters"] = ExponentialSmoothing(train.astype(float), trend="add", damped_trend=True, seasonal="mul", seasonal_periods=12, initialization_method="estimated").fit(optimized=True).forecast(h)
        f["SeasonalNaive"] = pd.Series(train.values[-12:][np.arange(h) % 12], index=test.index)
        f["Combination"] = (f["SARIMA"].values + f["ETS"].values + f["HoltWinters"].values) / 3
        scale = np.mean(np.abs(train.values[12:] - train.values[:-12]))
        for k, v in f.items():
            v = np.asarray(v)
            for i in range(h):
                rows.append(dict(origin=str(o.date()), model=k, h=i + 1, actual=test.values[i], fc=v[i], ae=abs(test.values[i] - v[i]), ape=abs(test.values[i] - v[i]) / test.values[i], scale=scale))
    return pd.DataFrame(rows)
origins = pd.date_range("2022-01-01", "2025-09-01", freq="MS")  # 45 origins; last origin has 12-month test window to Sep 2026
cv = ro_cv(tot.arrivals, *best_a, origins); cv["ase"] = cv.ae / cv.scale
cv.to_csv(P("outputs/rev_rolling_origin_raw.csv"), index=False)
summ = cv.groupby(["model", "h"]).agg(MAPE=("ape", lambda x: 100 * x.mean()), MASE=("ase", "mean")).reset_index()
tab = summ.pivot(index="h", columns="model", values="MASE").round(2); tab2 = summ.pivot(index="h", columns="model", values="MAPE").round(1)
overall = cv.groupby("model").agg(MAPE=("ape", lambda x: 100 * x.mean()), MASE=("ase", "mean")).round(2)
h1_6 = cv[cv.h <= 6].groupby("model").agg(MAPE=("ape", lambda x: 100 * x.mean()), MASE=("ase", "mean")).round(2)
tab.to_csv(P("outputs/rev_rolling_origin_MASE_by_h.csv")); tab2.to_csv(P("outputs/rev_rolling_origin_MAPE_by_h.csv")); overall.to_csv(P("outputs/rev_rolling_origin_overall.csv"))
R["rolling_origin"] = dict(n_origins=int(cv.origin.nunique()), overall=overall.to_dict(), h1_6=h1_6.to_dict(), MASE_by_h=tab.to_dict())
print(tab); print(overall); print(h1_6)
fig, ax = plt.subplots(figsize=(7, 3.4))
for (k, ls, mk) in [("SARIMA", "-", "o"), ("ETS", "--", "s"), ("HoltWinters", "-.", "^"), ("SeasonalNaive", ":", "x"), ("Combination", (0, (5, 1, 1, 1)), "D")]:
    ax.plot(tab.index, tab[k], color="#000000", ls=ls, marker=mk, ms=4, lw=1.3, label=k)
ax.set_xlabel("Forecast horizon (months)"); ax.set_ylabel("MASE"); ax.set_xticks(range(1, 13)); ax.legend(fontsize=8, ncol=2)
fig.savefig(P("figures/bw/rev_rolling_origin.png")); plt.close()

# ---------------- (4) market x season percentages (replaces chord diagram) ----------------
lng = pd.read_csv(P("data/processed/evisitor_knin_long.csv")); lng = lng[(lng.span == "month") & (lng.year >= 2023)]
cm = lng.groupby(["country", "month"]).arrivals.sum().unstack(fill_value=0)
top10 = cm.sum(axis=1).sort_values(ascending=False).head(10).index
cm2 = cm.loc[top10].copy(); cm2.loc["Other markets"] = cm.drop(top10).sum()
en = {"Hrvatska": "Croatia", "Njemačka": "Germany", "Srbija": "Serbia", "Bosna i Hercegovina": "Bosnia and Herzegovina", "Poljska": "Poland", "Francuska": "France", "Austrija": "Austria", "Češka": "Czechia", "Slovenija": "Slovenia", "Italija": "Italy"}
cm2.index = [en.get(c, c) for c in cm2.index]
grp = {"Nov-Mar": [11, 12, 1, 2, 3], "Apr-May": [4, 5], "Jun-Aug": [6, 7, 8], "Sep-Oct": [9, 10]}
ms = pd.DataFrame({k: cm2[v].sum(axis=1) for k, v in grp.items()}); ms["Total"] = ms.sum(axis=1)
pct = ms[list(grp)].div(ms.Total, axis=0) * 100; out = pct.round(1); out["Arrivals 2023-2026"] = ms.Total.astype(int)
out.loc["All markets"] = list((ms[list(grp)].sum() / ms.Total.sum() * 100).round(1)) + [int(ms.Total.sum())]
out.to_csv(P("outputs/rev_market_season_pct.csv")); print(out)
# B/W heatmap figure as alternative
fig, ax = plt.subplots(figsize=(6.5, 4.2))
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("g", ["#f7f7f7", "#1a1a1a"])
im = ax.imshow(pct.values, cmap=cmap, aspect="auto", vmin=0, vmax=80); ax.grid(False)
ax.set_xticks(range(4)); ax.set_xticklabels(list(grp)); ax.set_yticks(range(len(pct))); ax.set_yticklabels(pct.index)
for i in range(pct.shape[0]):
    for j in range(4):
        v = pct.values[i, j]; ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8, color="white" if v > 45 else "black")
fig.savefig(P("figures/bw/rev_market_season_heatmap.png")); plt.close()

# ---------------- (5) DZS comparison if the file exists ----------------
dz = P("data/external/dzs_tu12.csv")
if os.path.exists(dz):
    d = pd.read_csv(dz)
    R["dzs"] = "file present; see 06_dzs_comparison.py"
else:
    R["dzs"] = "data/external/dzs_tu12.csv not available (PxWeb POST blocked from this environment)"
json.dump(R, open(P("outputs/revision.json"), "w"), indent=2, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
print("DONE")
