"""
Chart 6: Pillar-level gap decomposition — US vs UK across the 6 AI-readiness pillars
(Oxford Insights GARI 2025). Sorted by gap size to show WHERE the gap is largest,
which tells NI where to focus. NI sits within the UK score, so where the UK lags the US,
NI lags at least as much (NI is the UK's lowest-productivity region).
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

raw = pd.read_excel(DATA / '2025-Government-AI-Readiness-Index-data-1.xlsx',
                    sheet_name='Dimensions-Pillars', header=1)
pillars = ['Policy Capacity', 'AI Infrastructure', 'Governance',
           'Public Sector Adoption', 'Development & Diffusion', 'Resilience']
for c in pillars:
    raw[c] = pd.to_numeric(raw[c], errors='coerce')

us = raw[raw['Country'].str.contains('United States', case=False, na=False)].iloc[0]
uk = raw[raw['Country'].str.contains('United Kingdom', case=False, na=False)].iloc[0]

data = pd.DataFrame({
    'pillar': pillars,
    'US': [us[p] for p in pillars],
    'UK': [uk[p] for p in pillars],
})
data['gap'] = data['US'] - data['UK']
data = data.sort_values('gap', ascending=True).reset_index(drop=True)  # ascending -> largest gap at top in barh

print("Pillar | US | UK | gap (US-UK)")
for _, r in data.sort_values('gap', ascending=False).iterrows():
    print(f"  {r['pillar']:24} {r['US']:5.1f} {r['UK']:5.1f}  {r['gap']:+.1f}")

y = np.arange(len(data))
h = 0.38

fig, ax = plt.subplots(figsize=(11, 7))
b_us = ax.barh(y + h/2, data['US'], height=h, color='#c0392b', edgecolor='white', label='United States')
b_uk = ax.barh(y - h/2, data['UK'], height=h, color='#1a5276', edgecolor='white', label='United Kingdom')

for bars in (b_us, b_uk):
    for bar in bars:
        ax.text(bar.get_width() + 0.6, bar.get_y() + bar.get_height()/2,
                f'{bar.get_width():.0f}', va='center', fontsize=9, color='#2c3e50')

# Gap labels
for i, r in data.iterrows():
    ax.text(max(r['US'], r['UK']) + 6, y[i], f'gap {r["gap"]:+.0f}',
            va='center', fontsize=8.5, fontweight='bold', color='#a85107')

ax.set_yticks(y)
ax.set_yticklabels(data['pillar'], fontsize=10)
ax.set_xlabel('Pillar score (0–100)', fontsize=11, labelpad=8)
ax.set_xlim(0, 112)
ax.set_title('Where the Gap Is Largest: US vs UK Across AI-Readiness Pillars\n'
             '(Oxford Insights GARI 2025 — NI sits within the UK score)',
             fontsize=12.5, fontweight='bold', pad=14)
ax.legend(fontsize=10, frameon=False, loc='lower right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.text(0.10, 0.005,
         'Pillars ordered by US–UK gap. Where the UK trails the US, Northern Ireland trails at least as much '
         '(NI is the UK\'s lowest-productivity region). The largest gaps mark the priority areas for NI policy and investment.',
         fontsize=7.5, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(FIG / 'chart6_pillar_gap.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 6 saved.")
