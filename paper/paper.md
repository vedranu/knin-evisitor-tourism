---
title: "From transit stop to destination? A decade of e-Visitor data on tourism growth, seasonality, source-market structure and projections for Knin, Croatia (2016-2026)"
author:
  - "Vedran Uroš^1,2^, [Co-author Sorić]^[affiliation to be added]^"
date: "Draft, October 2026"
---

^1^ University of Applied Sciences "Marko Marulić" in Knin, Croatia (vuros@veleknin.hr, ORCID 0009-0007-6568-0827)
^2^ Faculty of Organization and Informatics, University of Zagreb, Varaždin, Croatia

# Abstract

This paper analyses the development of tourism in Knin, a small inland town in the Dalmatian hinterland of Croatia, using the complete monthly record of the national e-Visitor registration system from January 2016 to September 2026 (129 months, 75 source markets). Four questions are addressed: how fast tourism grew and whether the growth path changed after the COVID-19 pandemic; whether growth changed the seasonal profile; how the source-market structure evolved; and what the data imply for the period to 2030. Tourist arrivals rose from 1,404 in 2016 to 6,178 in 2025 (compound annual growth 17.9 %) and overnight stays from 3,456 to 12,558 (15.4 %), with growth concentrated in 2021-2025 (34.5 % per year). Structural-break estimation on the seasonally adjusted series places the main regime shift in 2022-2023 rather than at the pandemic shock, and the post-pandemic trend (32.7 % per year) is roughly twice the pre-pandemic trend (16.8 %). Seasonality measured by the Gini coefficient of monthly arrivals fluctuated between 0.35 and 0.47 with no significant trend; the July-August share fell from 43 % to 35 %, but the winter share also fell, so growth spread into the shoulder months rather than the off-season. The share of foreign arrivals rose from 49 % to 63 %, the number of active source markets from 38 to 59, and the foreign-market Herfindahl-Hirschman index stayed low (0.06-0.08), with Germany, Serbia, Poland, France and Bosnia and Herzegovina as leading foreign markets. Average length of stay fell from 2.5 to 2.0 nights, which keeps Knin in the transit-destination category. Out-of-sample validation of SARIMA, ETS and Holt-Winters models on a 21-month hold-out (January 2025 to September 2026) shows that all models over-predicted the 2026 season, because growth stalled in 2026 (arrivals January-September +0.2 % year on year). Projections to 2030 therefore diverge: trend-extrapolating SARIMA gives about 12,000 arrivals and 24,000 overnight stays, damped exponential smoothing a plateau at about 5,800 and 12,000-16,000, and the model combination about 7,900 arrivals and 17,600 overnight stays. The paper argues that the 2026 stall marks the end of the post-pandemic catch-up phase and that further growth depends on converting transit visitors into longer stays. Data and code are published for reuse.

**Keywords:** tourism demand, e-Visitor, seasonality, Gini coefficient, source-market concentration, structural break, SARIMA, exponential smoothing, hinterland tourism, Croatia

# 1. Introduction

Croatian tourism is concentrated on the Adriatic coast, both in space and in time. The coastal counties receive more than 90 % of overnight stays, and the summer peak is among the most pronounced in Europe (Duro & Turrión-Prats, 2019; Payne, Nazlioglu & Mervar, 2023). National and regional strategies have for years named the dispersion of demand towards the hinterland and the off-season as policy goals. Whether these goals are being met is usually assessed at the county or national level, where small inland destinations are invisible in aggregate statistics. This paper looks at one such destination, the town of Knin in Šibenik-Knin County, over the first decade of the national e-Visitor registration system.

Knin is a town of about 11,000 inhabitants, 55 km inland from Šibenik, on the main road and railway corridor between Zagreb and Split and close to the northern entrance of Krka National Park. Its tourism offer rests on the Knin Fortress, the source of the river Krka, the Dinara mountain nature park and the proximity to the Krka and Plitvice national parks. In the typology of visitor movement (Lew & McKercher, 2006; Lue, Crompton & Fesenmaier, 1993), Knin has been an en-route stop rather than a base: visitors pass through on the way to the coast, stay one or two nights and move on. The Institute for Tourism's capacity study for Šibenik-Knin County identified the hinterland cluster, to which Knin belongs, as the cluster with the largest unused growth potential in the county (Institut za turizam, 2019). The question addressed here is whether the decade 2016-2026 shows that potential being realised and whether the growth changed the character of the destination.

The empirical material is the complete monthly record of the e-Visitor system for the area of the Knin tourist board, from January 2016, when the system was introduced, to September 2026. e-Visitor is the mandatory national register of tourist arrivals and overnight stays in Croatia and the source of the official statistics of the Croatian Bureau of Statistics (Marušić, Kožul & Brozović, 2020). The data set comprises 129 monthly observations of arrivals and overnight stays by country of origin for 75 reported markets. To the authors' knowledge, no peer-reviewed study has analysed tourism in Knin, and few studies have used a decade of monthly e-Visitor data for a single small inland destination.

The paper makes four contributions. First, it documents the growth of tourism in Knin and tests for structural change in the growth path around the COVID-19 pandemic and the 2023 adoption of the euro and entry into the Schengen area. Second, it measures seasonality with the Gini coefficient and related indicators and tests whether growth changed the seasonal profile. Third, it describes the source-market structure with concentration indices and market-by-season flow diagrams. Fourth, it produces validated forecasts and scenario projections to 2030 and discusses why forecasting models disagree at the current turning point. Data, code and figures are published in an open repository so that the analysis can be reproduced and extended to other destinations.

The rest of the paper is structured as follows. Section 2 reviews the literature on tourism demand forecasting, seasonality measurement, source-market concentration and structural change. Section 3 describes the data and methods. Section 4 presents the results. Section 5 discusses the findings and their implications. Section 6 concludes.

# 2. Literature review

## 2.1 Tourism demand modelling and forecasting

Tourism demand forecasting is a mature field with several reviews (Song & Li, 2008; Wu, Song & Shen, 2017; Song, Qiu & Park, 2019). Three families of methods dominate: time-series models, econometric models with explanatory variables, and, more recently, machine-learning and mixed-frequency methods. For small destinations with short monthly series and no local explanatory variables at monthly frequency, univariate time-series models remain the practical choice. The tourism forecasting competition of Athanasopoulos, Hyndman, Song and Wu (2011) found that for monthly and quarterly tourism series, seasonal exponential smoothing (ETS) and seasonal ARIMA models perform well, that simple seasonal naive forecasts are hard to beat at short horizons, and that forecast combinations are robust. These findings motivate the model set used here: seasonal ARIMA (Box & Jenkins, 1970), the ETS state-space family (Hyndman, Koehler, Snyder & Grose, 2002; Hyndman & Khandakar, 2008), the multiplicative Holt-Winters method (Winters, 1960), the seasonal naive benchmark and a simple combination. Forecast accuracy is assessed with the scale-free measures recommended by Hyndman and Koehler (2006). Seasonality in tourism series is often better treated as stochastic than deterministic (Kulendran & Wong, 2005), which supports the use of seasonal differencing and seasonal smoothing rather than fixed monthly dummies. For Croatia, Apergis, Mervar and Payne (2017) forecast disaggregated arrivals by source market with seasonal ARIMA and related models, and Mervar and Payne (2007) estimated long-run elasticities of foreign demand for Croatian destinations.

