"""
Robustness check: run PCA independently on Oxford Insights GARI 2023, 2024, 2025.
2023/2024 use 3 pillars; 2025 uses 6 pillars (methodology changed). If the structure
(one dominant 'readiness' dimension; US at top; UK high) replicates across all three
years AND across the methodology break, the finding is robust, not an artefact.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import pandas as pd, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

base = DATA

def analyse(path, sheet, header, pillars, label):
    df = pd.read_excel(base / path, sheet_name=sheet, header=header)
    df = df.loc[:, ~df.columns.duplicated()]
    df = df[['Country'] + pillars].copy()
    for c in pillars:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.dropna(subset=pillars).reset_index(drop=True)
    X = StandardScaler().fit_transform(df[pillars].values)
    pca = PCA().fit(X)
    pc1 = pca.transform(X)[:, 0]
    # Orient PC1 so higher = more ready (align with mean pillar score)
    if np.corrcoef(pc1, df[pillars].mean(axis=1))[0, 1] < 0:
        pc1 = -pc1
    df['PC1'] = pc1
    df['pctile'] = df['PC1'].rank(pct=True) * 100
    n = len(df)
    print(f"\n=== {label} ({n} countries, {len(pillars)} pillars) ===")
    print(f"PC1 explained variance: {pca.explained_variance_ratio_[0]:.1%}")
    for needle in ['United States', 'United Kingdom', 'Ireland', 'China', 'Singapore']:
        row = df[df['Country'].astype(str).str.contains(needle, case=False, na=False)]
        if len(row):
            row = row.sort_values('PC1', ascending=False).iloc[0]
            rank = (df['PC1'] > row['PC1']).sum() + 1
            print(f"  {needle:16} PC1 rank {rank:>3}/{n}  ({row['pctile']:.0f}th pctile)")

# 2025: 6 pillars
analyse('2025-Government-AI-Readiness-Index-data-1.xlsx', 'Dimensions-Pillars', 1,
        ['Policy Capacity','AI Infrastructure','Governance','Public Sector Adoption',
         'Development & Diffusion','Resilience'], '2025')
# 2024: 3 pillars
analyse('2024-GAIRI-data.xlsx', 'Scores per pillar and dimension', 1,
        ['Government','Technology Sector','Data and Infrastructure'], '2024')
# 2023: 3 pillars
analyse('2023-Government-AI-Readiness-Index-Public-Indicator-Data.xlsx', 'Pillar & dimension scores', 1,
        ['Government','Technology Sector','Data and Infrastructure'], '2023')
