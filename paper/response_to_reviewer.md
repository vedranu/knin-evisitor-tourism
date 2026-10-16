# Odgovor na primjedbe (interna recenzija, 16. 10. 2026.)

Verzija: paper/Knin_THM_submission.docx (THM), izgrađena iz paper/paper_thm.md; nove analize u scripts/05_revision.py, rezultati u outputs/revision.json.

## Veće primjedbe

1. **Istraživačka pitanja/hipoteze.** Dodana četiri istraživačka pitanja (RQ1 - RQ4) s pripadajućim očekivanjima (H1 - H4) na kraju Uvoda; Zaključak sada odgovara na svako pitanje i izričito navodi je li hipoteza podržana (H1 djelomično, H2 odbačena, H3 odbačena, H4 podržana).

2. **Bai-Perron "break in mean" na trendirajućoj seriji.** Analiza je zamijenjena: (a) segmentirana log-linearna regresija s lomovima u odsječku i nagibu (ruptures, model "linear", min. segment 18 mj., BIC); (b) lomovi u stopi rasta (diferencirana desezonirana serija); (c) supF test za jedan lom s bootstrap p-vrijednošću (sieve bootstrap, AR(2), 499 replikacija); (d) bootstrap 90 % intervali pouzdanosti za datume lomova (299 replikacija). Rezultati: BIC bira 3 loma (2018-05, 2020-04, 2024-08) s nagibima -18 %, +9 %, +54 %, +9 % godišnje, ali su intervali pouzdanosti široki (treći lom: 2022-02 do 2025-04); supF je najveći u travnju 2020. (F = 29,2, bootstrap p = 0,054); **u stopi rasta BIC ne podržava nijedan lom**. Tekst odjeljka 3.4, sažetak i rasprava preformulirani su: govori se o "epizodi ubrzanja", ne o datiranoj promjeni režima; tvrdnja "lom 2022-2023, ne 2020" je povučena. Chowovi testovi ostaju samo kao usporedba i izričito se ne koriste za zaključivanje.

3. **Interval za godišnji zbroj.** Zamijenjen simulacijom 1.000 putanja iz SARIMA modela (kvantili godišnjih suma, 10. i 90. percentil). 2030.: dolasci 3.878 - 48.912 (medijan 13.452), noćenja 13.004 - 51.945. Interval je asimetričan (log skala), što je u tekstu objašnjeno; donja granica ispod razine 2025. pa je i pad do 2030. unutar 80 % raspona. Slika 5 (bivša 6) ima novu os y koja obuhvaća cijeli pojas; logistička krivulja izbačena iz slike.

4. **Validacija.** Dodana rolling-origin evaluacija (45 ishodišta, siječanj 2022. - rujan 2025., horizonti 1 - 12) za dolaske, Tablica 5. Nalaz: sezonski naivni model ima najniži MASE (2,54) i MAPE (32,4 %); modeli ga tuku samo na horizontima 5 - 8; kombinacija je najbolja među modelima. Rečeno je otvoreno da nijedan univarijatni model ne izvlači puno više od prošlogodišnjeg sezonskog obrasca u razdoblju brzog rasta.

5. **Logistička krivulja.** Izbačena iz slika i tablica; jedna rečenica u ograničenjima (SE kapaciteta veća od procjene, stoga se ne iskazuje).

6. **Schengen/euro i usporedba s DZS-om.** Napravljeno. DZS tablica BS_TU12 (županije, mjesečno, komercijalni smještaj) dohvaćena preko PxWeb API-ja 16. 10. 2026. (upit u data/external/dzs_tu12_query.json, podaci u data/external/dzs_tu12.csv, skripta scripts/06_dzs_comparison.py). Nalaz (3.4, Slika 4): dolasci 2019. - 2025.: ŠKŽ -4,3 %, RH +5,8 %, Knin +208 %; 2022. - 2025.: +9,1 %, +16,5 %, +147 %; udio Knina u dolascima županije 0,20 % → 0,64 %; log omjer Knin/ŠKŽ raste 3,5 %/god. 2016. - 2019. (p = 0,48) i 28,7 %/god. 2021. - 2025. (p = 0,008); siječanj - kolovoz 2026. sve tri serije stagniraju. Zaključak u radu: rast je lokalan, ne zrcali nacionalni trend; ali se Schengen i dalje ne može razdvojiti od rasta lokalne ponude. Sažetak i rasprava prilagođeni. Napomena o usporedivosti (DZS = komercijalni smještaj) navedena u 2.1.