## 2.2 Measuring seasonality

Seasonality is the most studied structural feature of tourism demand (Butler, 1994, 2001; Koenig-Lewis & Bischoff, 2005). Lundtorp (2001) classified measures into amplitude measures (seasonality ratio, peak share) and concentration measures (coefficient of variation, Gini coefficient). The Gini coefficient of monthly values has become the standard concentration measure since Fernández-Morales (2003) showed that it can be decomposed by source market, which allows the contribution of each market to overall seasonal concentration to be quantified (Cisneros-Martínez & Fernández-Morales, 2015; Fernández-Morales, Cisneros-Martínez & McCabe, 2016; Duro, 2016). Duro and Turrión-Prats (2019) computed Gini coefficients for a large set of countries and found Croatia among the most seasonal destinations in the world. Croatian studies confirmed this at the national and county level (Kožić, Krešić & Boranić-Živoder, 2013; Mak & Kovač, 2021), and Payne, Gil-Alana, Mervar and Goenechea (2023) found that the pandemic changed the persistence and seasonality of coastal county series. Whether inland destinations follow the coastal pattern is an open question that this paper addresses for one case.

## 2.3 Source-market structure

The concentration of demand on few source markets exposes a destination to shocks in those markets. The Herfindahl-Hirschman index (HHI) of market shares is the usual measure; Ağazade (2022) and Ağazade, Tükenmez and Uzun (2023) showed for Turkey that source-market concentration affects the level and the volatility of tourism revenues. The inverse of the HHI, the effective number of markets, is easier to interpret. Diversification across markets is also linked to seasonality, because different markets travel in different months (Fernández-Morales et al., 2016), which is why this paper presents market-by-season flows jointly.

## 2.4 Structural change, the pandemic and institutional integration

The COVID-19 pandemic was the largest shock to tourism in the post-war period (Gössling, Scott & Hall, 2021; Škare, Soriano & Porada-Rochoń, 2021), and recovery took different paths in different destinations (Fotiadis, Polyzos & Huan, 2021; Zhang, Song, Wen & Liu, 2021; Čorak, Boranić Živoder & Marušić, 2020). Payne, Gil-Alana and Mervar (2022) found that Croatian tourism series changed persistence after the pandemic. Structural change in a time series is tested with the Chow (1960) test when the break date is known and estimated with the Bai and Perron (1998, 2003) procedure when it is not. Croatia's accession to the European Union in 2013 had a measurable effect on tourism (Tkalec, 2024); the adoption of the euro and entry into Schengen on 1 January 2023 may have had similar effects through lower transaction costs and the removal of border queues (Gil-Pareja, Llorca-Vivero & Martínez-Serrano, 2007; Santana-Gallego, Ledesma-Rodríguez & Pérez-Rodríguez, 2010; Franjić, Jagodič, Božinovski & Jurakić, 2026), but no study has yet quantified this for a destination. Growth paths of destinations are also interpreted through the tourism area life cycle (Butler, 1980), which Lundtorp and Wanhill (2001) formalised as a logistic curve whose carrying capacity can be estimated from arrivals data.

## 2.5 Hinterland tourism in Croatia

Croatian tourism is spatially concentrated on the coast (Kranjčević & Hajdinjak, 2019) and regional convergence between coastal and continental counties has been slow (Payne, Nazlioglu & Mervar, 2023). Studies of the Dalmatian hinterland are few. Radeljak Kaufmann (2020) analysed rural tourism around Krka National Park and found spillover effects on the surrounding municipalities. Opačić, Klarić, Beroš and Boranić Živoder (2022) built a tourism development index for all Croatian local self-government units and placed inland towns such as Knin in the lowest categories. Tomljenović and Kunst (2014) discussed diversification from sun-and-sea towards cultural tourism in Dalmatia, and Koens, Postma and Papp (2018) discussed the dispersal of visitors from saturated hotspots as a response to overtourism. This paper adds a quantitative, decade-long case study to this thin literature.

# 3. Data and methods

## 3.1 Data

The data are monthly reports exported from the e-Visitor system by the Tourist Board of the City of Knin for the area "Šibensko-kninska - Knin", all accommodation types, tourists only (excursionists excluded), all billing categories (commercial per night, commercial flat-rate, camps, non-commercial and exempt). Each monthly report lists arrivals, overnight stays and number of tourists by country of origin, using the country classification of the Croatian Bureau of Statistics (75 reported countries and residual groups). Reports cover January 2016 to September 2026 (129 months); annual reports for 2016-2025 were used to check the monthly totals. The reports were exported in September 2026, so data for 2016-2025 are final and data for 2026 reflect the state of the register at the end of September 2026.

Two data problems were found and resolved. First, several files were mislabelled (for example, a file named "May 2017" contained an April 2017 export); the month of each file was therefore taken from the date parameters stored inside the file, not from the file name. Second, no valid export existed for May 2017; the May 2017 values were reconstructed for each country as the difference between the 2017 annual report and the sum of the other eleven months, which reproduces the annual totals exactly. The monthly totals of all other years match the annual reports.

e-Visitor is an administrative register. Marušić et al. (2020) discuss its limitations: non-commercial stays (second homes, visits to friends and relatives) are under-registered, and compliance improved in the first years after introduction, so 2016 may be slightly understated relative to later years. These limitations affect levels more than growth rates and seasonal patterns.

## 3.2 Descriptive indicators

Annual arrivals, overnight stays, the foreign share and average length of stay (ALOS, overnight stays per arrival) are tabulated. Growth is summarised by compound annual growth rates (CAGR). For 2026 only January-September is available, so 2026 is compared with the same months of 2025.

## 3.3 Decomposition and seasonality

Monthly arrivals and overnight stays were log-transformed (log(1+y)) and decomposed with the robust STL procedure (Cleveland, Cleveland, McRae & Terpenning, 1990) with a seasonal period of 12. The strength of trend and seasonality was computed as F_T = 1 - Var(R)/Var(T+R) and F_S = 1 - Var(R)/Var(S+R), where T, S and R are the trend, seasonal and remainder components (Hyndman & Athanasopoulos, 2021). For each complete year, seasonality was measured by the Gini coefficient of the twelve monthly values (Fernández-Morales, 2003; Lundtorp, 2001), the seasonality ratio (peak month over mean month), the coefficient of variation, the July-August share and the November-March share. A time trend in the Gini coefficient was tested with Kendall's tau and ordinary least squares.

## 3.4 Source-market structure

For each year the HHI of arrivals across countries was computed for all markets and for foreign markets only, together with the effective number of markets (1/HHI), the share of the five largest markets and the number of markets with at least one arrival. Market-by-season flows for 2023-2026 were visualised with a chord diagram linking the ten largest markets (and a residual group) to four seasons (November-March, April-May, June-August, September-October).

## 3.5 Structural change

