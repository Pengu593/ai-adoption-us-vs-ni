# AI adoption: the United States vs Northern Ireland

Analysis code for my university research paper comparing business AI adoption in the United States and Northern Ireland, and what Northern Ireland's small and medium-sized businesses could learn from it (Queen's University Belfast, Study USA programme, June 2026).

## What's in it

The paper triangulates the adoption gap from several public sources, then tests two structural questions with the data.

| Script | What it does | Data |
|---|---|---|
| `chart1_adoption_gap.py` | Compares business AI adoption rates across the US, Nordic countries, the OECD, Northern Ireland and the UK | Published figures (Stanford AI Index, OECD, DSIT, AICC/Invest NI) |
| `chart2_investment_gap.py` | Private AI investment in 2024: US vs China vs UK | Stanford AI Index 2025 |
| `chart3_sme_gap.py` | The gap between large and small firms, across three independent datasets | OECD, DSIT, US Census Bureau |
| `chart4_scatter.py` | **Regression:** AI adoption against labour productivity for 23 European economies | Eurostat 2024, OECD 2023 (`data/country_data.csv`) |
| `chart5_kmeans.py` | K-means clustering on adoption and productivity (exploratory; later abandoned, see below) | `data/country_data.csv` |
| `chart5_pca_kmeans.py` | **Principal component analysis** of national AI readiness, 195 countries | Oxford Insights Government AI Readiness Index 2025 |
| `chart6_pillar_gap.py` | Breaks the US–UK readiness gap down by pillar | Oxford Insights 2025 |
| `robustness_check.py` | Re-runs the PCA on the 2023, 2024 and 2025 indices to check the result isn't an artefact of one year's method | Oxford Insights 2023–2025 |

## Main findings

- **Adoption and productivity move together.** Across 23 European economies, AI adoption is positively associated with GDP per hour worked (r = 0.61, R² = 0.37, p = 0.002). Excluding three economies whose GDP is distorted by multinationals, finance or oil (Ireland, Luxembourg, Norway) strengthens it to r = 0.77. This is an association, not proof of cause.
- **AI readiness is one continuum, not separate tiers.** In the Oxford Insights index, the first principal component explains **82.6%** of the variation across six pillars, so countries that are strong on one pillar tend to be strong on all of them. The same pattern holds in 2024 (89.0%) and 2023 (89.9%), despite a change in the index's method.
- **I set out to find clusters, and the data didn't support them.** K-means with the silhouette score favoured two groups, but the "leader" group held 81 countries, too broad to mean anything. I reported the continuum rather than forcing tiers the data didn't show.
- **The US–UK gap is about implementation, not governance.** The US leads on public sector adoption, diffusion and infrastructure; the UK scores higher on governance, policy capacity and resilience.

Northern Ireland has no separate score in most international datasets (the index folds it into the United Kingdom), so it appears on the charts only as a clearly marked indicative point.

## Running it

```bash
pip install -r requirements.txt
python scripts/chart4_scatter.py
```

Charts are written to `figures/`. The Oxford Insights scripts (`chart5_pca_kmeans.py`, `chart6_pillar_gap.py`, `robustness_check.py`) need the index spreadsheets, which aren't included here. See [`data/README.md`](data/README.md) for where to download them.

## How it was built

Python 3.12 with pandas, NumPy, scikit-learn (`StandardScaler`, `PCA`, `KMeans`), SciPy and matplotlib. I wrote the analysis with the help of an AI coding assistant, and chose the methods, checked the results and made the analytical calls (such as dropping the clustering in favour of the continuum) myself.

## Licence

Code: MIT (see `LICENSE`). Data belongs to its original publishers; see `data/README.md` for sources.
