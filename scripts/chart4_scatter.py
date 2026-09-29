"""
Chart 4: AI Adoption vs Labour Productivity across European economies,
with US and Northern Ireland positioned as the focal subjects.

Data sources:
- European AI adoption: Eurostat isoc_eb_ai, E_AI_TANY, PC_ENT, 10+ employees, 2024
- Productivity (GDP per hour worked, USD PPP, 2023): OECD
- US adoption 78%: Stanford HAI AI Index 2025 (BROAD survey measure — see caveat)
- US productivity $97.05: OECD 2023
- NI adoption 30%: AICC/Invest NI 2024 (SME using/exploring — softer measure, see caveat)
- NI productivity ~$62: INDICATIVE estimate (NI is lowest output/hour in UK; UK=$78.05 OECD 2023, NI ~80% of UK)

INTEGRITY NOTES:
- Trend line is fitted ONLY on the 23 European countries (consistent Eurostat/OECD methodology).
- Full sample reported as headline (r=0.61). Robustness excluding structural outliers
  (Ireland, Luxembourg, Norway — GDP distorted by multinationals/finance/oil): r=0.77.
- US and NI use DIFFERENT adoption surveys and are NOT directly comparable on the x-axis.
  They are shown as clearly-marked indicative reference points, not as fitted data.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv(DATA / 'country_data.csv', comment='#').dropna()

outliers = ['Ireland', 'Luxembourg', 'Norway']
df['is_outlier'] = df['country'].isin(outliers)

x = df['ai_adoption_2024']
y = df['productivity_2023']

# Full-sample OLS (headline)
slope, intercept, r, p, se = stats.linregress(x, y)

fig, ax = plt.subplots(figsize=(11, 7.5))

# European points — non-outliers
core = df[~df['is_outlier']]
ax.scatter(core['ai_adoption_2024'], core['productivity_2023'],
           s=70, color='#5dade2', edgecolor='white', zorder=3, label='European economies')
# European points — structural outliers, marked distinctly
out = df[df['is_outlier']]
ax.scatter(out['ai_adoption_2024'], out['productivity_2023'],
           s=70, facecolor='none', edgecolor='#5dade2', linewidth=1.8,
           zorder=3, label='Structural outliers (IE, LU, NO)')

# Label European countries lightly
for _, row in df.iterrows():
    ax.annotate(row['country'], (row['ai_adoption_2024'], row['productivity_2023']),
                fontsize=7, color='grey', xytext=(4, 3), textcoords='offset points')

# Full-sample trend line
xs = np.linspace(x.min(), x.max(), 100)
ax.plot(xs, slope * xs + intercept, color='#34495e', linestyle='--', linewidth=1.6,
        zorder=2, label=f'European trend (full sample): r = {r:.2f}')

# --- FOCAL SUBJECTS: US and NI (indicative, different methodology) ---
ax.scatter([78], [97.05], marker='*', s=520, color='#1a5276',
           edgecolor='white', linewidth=1.2, zorder=5)
ax.annotate('UNITED STATES\n(78% adoption — broad survey;\nnot Eurostat-comparable)',
            (78, 97.05), fontsize=9, fontweight='bold', color='#1a5276',
            xytext=(-30, -48), textcoords='offset points', ha='center')

ax.scatter([30], [62], marker='*', s=520, color='#e67e22',
           edgecolor='white', linewidth=1.2, zorder=5)
ax.annotate('NORTHERN IRELAND\n(30% SME using/exploring;\nproductivity indicative ~80% of UK)',
            (30, 62), fontsize=9, fontweight='bold', color='#b9540a',
            xytext=(60, -10), textcoords='offset points', ha='center')

ax.set_xlabel('Enterprise AI Adoption (% of enterprises, 2024)', fontsize=11, labelpad=10)
ax.set_ylabel('Labour Productivity (GDP per hour worked, USD PPP, 2023)', fontsize=11, labelpad=10)
ax.set_title('AI Adoption and Productivity: Where the US and Northern Ireland Sit',
             fontsize=13.5, fontweight='bold', pad=15)
ax.legend(fontsize=9, frameon=False, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.15)

fig.text(0.10, 0.005,
         'Trend line fitted on 23 European economies only (consistent Eurostat 2024 + OECD 2023 methodology); full-sample r = {:.2f}, '
         'strengthening to r = 0.77 when structural outliers (Ireland, Luxembourg, Norway) are excluded.\n'
         'US and NI shown as INDICATIVE reference points — their adoption figures come from different surveys (US: Stanford; NI: AICC/Invest NI) '
         'and are not directly comparable on the x-axis. Association does not imply causation.'.format(r),
         fontsize=7, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(FIG / 'chart4_scatter.png', dpi=200, bbox_inches='tight')
plt.close()
print(f"Chart 4 saved. Full-sample r={r:.3f}, R2={r**2:.3f}, p={p:.4f}, slope={slope:.2f}")
