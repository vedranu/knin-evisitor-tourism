import pandas as pd, glob, re, sys, os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "EVISITOR GODINE")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "processed")
os.makedirs(OUT, exist_ok=True)

rows = []
log = []
for f in sorted(glob.glob(SRC + "/**/*.xlsx", recursive=True)):
    df = pd.read_excel(f, header=None, engine="calamine")
    txt = "\n".join(str(x) for x in df[0].tolist())
    m = re.search(r"Od datuma = (\d+)\.(\d+)\.(\d+)\.; Do datuma = (\d+)\.(\d+)\.(\d+)\.", txt)
    if not m:
        log.append(("NO DATE", f)); continue
    d1 = tuple(int(x) for x in m.groups()[:3]); d2 = tuple(int(x) for x in m.groups()[3:])
    name = df[0].tolist()[0]
    report = str(name).replace("Naziv izvještaja: ", "")
    span = "year" if (d1[1] == 1 and d2[1] == 12) else "month"
    # locate header row
    hdr = df.index[df[0] == "Država"].tolist()
    if not hdr:
        log.append(("NO COUNTRY TABLE", f, report, d1, d2)); continue
    h = hdr[0]
    tab = df.iloc[h+1:].copy()
    tab.columns = df.iloc[h].tolist()
    tab = tab.dropna(subset=["Država"])
    tab = tab[~tab["Država"].astype(str).str.contains("turisti:|UKUPNO", regex=True)]
    for _, r in tab.iterrows():
        rows.append(dict(year=d1[2], month=d1[1], span=span, country=str(r["Država"]).strip(),
                         arrivals=int(r["Dolasci"]), nights=int(r["Noćenja"]), tourists=int(r["Broj turista"]),
                         file=os.path.relpath(f, SRC)))
    log.append(("OK", os.path.relpath(f, SRC), span, d1, d2))

db = pd.DataFrame(rows)
for l in log: print(l)
mon = db[db.span == "month"]
print("monthly files:", mon.groupby(["year", "month"]).ngroups)
# check duplicates / missing
got = set(zip(mon.year, mon.month))
expected = [(y, m) for y in range(2016, 2027) for m in range(1, 13) if (y, m) <= (2026, 9)]
print("missing:", [e for e in expected if e not in got])
dup = mon.groupby(["year", "month"]).file.nunique(); print("dups:", dup[dup > 1])
db.to_csv(OUT + "/evisitor_knin_long.csv", index=False)
# monthly totals
tot = mon.groupby(["year", "month"])[["arrivals", "nights", "tourists"]].sum().reset_index()
tot["domestic_arr"] = mon[mon.country == "Hrvatska"].groupby(["year", "month"]).arrivals.sum().values
tot["domestic_nights"] = mon[mon.country == "Hrvatska"].groupby(["year", "month"]).nights.sum().values
tot["foreign_arr"] = tot.arrivals - tot.domestic_arr
tot["foreign_nights"] = tot.nights - tot.domestic_nights
tot["date"] = pd.to_datetime(dict(year=tot.year, month=tot.month, day=1))
tot.to_csv(OUT + "/monthly_totals.csv", index=False)
print(tot.to_string())
# compare yearly sum of months vs yearly file
yr = db[db.span == "year"].groupby("year")[["arrivals", "nights"]].sum()
ym = mon.groupby("year")[["arrivals", "nights"]].sum()
print(pd.concat([yr, ym], axis=1, keys=["yearfile", "sum_months"]))

# ---- fix 2017: '5.svibanj 2017.xlsx' was exported with April parameters -> drop it, impute May from yearly file
db = db[db.file != "2017/2017-po mjesecima/5.svibanj 2017.xlsx"]
y17 = db[(db.span=="year")&(db.year==2017)].set_index("country")[["arrivals","nights","tourists"]]
m17 = db[(db.span=="month")&(db.year==2017)].groupby("country")[["arrivals","nights","tourists"]].sum()
may = (y17 - m17.reindex(y17.index).fillna(0))
print("May 2017 imputed, negatives:", (may<0).sum().to_dict())
may = may.clip(lower=0).reset_index()
may["year"]=2017; may["month"]=5; may["span"]="month"; may["file"]="IMPUTED from 2017 yearly file"
db = pd.concat([db, may], ignore_index=True)
mon = db[db.span=="month"]
db.to_csv(OUT + "/evisitor_knin_long.csv", index=False)
tot = mon.groupby(["year","month"])[["arrivals","nights","tourists"]].sum().reset_index()
dom = mon[mon.country=="Hrvatska"].groupby(["year","month"])[["arrivals","nights"]].sum().reset_index().rename(columns={"arrivals":"domestic_arr","nights":"domestic_nights"})
tot = tot.merge(dom, on=["year","month"], how="left").fillna(0)
tot["foreign_arr"]=tot.arrivals-tot.domestic_arr; tot["foreign_nights"]=tot.nights-tot.domestic_nights
tot["date"]=pd.to_datetime(dict(year=tot.year,month=tot.month,day=1))
tot = tot.sort_values("date")
tot.to_csv(OUT+"/monthly_totals.csv", index=False)
print(tot[tot.year==2017])
print(len(tot), "months")
yr = db[db.span=="year"].groupby("year")[["arrivals","nights"]].sum(); ym = mon.groupby("year")[["arrivals","nights"]].sum()
print(pd.concat([yr, ym], axis=1, keys=["yearfile","sum_months"]))
