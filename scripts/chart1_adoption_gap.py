"""
Chart 1: AI Adoption Gap — US vs comparators
Sources:
- US 78%: Stanford HAI, AI Index Report 2025
- UK 17%: DSIT, Technology Adoption Review 2025
- OECD average 20.2%: OECD, AI Adoption by SMEs 2025
- Nordic countries 35%+: OECD, AI Adoption by SMEs 2025
- NI SMEs 30%: AICC/QUB/Invest NI, NI AI Economy Report 2024
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- DATA (all figures verified against cited sources) ---
regions = [
    'United States\n(Stanford AI Index 2025)',
    'Nordic Countries\n(OECD 2025)',
    'OECD Average\n(OECD 2025)',
    'Northern Ireland SMEs\n(AICC/Invest NI 2024)',
    'United Kingdom\n(DSIT 2025)'
]
adoption_rates = [78, 35, 20.2, 30, 17]

# Colour: highlight US and NI for contrast
colors = ['#1a5276', '#2e86c1', '#85c1e9', '#e67e22', '#aab7b8']

# --- CHART ---
fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.barh(regions, adoption_rates, color=colors, edgecolor='white', height=0.55)

# Value labels on bars
for bar, val in zip(bars, adoption_rates):
    ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
            f'{val}%', va='center', ha='left', fontsize=11, fontweight='bold', color='#2c3e50')

# Reference line at UK baseline
ax.axvline(x=17, color='#aab7b8', linestyle='--', linewidth=1.2, alpha=0.7)

ax.set_xlabel('Percentage of Organisations Using AI (%)', fontsize=11, labelpad=10)
ax.set_title('The AI Adoption Gap: US, OECD, and Northern Ireland',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlim(0, 90)
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='y', labelsize=9.5)

# Note on measurement methodology
fig.text(0.12, 0.01,
         'Note: US figure (Stanford) measures any AI use; UK figure (DSIT) measures deliberate AI deployment — methodologies differ.\n'
         'Nordic figure represents countries exceeding 35% adoption (Denmark, Finland, Sweden). NI figure includes businesses using or actively exploring AI.',
         fontsize=7.5, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig(FIG / 'chart1_adoption_gap.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 1 saved.")