Structural breaks were estimated on the seasonally adjusted log arrivals (log series minus the STL seasonal component). Break dates for one to three breaks in the mean were estimated by dynamic programming with a minimum segment length of 18 months, which is the exact-solution algorithm of Bai and Perron (2003); the number of breaks was selected by the Bayesian information criterion. Chow (1960) tests of a change in intercept and slope of a linear trend were computed at three a priori dates: March 2020 (pandemic), June 2021 (reopening) and January 2023 (euro and Schengen). Pre- and post-pandemic trend growth rates were estimated by regressing seasonally adjusted log arrivals on time for 2016-2019 and for June 2021 to September 2026. Stationarity was examined with the augmented Dickey-Fuller and KPSS tests.

## 3.6 Forecasting models and validation

Four models were fitted to monthly arrivals and overnight stays: (i) a seasonal ARIMA(p,1,q)(P,1,Q)~12~ model on the log scale, with the orders p, q from 0 to 3 and P, Q from 0 to 2 selected by the Akaike information criterion under stationarity and invertibility constraints, and residuals checked with the Ljung-Box test; (ii) an ETS(A,A~d~,A) model on the log scale, that is, additive damped trend and additive seasonality, which corresponds to multiplicative seasonality on the original scale; (iii) the Holt-Winters method with damped additive trend and multiplicative seasonality on the original scale; (iv) the seasonal naive method as benchmark; and (v) the arithmetic mean of models (i) to (iii) as a combination. Models were estimated on January 2016 to December 2024 and evaluated on the 21-month hold-out from January 2025 to September 2026 with the mean absolute percentage error (MAPE), the root mean squared error (RMSE), the mean absolute scaled error (MASE, scaled by the in-sample seasonal naive error) and the cumulative bias in per cent (Hyndman & Koehler, 2006). Final projections were produced by refitting each model on the full sample to September 2026 and forecasting 51 months ahead to December 2030; the 80 % prediction interval of the SARIMA model is reported. Annual totals for 2026 combine the observed January-September values with the forecasts for October-December. As a complementary long-run scenario, a logistic curve N(t) = K/(1 + exp(-r(t - t~0~))) was fitted to annual arrivals 2016-2026 by non-linear least squares (Lundtorp & Wanhill, 2001).

All computations were done in Python 3.13 with pandas, statsmodels 0.15, ruptures 1.1, SciPy and pyCirclize. The code, the consolidated data set and all outputs are available in the accompanying repository.

# 4. Results

## 4.1 Growth 2016-2026

Table 1 and Figure 1 summarise the decade. Arrivals grew from 1,404 in 2016 to 6,178 in 2025, overnight stays from 3,456 to 12,558. The compound annual growth rates for 2016-2025 are 17.9 % for arrivals and 15.4 % for overnight stays, but the growth was not uniform. From 2016 to 2019 arrivals rose by 43 % in total; 2020 brought a 39 % fall in arrivals but only an 11 % fall in overnight stays, because the few tourists who came stayed longer (ALOS 3.6 nights). The years 2021-2025 were a period of rapid expansion: arrivals grew at 34.5 % per year and overnight stays at 31.8 % per year, with the largest annual increases in 2023 (+59 % arrivals) and 2024 (+45 %). Growth decelerated to +7 % arrivals and +23 % overnight stays in 2025, and in 2026 it stopped: arrivals in January-September 2026 were 5,346, 0.2 % above the same months of 2025, and overnight stays were 11,328, 4.6 % above.

Table 1. Annual tourist arrivals and overnight stays in Knin, 2016-2026 (e-Visitor)

| Year | Arrivals | Overnight stays | Foreign share of arrivals (%) | ALOS (nights) | Arrivals y/y (%) | Nights y/y (%) |
|----------------------|--------:|--------:|--------:|--------:|--------:|--------:|
| 2016 | 1,404 | 3,456 | 49.4 | 2.46 | - | - |
| 2017 | 1,645 | 4,177 | 64.9 | 2.54 | +17.2 | +20.9 |
| 2018 | 1,565 | 4,129 | 62.4 | 2.64 | -4.9 | -1.1 |
| 2019 | 2,003 | 4,964 | 67.7 | 2.48 | +28.0 | +20.2 |
| 2020 | 1,227 | 4,432 | 52.2 | 3.61 | -38.7 | -10.7 |
| 2021 | 1,886 | 4,157 | 65.5 | 2.20 | +53.7 | -6.2 |
| 2022 | 2,503 | 5,755 | 66.7 | 2.30 | +32.7 | +38.4 |
| 2023 | 3,977 | 7,566 | 68.9 | 1.90 | +58.9 | +31.5 |
| 2024 | 5,758 | 10,236 | 67.2 | 1.78 | +44.8 | +35.3 |
| 2025 | 6,178 | 12,558 | 63.3 | 2.03 | +7.3 | +22.7 |
| 2026 (Jan-Sep) | 5,346 | 11,328 | 56.5 | 2.12 | +0.2* | +4.6* |

\* January-September 2026 compared with January-September 2025. ALOS = average length of stay. Source: authors' calculation from e-Visitor data.

![Figure 1. Monthly tourist arrivals and overnight stays in Knin, January 2016 to September 2026, domestic and foreign.](../figures/fig1_monthly_series.png)

The composition of demand changed in two ways. The foreign share of arrivals rose from 49 % in 2016 to a plateau of 63-69 % in 2019-2025, and fell back to 57 % in January-September 2026 as domestic arrivals continued to grow (+31 % year on year, domestic overnight stays +48 %) while foreign arrivals fell (-15 %). The average length of stay fell from 2.5-2.6 nights in 2016-2018 to 1.8-2.0 nights in 2023-2025, with a partial recovery to 2.1 nights in 2026. Growth was therefore driven by more, shorter visits.

## 4.2 Trend and seasonal components

The STL decomposition (Figure 2) separates a strong trend (F_T = 0.75 for arrivals, 0.67 for overnight stays) from a strong and stable seasonal component (F_S = 0.82 and 0.81). The seasonal component implies a peak-to-trough ratio of about 13 for arrivals, which means that the August level is typically thirteen times the February level once the trend is removed. The trend component is flat from 2016 to 2019, dips in 2020, and rises steeply from mid-2021 to 2025, with the annualised slope of the trend over June 2021 to September 2026 equal to 29.5 %. The remainder component shows the pandemic months of April-May 2020 as the largest negative outliers and no comparable outliers afterwards.

![Figure 2. STL decomposition of log monthly arrivals in Knin, 2016-2026.](../figures/fig2_stl_arrivals.png)

Unit-root tests confirm that the log series is non-stationary in levels (ADF with trend: p = 0.68; KPSS: p = 0.10) and stationary after one regular and one seasonal difference (ADF: p < 0.001), which supports the (1,1) differencing structure of the SARIMA models.

## 4.3 Seasonality

