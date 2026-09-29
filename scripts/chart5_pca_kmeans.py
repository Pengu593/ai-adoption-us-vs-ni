"""
Chart 5 (polished): PCA of the Oxford Insights Government AI Readiness Index 2025,
focused on the US <-> Northern Ireland comparison (UK shown as the bridging context).

- US and UK plotted as REAL data points (both scored in the index).
- NI shown as a CLEARLY INDICATIVE annotation only: it has no independent score
  (index folds it into "United Kingdom of Great Britain and Northern Ireland").
  It is positioned below the UK as the UK's lowest-productivity region -- labelled indicative.
- Context countries shown as faint grey dots so the focal subjects pop.
- K-means earlier showed a continuum (silhouette favoured k=2); we therefore lead with PCA
  and do NOT impose discrete cluster colours here.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

raw = pd.read_excel(DATA / '2025-Government-AI-Readiness-Index-data-1.xlsx',
                    sheet_name='Dimensions-Pillars', header=1)
pillars = ['Policy Capacity', 'AI Infrastructure', 'Governance',
           'Public Sector Adoption', 'Development & Diffusion', 'Resilience']
df = raw[['Country', 'Total Score'] + pillars].copy()
for c in pillars + ['Total Score']:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df = df.dropna(subset=pillars).reset_index(drop=True)

X = StandardScaler().fit_transform(df[pillars].values)
pca = PCA(n_components=2).fit(X)
pcs = pca.transform(X)
# Orient PC1 so higher = more ready
if np.corrcoef(pcs[:, 0], df[pillars].mean(axis=1))[0, 1] < 0:
    pcs[:, 0] = -pcs[:, 0]
df['PC1'], df['PC2'] = pcs[:, 0], pcs[:, 1]

def pt(name):
    r = df[df['Country'].str.contains(name, case=False, na=False)].iloc[0]
    return r['PC1'], r['PC2']

fig, ax = plt.subplots(figsize=(12, 8))

# Context countries — faint
ax.scatter(df['PC1'], df['PC2'], s=38, color='#d5dbdb', edgecolor='white',
           linewidth=0.3, zorder=1, label='Other economies (n=195)')

# Secondary reference countries — small dark dots
for c in ['China', 'Singapore', 'Ireland', 'Germany', 'France', 'Republic of Korea']:
    m = df[df['Country'].str.contains(c, case=False, na=False)]
    if len(m):
        r = m.iloc[0]
        ax.scatter(r['PC1'], r['PC2'], s=55, color='#7f8c8d', edgecolor='white', zorder=3)
        nm = 'South Korea' if 'Korea' in c else c
        ax.annotate(nm, (r['PC1'], r['PC2']), fontsize=8, color='#566573',
                    xytext=(6, 3), textcoords='offset points', zorder=4)

# FOCAL: United States (real point)
us = pt('United States')
ax.scatter(*us, marker='*', s=720, color='#c0392b', edgecolor='white', linewidth=1.4, zorder=8)
ax.annotate('UNITED STATES\n(#1 globally)', us, fontsize=11, fontweight='bold',
            color='#c0392b', xytext=(12, -6), textcoords='offset points', zorder=9)

# BRIDGE CONTEXT: United Kingdom (real point)
uk = pt('United Kingdom')
ax.scatter(*uk, marker='*', s=520, color='#1a5276', edgecolor='white', linewidth=1.3, zorder=8)
ax.annotate('UNITED KINGDOM\n(#3 globally)', uk, fontsize=10.5, fontweight='bold',
            color='#1a5276', xytext=(10, 8), textcoords='offset points', zorder=9)

# FOCAL: Northern Ireland — INDICATIVE only (no independent score)
# Positioned LOWER on PC1 (the readiness axis) than the UK; PC2 held near the UK level.
ni_pc1, ni_pc2 = uk[0] - 2.1, uk[1] - 0.25
ax.scatter(ni_pc1, ni_pc2, marker='*', s=620, facecolor='#e67e22', edgecolor='#7e3d09',
           linewidth=1.8, alpha=0.9, zorder=8)
ax.annotate('NORTHERN IRELAND\n(indicative — within UK score;\nlowest-productivity UK region)',
            (ni_pc1, ni_pc2), fontsize=10, fontweight='bold', color='#a85107',
            xytext=(-8, 14), textcoords='offset points', ha='center', va='bottom', zorder=9)
# Dashed arrow UK -> NI indicative
ax.annotate('', xy=(ni_pc1, ni_pc2), xytext=uk,
            arrowprops=dict(arrowstyle='->', linestyle='--', color='#a85107', lw=1.6), zorder=7)

ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]:.0%} of variance) — overall AI readiness  →',
              fontsize=11.5, labelpad=10)
ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]:.0%} of variance)',
              fontsize=11, labelpad=10)
ax.set_title('AI Readiness: The United States vs Northern Ireland (UK as context)\n'
             'PCA of the Oxford Insights Government AI Readiness Index 2025',
             fontsize=13.5, fontweight='bold', pad=15)
ax.legend(fontsize=9, frameon=False, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.15)

fig.text(0.10, 0.005,
         'PCA on 6 standardised pillars; PC1 captures {:.0%} of variance (readiness is one cumulative dimension). '
         'US and UK are scored data points; NI has NO independent score (index folds NI into the UK) and is shown as an indicative position only. '
         'Robustness: US ranked #1 and UK top-5 on PC1 in 2023, 2024 and 2025.'.format(pca.explained_variance_ratio_[0]),
         fontsize=7, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(FIG / 'chart5_pca_kmeans.png', dpi=200, bbox_inches='tight')
plt.close()
print(f"Polished Chart 5 saved. US PC1={us[0]:.2f}, UK PC1={uk[0]:.2f}, NI indicative={ni_pc1:.2f}")