7. **Izjava o AI.** Preformulirana: korištenje za čitljivost i jezik te za pomoć pri pisanju i dokumentiranju koda koji je javno objavljen; svi rezultati reproducirani i provjereni od autora; alat nije korišten za generiranje nalaza i zaključaka. Na stranicama THM-a (Code of ethics, Journal policy) nisam našao klauzulu "only to improve readability and language"; jedini tekst o AI je onaj u predlošku (obvezna izjava). Preporuka ostaje: provjeriti s uredništvom prije slanja.

## Manje primjedbe

- Naslov skraćen: "From transit stop to destination? A decade of e-Visitor data on tourism in Knin, Croatia".
- Chord dijagram zamijenjen Tablicom 3 (tržište x sezona, postoci); postoci iz teksta prebačeni u tablicu. Crno-bijeli heatmap ostaje u figures/bw/rev_market_season_heatmap.png kao alternativa.
- Slika 5 (projekcije): različiti markeri i vrste linija za svaki model.
- Tablica 4: RMSE s jedinicama (arrivals/month, nights/month).
- 3.1: naveden KPSS (p = 0,10) i način odabira pomaka (ADF: AIC; KPSS: automatska širina).
- 3.2: dodana napomena o maloj snazi Kendallova tau pri n = 10.
- "90 %" → "90%" u cijelom radu.
- Numeracija: Uvod i Zaključak nenumerirani prema predlošku THM-a (predložak: INTRODUCTION i CONCLUSION bez broja, "1. HEADING 1" dalje).
- Reference: Petrić i sur. (2025) sada s urednicima (Matteucci & Moretti) i stranicama; Milenkovska Klimoska (2021) uklonjena jer DOI nije potvrđen; Opačić & Banda: Scopus navodi 2025., svezak 87(2), DOI 10.21861/HGG.2024.87.02.06 (oznaka DOI-ja s "2024" je izdavačeva, godina ostaje 2025. prema Scopusu). Ružić & Gavrić, Krešić, Pranić & Vuković: DOI, svezak i stranice pročitani izravno sa Scopus stranica dokumenata (16. 10. 2026.).
- Ukupno riječi: 7.703 (limit 8.000); sažetak 172 riječi (bez oznaka odjeljaka).
- APA 7: svi radovi s tri i više autora u tekstu kao "Prvi et al."; Payne 2023 razlikovani kao "Payne, Gil-Alana, et al., 2023" i "Payne, Nazlioglu, et al., 2023".
- Opačić & Banda: Crossref (DOI 10.21861/HGG.2024.87.02.06) navodi issued 2025-12, vol. 87(2), str. 137-167; godina 2025. je ispravna.
- Slika 6 (projekcije): logaritamska os y, pojas simuliranog intervala više ne stišće stupce.

## Napomena

Duga verzija (paper.md / paper_hr.md) zadržava stariju analizu lomova; ako se i ona šalje negdje, treba prenijeti promjene iz točaka 2 - 5.

## Dopuna 16. 10. 2026. (drugi krug)

- Popravljena oštećena rečenica u 1.1 ("..., Tica and Kožić (2015) compared ...").
- Redoslijed slika: Slika 3 (segmentirani trend) sada je odmah iza prvog odlomka 3.4, ispred Slike 4 (usporedba sa ŠKŽ i RH).
- Dodana referenca: Croatian Bureau of Statistics. (2026). *Tourist arrivals and nights ... by county, monthly (Table 1.2, BS_TU12)* [Data set]. PxWeb. Retrieved October 16, 2026, from https://web.dzs.hr/PXWeb/ i citat (Croatian Bureau of Statistics, 2026) u 2.1, 3.4 i izvoru Slike 4.
- Opačić & Banda: ponovno provjereno u Crossrefu za DOI 10.21861/HGG.2024.87.02.06: "issued" 2025-12 (online 2025-12, tisak 2026-02), svezak 87, broj 2, str. 137-167. Godina 2025. je ispravna; "2024" u DOI-ju je oznaka izdavača (HGG DOI-ji nose godinu sveska prema njihovoj internoj shemi), ne godina objave.
- Ukupno riječi: 7.742.