Table 2 and Figure 3 present the seasonality indicators. The Gini coefficient of monthly arrivals ranged from 0.345 (2019) to 0.471 (2017), with 0.409 in 2016 and 0.381 in 2025. Neither Kendall's tau (-0.29, p = 0.29) nor the OLS slope (-0.003 per year, p = 0.47) indicates a significant trend. For overnight stays the coefficient moved from 0.424 to 0.397 (tau = 0.02, p = 1.00). The share of July and August in annual arrivals fell from 43 % in 2016 and 46 % in 2021-2022 to 35 % in 2025, and the seasonality ratio fell from 3.2 in 2021-2022 to 2.6 in 2025. The heatmap in Figure 3 shows where the peak share went: May, June and September, each of which gained two to four percentage points. The winter share (November-March) did not increase; it fell from 18 % in 2016 to 14 % in 2025, and winter arrivals grew more slowly (CAGR 14.8 %) than June-September arrivals (17.6 %).

Table 2. Seasonality indicators of monthly arrivals, complete years 2016-2025

| Year | Gini | Seasonality ratio | CV | Jul-Aug share (%) | Jun-Sep share (%) | Nov-Mar share (%) |
|----------------------|--------:|--------:|--------:|--------:|--------:|--------:|
| 2016 | 0.409 | 2.74 | 0.83 | 42.7 | 62.2 | 18.2 |
| 2017 | 0.471 | 3.46 | 0.98 | 44.9 | 64.8 | 13.4 |
| 2018 | 0.466 | 2.86 | 0.90 | 43.6 | 65.6 | 13.6 |
| 2019 | 0.345 | 2.40 | 0.66 | 35.4 | 58.3 | 17.2 |
| 2020 | 0.422 | 3.15 | 0.89 | 44.8 | 65.7 | 21.3 |
| 2021 | 0.440 | 3.24 | 0.92 | 45.9 | 67.5 | 14.7 |
| 2022 | 0.446 | 3.18 | 0.92 | 45.7 | 68.3 | 15.1 |
| 2023 | 0.422 | 2.80 | 0.83 | 41.8 | 65.3 | 14.1 |
| 2024 | 0.417 | 2.65 | 0.81 | 40.7 | 64.2 | 13.4 |
| 2025 | 0.381 | 2.57 | 0.73 | 34.9 | 60.9 | 14.3 |

Seasonality ratio = peak month / mean month; CV = coefficient of variation. Source: authors' calculation.

![Figure 3. Share of annual arrivals by month (left) and Gini coefficient of seasonality of arrivals and overnight stays (right), Knin 2016-2025.](../figures/fig3_seasonality.png)

Domestic demand is much less seasonal than foreign demand: the Gini coefficient of domestic arrivals was 0.23-0.32 in every year except 2020 (0.37), against 0.42-0.61 for foreign arrivals. Domestic visitors travel to Knin throughout the year, often for events, family and business reasons, while foreign visitors are concentrated in the summer transit season. The partial return of domestic demand in 2026 is consistent with the slight reduction in seasonality.

## 4.4 Source-market structure

Table 3 lists the fifteen largest markets. Croatia remained the largest single market but its share fell from 51 % in 2016 to 37 % in 2025. Germany rose from 4 % to 11 % and became the largest foreign market from 2019 onwards. Serbia (6 %), Poland (5 %), France (4.5 %), Bosnia and Herzegovina (4 %), Czechia (3.8 %), Austria (3.5 %), Italy (3.1 %) and Slovenia (2.8 %) complete the top ten. Between 2019 and 2025 the fastest-growing markets among the top ten were Austria (CAGR 36 %), Slovenia (33 %), Czechia (27 %), Serbia (26 %), Germany (24 %) and Croatia (23 %), while France (13 %), Italy (12 %) and the United Kingdom (5 %) grew more slowly. Markets that were prominent in 2016 because of single organised groups (Romania, Latvia, Belarus) disappeared. Average length of stay differs sharply by market: Serbian visitors stayed 3.7 nights in 2025, visitors from Bosnia and Herzegovina 2.4 and from the United States 2.4, while Italian (1.2), Czech (1.4) and Slovenian (1.4) visitors were almost pure transit traffic.

Table 3. Fifteen largest source markets by arrivals, 2016-2025

| Market | 2016 | 2019 | 2022 | 2025 | Share 2016 (%) | Share 2025 (%) | CAGR 2019-2025 (%) | ALOS 2025 |
|----------------------|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|
| Croatia | 710 | 647 | 834 | 2,270 | 50.6 | 36.7 | 23.3 | 1.93 |
| Germany | 56 | 193 | 249 | 686 | 4.0 | 11.1 | 23.5 | 1.85 |
| Serbia | 32 | 93 | 92 | 370 | 2.3 | 6.0 | 25.9 | 3.74 |
| Poland | 22 | 91 | 126 | 307 | 1.6 | 5.0 | 22.5 | 1.78 |
| France | 23 | 135 | 151 | 276 | 1.6 | 4.5 | 12.7 | 1.54 |
| Bosnia and Herzegovina | 53 | 103 | 71 | 245 | 3.8 | 4.0 | 15.5 | 2.39 |
| Czechia | 17 | 57 | 111 | 237 | 1.2 | 3.8 | 26.8 | 1.41 |
| Austria | 46 | 34 | 66 | 218 | 3.3 | 3.5 | 36.3 | 1.91 |
| Italy | 44 | 95 | 146 | 189 | 3.1 | 3.1 | 12.1 | 1.16 |
| Slovenia | 25 | 32 | 57 | 176 | 1.8 | 2.8 | 32.9 | 1.43 |
| Netherlands | 16 | 51 | 90 | 111 | 1.1 | 1.8 | 13.8 | 2.06 |
| United Kingdom | 26 | 72 | 45 | 98 | 1.9 | 1.6 | 5.3 | 1.86 |
| United States | 10 | 22 | 40 | 91 | 0.7 | 1.5 | 26.7 | 2.36 |
| Switzerland | 25 | 22 | 52 | 73 | 1.8 | 1.2 | 22.1 | 1.49 |
| Hungary | 5 | 27 | 20 | 66 | 0.4 | 1.1 | 16.1 | 1.55 |

Source: authors' calculation from e-Visitor data.

![Figure 4. Source-market structure of arrivals in Knin, 2016-2026 (2026 = January-September).](../figures/fig4_market_shares.png)

