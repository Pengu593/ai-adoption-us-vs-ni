"""
Chart 5: K-means clustering of European economies by AI adoption + productivity,
with US and Northern Ireland positioned against the resulting clusters.

Method:
- Features: AI adoption (Eurostat 2024) + productivity (OECD 2023), standardised (z-scores).
- KMeans (k=3) fitted ONLY on the 23 European economies with consistent-methodology data.
- US and NI then assigned to their nearest cluster centroid (transformed with the same scaler),
  shown as focal subjects. Their adoption figures use different surveys (caveated); productivity
  (the more comparable axis) drives a robust assignment regardless.

INTEGRITY NOTES:
- k=3 chosen for interpretability (leaders / middle / lagging); this is a descriptive grouping,
  NOT a causal claim. Clusters describe where economies sit, they do not explain why.
- US/NI assignment is indicative given measurement differences, but robust: US lands with leaders
  on productivity alone; NI lands with the lagging group on both axes.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv(DATA / 'country_data.csv', comment='#').dropna().reset_index(drop=True)

X = df[['ai_adoption_2024', 'productivity_2023']].values
scaler = StandardScaler().fit(X)
Xs = scaler.transform(X)

km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Xs)
df['cluster'] = km.labels_

# Label clusters by mean productivity (high=leaders, low=lagging)
order = df.groupby('cluster')['productivity_2023'].mean().sort_values(ascending=False).index.tolist()
names = {order[0]: 'Leaders', order[1]: 'Middle', order[2]: 'Lagging'}
colors = {order[0]: '#1a5276', order[1]: '#5dade2', order[2]: '#e67e22'}

fig, ax = plt.subplots(figsize=(11, 7.5))

for cl in df['cluster'].unique():
    sub = df[df['cluster'] == cl]
    ax.scatter(sub['ai_adoption_2024'], sub['productivity_2023'],
               s=80, color=colors[cl], edgecolor='white', zorder=3,
               label=f'{names[cl]} cluster')
    for _, row in sub.iterrows():
        ax.annotate(row['country'], (row['ai_adoption_2024'], row['productivity_2023']),
                    fontsize=7, color='grey', xytext=(4, 3), textcoords='offset points')

# Assign US and NI to nearest centroid
subjects = {'UNITED STATES': (78, 97.05, '#0b3a5c'), 'NORTHERN IRELAND': (30, 62, '#b9540a')}
for name, (adopt, prod, col) in subjects.items():
    z = scaler.transform([[adopt, prod]])
    nearest = km.predict(z)[0]
    ax.scatter([adopt], [prod], marker='*', s=560, color=col, edgecolor='white',
               linewidth=1.3, zorder=6)
    ax.annotate(f'{name}\n(nearest: {names[nearest]})', (adopt, prod),
                fontsize=9, fontweight='bold', color=col,
                xytext=(0, -42), textcoords='offset points', ha='center')

ax.set_xlabel('Enterprise AI Adoption (% of enterprises, 2024)', fontsize=11, labelpad=10)
ax.set_ylabel('Labour Productivity (GDP per hour worked, USD PPP, 2023)', fontsize=11, labelpad=10)
ax.set_title('AI Readiness Clusters: Which Group Do the US and Northern Ireland Belong To?',
             fontsize=13, fontweight='bold', pad=15)
ax.legend(fontsize=9, frameon=False, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.15)

fig.text(0.10, 0.005,
         'K-means (k=3) fitted on 23 European economies (Eurostat 2024 adoption + OECD 2023 productivity, standardised). '
         'US and NI assigned to nearest cluster centroid as focal subjects — indicative given differing adoption surveys, '
         'but robust (US groups with Leaders, NI with Lagging). Clusters are descriptive, not causal.',
         fontsize=7, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(FIG / 'chart5_kmeans.png', dpi=200, bbox_inches='tight')
plt.close()

# Print cluster membership for the record
for cl in order:
    members = df[df['cluster'] == cl]['country'].tolist()
    print(f"{names[cl]}: {', '.join(members)}")
