"""
Chart 3: The SME vs Large-Firm AI Adoption Gap
Shows the consistent pattern across three independent datasets that smaller
firms adopt AI at far lower rates than large firms.

Sources:
- OECD (2025): large firms 52.0%, small firms 17.4%
- UK DSIT (2025): large 36%, medium 23%
- US Census BTOS (2023): 250+ employees 27%, <50 employees ~18% (reported as <20%)
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import matplotlib.pyplot as plt
import numpy as np

# --- DATA (verified against cited sources) ---
datasets = ['OECD\n(2025)', 'UK DSIT\n(2025)', 'US Census\n(2023)']
large_firm = [52.0, 36, 27]
small_firm = [17.4, 23, 18]  # UK 'medium' used as the smaller comparator; US <50 employees

x = np.arange(len(datasets))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, large_firm, width, label='Large firms', color='#1a5276', edgecolor='white')
bars2 = ax.bar(x + width/2, small_firm, width, label='Small / smaller firms', color='#e67e22', edgecolor='white')

for bars in (bars1, bars2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f'{bar.get_height():g}%', ha='center', va='bottom',
                fontsize=10.5, fontweight='bold', color='#2c3e50')

ax.set_ylabel('Percentage of Firms Using AI (%)', fontsize=11, labelpad=10)
ax.set_title('The SME Gap: AI Adoption by Firm Size Across Three Datasets',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(datasets, fontsize=10.5)
ax.set_ylim(0, 60)
ax.legend(fontsize=10, frameon=False, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.text(0.12, 0.01,
         'Sources: OECD AI Adoption by SMEs 2025; UK DSIT Technology Adoption Review 2025; US Census BTOS 2023.\n'
         'Note: definitions of firm size and AI use vary across surveys; UK comparator uses medium-sized firms, US uses firms <50 employees.',
         fontsize=7.5, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig(FIG / 'chart3_sme_gap.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 3 saved.")