Concentration indices (Table 4) show a diversified foreign demand. The HHI across all markets fell from 0.272 in 2016, when Croatia dominated, to 0.12-0.16 in 2022-2025, and the effective number of markets rose from 3.7 to 6-8. Among foreign markets alone the HHI stayed between 0.058 and 0.082 over the whole decade, which corresponds to 12-17 effective foreign markets, and showed no trend (Kendall's tau = 0.16, p = 0.60). The share of the five largest markets fell from 71 % to 57-63 %, and the number of markets with at least one arrival rose from 38 to 59-60. Knin therefore does not depend on any single foreign market; the risk in its market structure lies in the dependence on summer transit traffic from Central Europe rather than in concentration by country.

Table 4. Source-market concentration of arrivals, 2016-2026

| Year | HHI all markets | HHI foreign markets | Effective number of foreign markets | Top-5 share (%) | Markets with arrivals > 0 |
|----------------------|--------:|--------:|--------:|--------:|--------:|
| 2016 | 0.272 | 0.066 | 15.1 | 70.6 | 38 |
| 2017 | 0.148 | 0.058 | 17.4 | 59.0 | 46 |
| 2018 | 0.164 | 0.058 | 17.3 | 61.6 | 44 |
| 2019 | 0.133 | 0.063 | 15.8 | 58.6 | 50 |
| 2020 | 0.251 | 0.082 | 12.2 | 72.8 | 40 |
| 2021 | 0.151 | 0.075 | 13.4 | 64.2 | 51 |
| 2022 | 0.139 | 0.064 | 15.7 | 60.2 | 50 |
| 2023 | 0.124 | 0.058 | 17.4 | 57.3 | 60 |
| 2024 | 0.136 | 0.063 | 15.8 | 58.8 | 53 |
| 2025 | 0.163 | 0.070 | 14.2 | 63.3 | 59 |
| 2026 (Jan-Sep) | 0.209 | 0.063 | 16.0 | 65.2 | 59 |

Source: authors' calculation.

The chord diagram in Figure 5 links the ten largest markets to the four seasons for 2023 to September 2026. Croatian demand is spread over all seasons, with the November-March band (2,062 arrivals) almost as large as the June-August band (2,863). Every foreign market is dominated by June-August: Germany sends 53 % of its arrivals in those three months, France 65 %, Italy 71 %, Poland 60 % and Serbia 62 %. The shoulder seasons are served mainly by Germany, Poland, Czechia, Austria and Slovenia in April-May and by Germany and the residual group in September-October. Winter foreign demand is negligible for all markets except Bosnia and Herzegovina and Serbia, whose winter arrivals reflect family and business ties rather than leisure tourism.

![Figure 5. Chord diagram of arrivals by source market and season, Knin, January 2023 to September 2026.](../figures/fig5_chord_market_season.png)

![Figure 6. Rolling 12-month arrivals by leading foreign market, 2016-2026.](../figures/fig10_markets_small_multiples.png)

Figure 6 shows the rolling 12-month arrivals for the six largest foreign markets. All six show the same shape: flat or slowly rising to 2019, a dip in 2020-2021, a steep rise from 2022 to 2024-2025 and a plateau or decline in 2026. In January-September 2026 all six markets were below the same months of 2025: Germany by 30 %, France by 39 %, Bosnia and Herzegovina by 28 %, Serbia by 21 %, Austria by 14 % and Poland by 8 %. Of the larger markets only Croatia (+31 %), Slovenia (+30 %) and the Netherlands (+11 %) grew.

## 4.5 Structural change

The dynamic-programming estimation of breaks in the mean of seasonally adjusted log arrivals (Figure 7) gives a single break in February 2023 when one break is allowed, breaks in May 2018 and February 2023 when two are allowed, and breaks in May 2018, July 2022 and March 2024 when three are allowed. The BIC favours three breaks over two by a small margin (-227.3 against -225.2) and both strongly over none (-82.9). In all specifications the dominant regime shift is placed in 2022-2023, not in 2020. The pandemic appears as a temporary level shift that is absorbed within the segment, because the series had returned to its 2019 level by mid-2021; the regime change that matters is the acceleration that started in mid-2022 and continued to early 2024, after which the level stabilised.

Chow tests reject parameter stability at all three a priori dates: March 2020 (F = 28.1, p < 0.001), June 2021 (F = 18.4, p < 0.001) and January 2023 (F = 17.9, p < 0.001). The pre-pandemic trend, estimated on 2016-2019, was 16.8 % per year; the post-pandemic trend, estimated on June 2021 to September 2026, was 32.7 % per year (standard error 1.5 percentage points). The post-pandemic growth path is thus not a return to the pre-pandemic trend but a steeper one, which is consistent with the break estimates. The data cannot separate the effect of the euro and Schengen accession from the general post-pandemic catch-up of Croatian and European tourism, because both occurred in the same period; Section 5 discusses this.

![Figure 7. Seasonally adjusted arrivals and estimated structural breaks.](../figures/fig6_structural_breaks.png)

## 4.6 Forecasting models and out-of-sample validation

The AIC selected a SARIMA(0,1,2)(0,1,1)~12~ model for log arrivals (AIC 136.7; Ljung-Box p = 0.84 at lag 12 and 0.33 at lag 24) and a SARIMA(1,1,1)(1,1,1)~12~ model for log overnight stays (AIC 138.4; Ljung-Box p = 0.28 and 0.07). Both are close to the airline model, with no evidence of remaining autocorrelation. The ETS models on the log scale estimated a level smoothing parameter of 0.34 (arrivals) and 0.31 (overnight stays), a trend smoothing parameter of zero and a damping parameter of 0.995, which means that the trend is fixed at its estimated value and damped very slowly.

Table 5 reports the accuracy on the 21-month hold-out. For arrivals the Holt-Winters model had the lowest MAPE (18.9 %), the seasonal naive benchmark the lowest RMSE and MASE (1.50), and the ETS model the smallest cumulative bias (-3.6 %). For overnight stays the ETS model had the lowest MAPE (24.8 %) and the seasonal naive benchmark again the lowest MASE (1.84); all models under-predicted overnight stays by 20-36 %, because the 2025 season brought a 23 % increase in overnight stays that no model fitted to 2016-2024 anticipated. All MASE values exceed one, which is expected for a 21-month horizon (MASE is scaled by one-step in-sample errors) but also reflects the turning point in 2026: as Figure 8 shows, every model, including the seasonal naive benchmark, over-predicted June to August 2026, when arrivals fell 12-20 % below the same months of 2025, after January-May 2026 had been 24-56 % above 2025. The combination did not outperform the best single model, but it was never the worst and had the smallest absolute bias for arrivals among the trend models.

Table 5. Out-of-sample forecast accuracy, hold-out January 2025 to September 2026 (21 months)

| Model | Arrivals MAPE (%) | Arrivals RMSE | Arrivals MASE | Arrivals bias (%) | Nights MAPE (%) | Nights RMSE | Nights MASE | Nights bias (%) |
|----------------------|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|
| SARIMA (log) | 26.9 | 236 | 2.23 | +7.8 | 27.0 | 371 | 2.15 | -24.0 |
| ETS(A,A~d~,A) (log) | 24.8 | 185 | 1.94 | -3.6 | 24.8 | 347 | 1.99 | -21.0 |
| Holt-Winters (A,A~d~,M) | 18.9 | 192 | 1.67 | +8.8 | 35.2 | 540 | 3.19 | -36.4 |
| Seasonal naive | 21.0 | 137 | 1.50 | -6.3 | 25.3 | 342 | 1.84 | -20.0 |
| Combination (mean of three) | 23.1 | 200 | 1.92 | +4.3 | 27.1 | 406 | 2.32 | -27.1 |

Bias = (sum of forecasts - sum of actuals) / sum of actuals. Source: authors' calculation.

![Figure 8. Out-of-sample validation of monthly arrival forecasts, models fitted on 2016-2024.](../figures/fig7_validation.png)

## 4.7 Projections to 2030

Table 6 and Figures 9 and 10 present the projections from models refitted on the full sample to September 2026. For the full year 2026 the models agree: 6,100-6,200 arrivals (0 to +1 % against 2025) and 13,000-13,200 overnight stays (+4 to +5 %). Beyond 2026 they diverge. The SARIMA models, which extrapolate the average growth of the differenced series over the whole sample, project 12,200 arrivals and 24,200 overnight stays in 2030, which would require a return to about 18 % annual growth. The damped-trend ETS and Holt-Winters models, whose estimated trend is close to zero at the end of the sample, project a plateau of 5,800 arrivals and 12,100-16,300 overnight stays. The combination gives 7,900 arrivals and 17,600 overnight stays in 2030, equivalent to about 6.5 % annual growth in arrivals and 7.5 % in overnight stays from 2026. The 80 % interval of the SARIMA model for 2030 (3,100 to 47,700 arrivals, obtained by summing monthly bounds and therefore conservative) illustrates the uncertainty of a four-year horizon for a series of this size.

Table 6. Annual projections of arrivals and overnight stays to 2030

| Year | Arrivals SARIMA | Arrivals ETS (log) | Arrivals Holt-Winters | Arrivals combination | Nights SARIMA | Nights ETS (log) | Nights Holt-Winters | Nights combination |
|----------------------|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|
| 2026* | 6,198 | 6,073 | 6,068 | 6,113 | 13,165 | 13,033 | 12,810 | 13,003 |
| 2027 | 7,490 | 5,812 | 5,764 | 6,355 | 15,361 | 13,296 | 12,139 | 13,599 |
| 2028 | 8,818 | 5,812 | 5,764 | 6,798 | 17,952 | 14,293 | 12,139 | 14,795 |
| 2029 | 10,380 | 5,812 | 5,764 | 7,318 | 20,879 | 15,300 | 12,139 | 16,106 |
| 2030 | 12,219 | 5,812 | 5,764 | 7,931 | 24,247 | 16,312 | 12,139 | 17,566 |

\* Observed January-September plus forecast October-December. Source: authors' calculation.

![Figure 9. Annual arrivals and overnight stays, actual 2016-2026 and projections to 2030.](../figures/fig8_projections.png)

![Figure 10. Monthly projections of arrivals to December 2030 with the SARIMA 80 % prediction interval.](../figures/fig9_monthly_projection.png)

The logistic curve fitted to annual arrivals gives a carrying capacity K of about 21,900 arrivals with an inflection point in 2029, but the standard error of K (50,300) is larger than the estimate itself. With ten complete years and the inflection not yet passed, the carrying capacity is not identified from the data; the logistic fit is reported only to show that the observed path is consistent with the early phase of a life-cycle curve, not to predict its ceiling.

# 5. Discussion

## 5.1 Growth and its drivers

The decade divides into three phases: slow growth to 2019 (about 17 % per year from a very low base), the pandemic interruption, and rapid expansion from mid-2021 to 2025 followed by a stall in 2026. The break estimates place the regime shift in 2022-2023, which coincides with three developments: the full reopening of European travel in 2022, Croatia's entry into the euro area and Schengen on 1 January 2023, and, possibly, growth in the local accommodation supply, which the e-Visitor exports used here do not record. The data cannot attribute the acceleration to any one of them. The Schengen effect should be strongest for transit traffic from Central Europe, because the removal of the Slovenian-Croatian border queue shortened the drive from Germany, Austria, Czechia and Poland, and those are indeed the markets that grew fastest between 2019 and 2025. But the same markets also grew strongly on the Croatian coast in the same years, so the Knin pattern may simply mirror national demand. A difference-in-differences comparison with similar inland towns in countries that did not join Schengen would be the natural next step and is outside the scope of this single-destination study.

The stall in 2026 deserves attention. Foreign arrivals in January-September 2026 fell 15 % below 2025 while domestic arrivals rose 31 %; the decline was concentrated in June-August and in the German, French, Bosnian, Serbian and Italian markets, while the first five months of 2026 were still 24-56 % above 2025. The pattern is consistent with the end of a catch-up phase in which the destination filled a gap in the market for inexpensive overnight stops on the way to the coast, and with the price-sensitivity of transit travellers after three years of strong price increases in Croatian tourism; a weaker summer season on the Croatian coast in 2026 would produce the same signature, and the two cannot be separated without comparable data for other destinations. The simultaneous growth of domestic demand in every month of 2026 shows that the stall is specific to the foreign summer segment. The forecasting exercise makes the same point from another angle: models fitted to 2016-2024 over-predicted 2026 by every measure, because the information in the data up to 2024 was "growth continues", and the realised path in 2026 was "growth stops".

## 5.2 Seasonality

The hypothesis that growth would spread demand into the off-season is not supported. The Gini coefficient did not fall significantly, and the winter share fell. What changed is the shape of the summer: the July-August share fell by eight to ten percentage points and the May, June and September shares rose. This is the pattern of a destination whose growth comes from the same transit flows spreading over a longer summer, not from new winter products. Compared with the coastal counties, whose seasonal concentration is among the highest in Europe (Kožić et al., 2013; Duro & Turrión-Prats, 2019; Payne et al., 2023), Knin is less seasonal, and its domestic demand (Gini 0.23-0.32) is only moderately seasonal. The decomposition by market in Figure 5 shows that off-season growth, if it comes, will come from domestic visitors and from the near markets (Bosnia and Herzegovina, Serbia, Slovenia), not from the Central European summer markets.

## 5.3 Market structure and the transit character

Knin's foreign demand is unusually diversified for a small destination: 12-17 effective foreign markets and no foreign market above 11 % of arrivals. The vulnerability of the destination lies elsewhere. Seven of the ten largest markets have an average length of stay below two nights, and the overall ALOS fell from 2.5 to 2.0 nights during the growth phase, which means that the new demand was even more transit-oriented than the old. In Lew and McKercher's (2006) terms, Knin grew as a node on the Zagreb-Split corridor, not as a base for exploring the hinterland. The exception is Serbia, with 3.7 nights, and to a lesser extent Bosnia and Herzegovina and the United States, which point to visiting-friends-and-relatives and heritage motives. The question in the title can therefore be answered: Knin became a much busier transit stop, but not yet a destination. The projection scenarios translate this into numbers. The plateau scenario of the damped models (5,800 arrivals) is what the data imply if nothing changes; the SARIMA scenario (12,200) is what the pre-2026 growth rate would deliver if it resumed; the combination (7,900) is a middle path. Converting a fraction of the transit visitors into two- or three-night stays would raise overnight stays without any increase in arrivals and is the lever with the highest return, because it does not depend on attracting new markets.

## 5.4 Methodological notes

Three methodological points deserve comment. First, the e-Visitor register gives a small destination a complete monthly census of registered tourists by market, which is a richer basis for analysis than the survey-based statistics available in most countries; the price is sensitivity to registration compliance in the early years and under-registration of non-commercial stays (Marušić et al., 2020). Second, the structural-break analysis shows that for a destination like Knin the pandemic was a transient shock and the regime change came later; studies that test only for a 2020 break will misdate the change. Third, the validation exercise shows that at a turning point the disagreement between model families is informative in itself: the gap between trend-extrapolating and damped models is a measure of how much the future depends on whether the recent growth was structural or a one-off catch-up, and reporting the range is more useful to a destination manager than reporting one number.

## 5.5 Limitations

The study covers one destination and ten complete years, which limits the power of trend tests on annual indicators such as the Gini coefficient and makes the logistic carrying capacity unidentifiable. The 2026 data cover nine months and may be revised as late registrations are entered. The analysis uses no explanatory variables, so it describes and extrapolates rather than explains; monthly data on accommodation capacity, prices, Krka National Park visitor numbers and national arrivals would allow a causal design. Arrivals and overnight stays do not measure expenditure, and a transit visitor who spends one night may spend as much as a longer-staying visitor in a cheaper category.

# 6. Conclusion

Ten years of e-Visitor data show that tourism in Knin grew more than fourfold between 2016 and 2025, that the growth was concentrated in 2022-2025, that it came from a diversified set of Central and South-East European markets travelling in summer, and that it stopped in 2026. Seasonality did not decrease; the summer peak flattened into a longer summer while the winter share fell. Average length of stay fell to two nights, so the growth made Knin a busier transit stop rather than a destination. Validated forecasting models disagree about the future because the series is at a turning point: a plateau at about 6,000 arrivals and 12,000-16,000 overnight stays if the 2026 stall persists, about 8,000 and 17,600 on the combined path, and about 12,000 and 24,000 if the 2022-2025 growth resumes. For the local tourist board and the county, the results point to length of stay and the shoulder seasons, not to new source markets, as the margins on which the next phase of development will be decided. The data set and code are published with the paper so that the same analysis can be run for other Croatian local tourist boards and so that the projections can be updated when the 2026 season closes.

# Data and code availability

The consolidated data set (monthly arrivals, overnight stays and tourists by country of origin, Knin, January 2016 to September 2026), the Python scripts that build it from the original e-Visitor exports and produce every table and figure in this paper, and the figures themselves are available at https://github.com/vedranu/knin-evisitor-tourism under an open licence (CC BY 4.0 for data, MIT for code). The original e-Visitor exports were provided by the Tourist Board of the City of Knin.

# Acknowledgements

The authors thank the Tourist Board of the City of Knin for providing the e-Visitor exports.

# References

Ağazade, S. (2022). The effect of tourism source market structure on international tourism revenues in Turkey. *Tourism Economics, 28*(3), 714-727. https://doi.org/10.1177/13548166211055985

Ağazade, S., Tükenmez, E. G., & Uzun, M. (2023). Is the volatility of international tourism revenues affected by tourism source market structure? An empirical analysis of Turkey. *Tourism Economics, 29*(2), 291-304. https://doi.org/10.1177/13548166211046070

Apergis, N., Mervar, A., & Payne, J. E. (2017). Forecasting disaggregated tourist arrivals in Croatia. *Tourism Economics, 23*(1), 78-98. https://doi.org/10.5367/te.2015.0499

Athanasopoulos, G., Hyndman, R. J., Song, H., & Wu, D. C. (2011). The tourism forecasting competition. *International Journal of Forecasting, 27*(3), 822-844. https://doi.org/10.1016/j.ijforecast.2010.04.009

Bai, J., & Perron, P. (1998). Estimating and testing linear models with multiple structural changes. *Econometrica, 66*(1), 47-78. https://doi.org/10.2307/2998540

Bai, J., & Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics, 18*(1), 1-22. https://doi.org/10.1002/jae.659

Box, G. E. P., & Jenkins, G. M. (1970). *Time series analysis: Forecasting and control*. Holden-Day.

Butler, R. W. (1980). The concept of a tourist area cycle of evolution: Implications for management of resources. *Canadian Geographer, 24*(1), 5-12. https://doi.org/10.1111/j.1541-0064.1980.tb00970.x

Butler, R. W. (1994). Seasonality in tourism: Issues and problems. In A. V. Seaton (Ed.), *Tourism: The state of the art* (pp. 332-339). Wiley.

Butler, R. W. (2001). Seasonality in tourism: Issues and implications. In T. Baum & S. Lundtorp (Eds.), *Seasonality in tourism* (pp. 5-21). Pergamon. https://doi.org/10.1016/B978-0-08-043674-6.50005-2

Chow, G. C. (1960). Tests of equality between sets of coefficients in two linear regressions. *Econometrica, 28*(3), 591-605. https://doi.org/10.2307/1910133

Cisneros-Martínez, J. D., & Fernández-Morales, A. (2015). Cultural tourism as tourist segment for reducing seasonality in a coastal area: The case study of Andalusia. *Current Issues in Tourism, 18*(8), 765-784. https://doi.org/10.1080/13683500.2013.861810

Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. (1990). STL: A seasonal-trend decomposition procedure based on loess. *Journal of Official Statistics, 6*(1), 3-73.

Čorak, S., Boranić Živoder, S., & Marušić, Z. (2020). Opportunities for tourism recovery and development during and after COVID-19. *Tourism, 68*(4), 434-449. https://doi.org/10.37741/t.68.4.5

Duro, J. A. (2016). Seasonality of hotel demand in the main Spanish provinces: Measurements and decomposition exercises. *Tourism Management, 52*, 52-63. https://doi.org/10.1016/j.tourman.2015.06.013

Duro, J. A., & Turrión-Prats, J. (2019). Tourism seasonality worldwide. *Tourism Management Perspectives, 31*, 38-53. https://doi.org/10.1016/j.tmp.2019.03.010

Fernández-Morales, A. (2003). Decomposing seasonal concentration. *Annals of Tourism Research, 30*(4), 942-956. https://doi.org/10.1016/S0160-7383(03)00090-2

Fernández-Morales, A., Cisneros-Martínez, J. D., & McCabe, S. (2016). Seasonal concentration of tourism demand: Decomposition analysis and marketing implications. *Tourism Management, 56*, 172-190. https://doi.org/10.1016/j.tourman.2016.04.004

Fotiadis, A., Polyzos, S., & Huan, T.-C. T. C. (2021). The good, the bad and the ugly on COVID-19 tourism recovery. *Annals of Tourism Research, 87*, 103117. https://doi.org/10.1016/j.annals.2020.103117

Franjić, M., Jagodič, G., Božinovski, B., & Jurakić, M. (2026). Currency conversion effects: Insights into tourist attitudes towards Croatia's entrance to the euro area. *Turyzm/Tourism, 36*(1), 19-33. https://doi.org/10.18778/0867-5856.2026.02

Gil-Pareja, S., Llorca-Vivero, R., & Martínez-Serrano, J. A. (2007). The effect of EMU on tourism. *Review of International Economics, 15*(2), 302-312. https://doi.org/10.1111/j.1467-9396.2006.00620.x

Gössling, S., Scott, D., & Hall, C. M. (2021). Pandemics, tourism and global change: A rapid assessment of COVID-19. *Journal of Sustainable Tourism, 29*(1), 1-20. https://doi.org/10.1080/09669582.2020.1758708

Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/

Hyndman, R. J., & Khandakar, Y. (2008). Automatic time series forecasting: The forecast package for R. *Journal of Statistical Software, 27*(3), 1-22. https://doi.org/10.18637/jss.v027.i03

Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting, 22*(4), 679-688. https://doi.org/10.1016/j.ijforecast.2006.03.001

Hyndman, R. J., Koehler, A. B., Snyder, R. D., & Grose, S. (2002). A state space framework for automatic forecasting using exponential smoothing methods. *International Journal of Forecasting, 18*(3), 439-454. https://doi.org/10.1016/S0169-2070(01)00110-8

Institut za turizam. (2019). *Studija održivosti razvoja turizma i prihvatnog kapaciteta s akcijskim planom Šibensko-kninske županije*. Institut za turizam. https://repozitorij.iztzg.hr/islandora/object/iztzg:48

Koenig-Lewis, N., & Bischoff, E. E. (2005). Seasonality research: The state of the art. *International Journal of Tourism Research, 7*(4-5), 201-219. https://doi.org/10.1002/jtr.531

Koens, K., Postma, A., & Papp, B. (2018). Is overtourism overused? Understanding the impact of tourism in a city context. *Sustainability, 10*(12), 4384. https://doi.org/10.3390/su10124384

Kožić, I., Krešić, D., & Boranić-Živoder, S. (2013). Analiza sezonalnosti turizma u Hrvatskoj primjenom metode Gini koeficijenta. *Ekonomski pregled, 64*(2), 159-181.

Kranjčević, J., & Hajdinjak, S. (2019). Tourism urbanization in Croatia: The cases of Poreč in Istria and Makarska in Dalmatia. *Südosteuropa, 67*(3), 393-420. https://doi.org/10.1515/soeu-2019-0028

Kulendran, N., & Wong, K. K. F. (2005). Modeling seasonality in tourism forecasting. *Journal of Travel Research, 44*(2), 163-170. https://doi.org/10.1177/0047287505276605

Lew, A., & McKercher, B. (2006). Modeling tourist movements: A local destination analysis. *Annals of Tourism Research, 33*(2), 403-423. https://doi.org/10.1016/j.annals.2005.12.002

Lue, C.-C., Crompton, J. L., & Fesenmaier, D. R. (1993). Conceptualization of multi-destination pleasure trips. *Annals of Tourism Research, 20*(2), 289-301. https://doi.org/10.1016/0160-7383(93)90056-9

Lundtorp, S. (2001). Measuring tourism seasonality. In T. Baum & S. Lundtorp (Eds.), *Seasonality in tourism* (pp. 23-50). Pergamon. https://doi.org/10.1016/B978-0-08-043674-6.50006-4

Lundtorp, S., & Wanhill, S. (2001). The resort lifecycle theory: Generating processes and estimation. *Annals of Tourism Research, 28*(4), 947-964. https://doi.org/10.1016/S0160-7383(00)00080-3

Mak, K., & Kovač, C. (2021). The impact of crisis on the seasonality of Croatian tourism after 2000. *Challenges of Tourism and Business Logistics in the 21st Century, 4*(1), 362-368. https://doi.org/10.46763/YFNTS2141362m

Marušić, Z., Kožul, M., & Brozović, I. (2020). Measuring non-commercial tourism traffic in Croatia: Challenges of using administrative data. *Croatian Review of Economic, Business and Social Statistics, 6*(2), 69-81. https://doi.org/10.2478/crebss-2020-0012

Mervar, A., & Payne, J. E. (2007). Analysis of foreign tourism demand for Croatian destinations: Long-run elasticity estimates. *Tourism Economics, 13*(3), 407-420. https://doi.org/10.5367/000000007781497764

Opačić, V. T., Klarić, Z., Beroš, I., & Boranić Živoder, S. (2022). Tourism Development Index of local self-government units: The example of Croatia. *Acta geographica Slovenica, 62*(1), 77-87. https://doi.org/10.3986/ags.9814

Payne, J. E., Gil-Alana, L. A., & Mervar, A. (2022). Persistence in Croatian tourism: The impact of COVID-19. *Tourism Economics, 28*(6), 1676-1682. https://doi.org/10.1177/1354816621999969

Payne, J. E., Gil-Alana, L. A., Mervar, A., & Goenechea, M. (2023). Tourist arrivals and overnight stays along the Croatian Adriatic Coast: Changes in persistence and seasonality from the COVID-19 disruption. *Tourism Economics, 29*(6), 1679-1693. https://doi.org/10.1177/13548166221110528

Payne, J. E., Nazlioglu, S., & Mervar, A. (2023). Regional tourism convergence: A disaggregated analysis of Croatia. *Applied Economics, 55*(52), 6149-6169. https://doi.org/10.1080/00036846.2022.2141460

Radeljak Kaufmann, P. (2020). Rural tourism in the surroundings of Krka National Park: Factors of development and spatial impacts. In M. Koderman & V. T. Opačić (Eds.), *Challenges of tourism development in protected areas of Croatia and Slovenia* (pp. 53-73). University of Primorska Press; Croatian Geographical Society. https://doi.org/10.26493/978-961-7055-08-5.53-73

Santana-Gallego, M., Ledesma-Rodríguez, F. J., & Pérez-Rodríguez, J. V. (2010). Exchange rate regimes and tourism. *Tourism Economics, 16*(1), 25-43. https://doi.org/10.5367/000000010790872015

Škare, M., Soriano, D. R., & Porada-Rochoń, M. (2021). Impact of COVID-19 on the travel and tourism industry. *Technological Forecasting and Social Change, 163*, 120469. https://doi.org/10.1016/j.techfore.2020.120469

Song, H., & Li, G. (2008). Tourism demand modelling and forecasting - A review of recent research. *Tourism Management, 29*(2), 203-220. https://doi.org/10.1016/j.tourman.2007.07.016

Song, H., Qiu, R. T. R., & Park, J. (2019). A review of research on tourism demand forecasting. *Annals of Tourism Research, 75*, 338-362. https://doi.org/10.1016/j.annals.2018.12.001

Tkalec, M. (2024). The effect of EU membership on tourism in Croatia. *European Journal of Tourism Research, 37*, 3708. https://doi.org/10.54055/ejtr.v37i.3342

Tomljenović, R., & Kunst, I. (2014). From sun and sea tourism to cultural tourism - the case of Split-Dalmatia county. *European Journal of Tourism Research, 8*, 83-98. https://doi.org/10.54055/ejtr.v8i.152

Winters, P. R. (1960). Forecasting sales by exponentially weighted moving averages. *Management Science, 6*(3), 324-342. https://doi.org/10.1287/mnsc.6.3.324

Wu, D. C., Song, H., & Shen, S. (2017). New developments in tourism and hotel demand modeling and forecasting. *International Journal of Contemporary Hospitality Management, 29*(1), 507-529. https://doi.org/10.1108/IJCHM-05-2015-0249

Zhang, H., Song, H., Wen, L., & Liu, C. (2021). Forecasting tourism recovery amid COVID-19. *Annals of Tourism Research, 87*, 103149. https://doi.org/10.1016/j.annals.2021.103149
