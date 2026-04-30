# Does Political Violence Trap Economies in Agriculture?

> Using 27 years of panel data (1996–2023) across 46 African countries, we examine whether political violence impedes structural economic transformation — the shift of labor from agriculture to industry and services.

## Overview

This project investigates the economic consequences of political violence, with a focus on Africa. When conflict erupts, investors pull out, supply chains break, and workers get stuck on farms. But how large is this effect, and how long does it persist? We combine conflict event data (ACLED, Africa-focused), employment statistics, GDP figures, and governance indicators to answer these questions through exploratory data analysis and panel regression modelling.

This repository contains cleaning scripts, exploratory analysis, panel regression code, and an interactive HTML report.

The full interactive report is available at [`docs/index.html`](docs/index.html).


## Data Sources

ACLED 
- (Armed Conflict Location & Event Data Project)
- Conflict events & fatalities by country-year
- 1997–2023
- 268,511
World Bank
- Employment in agriculture/ industry/ services (% of total employment)
- 1996–2023
- 6,576
V-Dem (Varieties of Democracy)
- Rule of law index
- 1996–2023
- 4,953

All data are filtered to 46 African countries using the ACLED country list as the authoritative set.

After cleaning and merging — with all datasets filtered to African countries only (using the ACLED country list as the authoritative set) — the analysis dataset contains 1,288 country-year observations from 46 African countries, spanning 1996 to 2023.


## Methodology

### Data Pipeline

1. Cleaning (`code/01_data_cleaning.ipynb`): Standardised country names across all datasets, filtered all World Bank and V-Dem data to African countries only (using the ACLED country list as the authoritative set), handled missing values, and merged into a single Africa-only panel dataset.
2. Exploratory Data Analysis (`code/02_exploration.ipynb`): Produced correlation heatmaps, scatterplot matrices, small-multiples trend charts, and distributional comparisons (high-conflict vs. low-conflict groups).
3. Analysis (`code/03_analysis.ipynb`): Estimated panel regressions with country and year fixed effects, tested for threshold effects (quadratic specification), and examined lagged impacts of conflict on employment shares.

### Analytical Approach

- Panel regression with country and year fixed effects — controls for time-invariant country characteristics (geography, culture, colonial legacy) and global shocks (commodity price cycles, pandemics).
- Three research questions:
  - RQ1 (Direct effect): Does higher conflict intensity increase agricultural employment? — Yes. A one-standard-deviation increase in conflict fatalities is associated with a 2–3 percentage point rise in agricultural employment.
  - RQ2 (Threshold effect): Is there a violence level beyond which structural transformation collapses? — Preliminary evidence says yes. Above ≈60 conflict events, economies appear trapped in agriculture.
  - RQ3 (Lagged effect): Does last year's violence still affect this year's employment? — Yes. The coefficient remains positive and meaningful through lag 2 (0.22), only dropping to near-zero at lag 3 (0.08).
- Principal Component Analysis confirmed that employment sectors, GDP, and governance load on a single "development dimension" (PC1 explains 66.3% of variance).


## Key Findings

1. Conflict directly raises agricultural employment. High-conflict countries average 8–10 percentage points more workers in agriculture than low-conflict countries. The regression scatterplot confirms a positive, statistically significant slope.

2. A violence threshold likely exists. Below ≈60 conflict events, economies can still shift workers into industry and services. Above it, structural transformation stalls — suggesting a tipping point for policy intervention.

3. The effect persists for years. Lagged coefficients show that conflict's impact on employment persists through year 2 after the violence, meaning a single episode can derail transformation for years.

4. Structural economic variables are tightly coupled.
Agriculture vs. services (r = −0.954), agriculture vs. GDP (r = −0.672), and services vs. GDP (r = 0.665) form a coherent "development dimension." Conflict's effects likely operate through non-linear or mediated pathways rather than simple linear correlations (conflict vs. GDP: r = 0.066, n.s.).

5. Governance matters. Countries with stronger rule of law (V-Dem index) tend to have lower conflict, higher GDP, and more diversified economies. However, governance does not change the fundamental economic relationship — it determines where a country sits on the development spectrum.

6. Nigeria and Sudan drive the African conflict trend. The post-2010 surge in violence is almost entirely attributable to these two countries. Without them, the regional trend would be largely flat.


## Limitations

- Observational data, not causal identification. The panel regression with fixed effects controls for many confounders, but unobserved time-varying factors (e.g., drought, commodity shocks) could still bias the estimates. The results should be interpreted as associations rather than causal effects.

- Missing data is non-random. V-Dem governance data has persistent gaps (≈114 missing entries per year from 2009–2023), concentrated in the most conflict-affected countries. This may attenuate the estimated relationship between governance and conflict.

- Ecological fallacy risk. The analysis operates at the country-year level. Within-country variation (urban vs. rural, conflict-affected vs. peaceful regions) is not captured, so the findings should not be interpreted as applying to individuals.

- Conflict measurement is imperfect. ACLED relies on media reporting, which undercounts events in remote or censored areas. The "tip of the iceberg" problem means observed conflict events likely underestimate true violence — and by extension, its economic effects.

- Reverse causality. While the theory predicts conflict → agricultural trap, it is plausible that agrarian, low-income economies are also more prone to conflict. The lagged analysis mitigates this concern but does not eliminate it.

- Sample selection. The merged regression sample excludes country-years with missing data, which disproportionately removes fragile states — precisely those where the conflict–economy link may be strongest.


## Project Structure

```
project_folder/
├── README.md                          ← This file
├── note_on_ai_use.md                  ← AI usage disclosure
├── code/
│   ├── 01_data_cleaning.ipynb         ← Data cleaning & merging
│   ├── 02_exploration.ipynb           ← EDA: correlations, trends, distributions
│   ├── 03_analysis.ipynb              ← Panel regressions & threshold/lag tests
│   └── Z_generate_report.py           ← Report generation script
├── data/
│   ├── acled_data.csv                 ← Raw ACLED conflict events
│   ├── employment_in_agriculture.csv  ← World Bank employment data
│   ├── employment_in_industry.csv
│   ├── employment_in_services.csv
│   ├── gdp_per_capita.csv
│   ├── population_density.csv
│   └── vdem_1996-2023_rule.csv        ← V-Dem rule of law index
├── outputs/
│   ├── cleaned_enhanced_data.csv       ← Merged analysis dataset
│   ├── summary_report.json
│   ├── summary_report.txt
│   ├── cleaned/                       ← Individual cleaned CSVs
│   └── eda/                           ← EDA figure outputs
└── docs/
    ├── index.html                      ← Full interactive report
    └── assets/                         ← Figures (PNG, HTML)
```

## Key Technologies
Built with Python (pandas, numpy, statsmodels, plotly) and Jupyter notebooks.

## Author

Xu Yingnuo


## How to Reproduce

1. Place the raw data files in `data/` (CSV format as listed above).
2. Run the notebooks in order:
   - `code/01_data_cleaning.ipynb` → produces `outputs/cleaned/` and `outputs/cleaned_enhanced_data.csv`
   - `code/02_exploration.ipynb` → produces EDA figures in `outputs/eda/` and `docs/assets/`
   - `code/03_analysis.ipynb` → produces regression outputs and analysis figures in `docs/assets/`
3. Open `docs/index.html` in a browser to view the full report.

---

## License

This project is for academic and educational purposes. Data sources retain their respective licenses:
- ACLED: [Terms of use](https://acleddata.com/terms-of-use/)
- World Bank: [Open Data License](https://data.worldbank.org/summary-terms-of-use)
- V-Dem: [License information](https://www.v-dem.net/data_use_policy/)

Move README to root
