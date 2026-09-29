"""
Chart 2: Private AI Investment Gap (2024)
Source: Stanford HAI, AI Index Report 2025
- US private AI investment: $109 billion
- China: $9.3 billion
- UK: $4.5 billion
Key framing: US investment is ~24x the UK and ~12x China.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
FIG = ROOT / 'figures'
import matplotlib.pyplot as plt

# --- DATA (Stanford AI Index 2025, verified) ---
countries = ['United States', 'China', 'United Kingdom']
investment = [109, 9.3, 4.5]  # USD billions, 2024
colors = ['#1a5276', '#a93226', '#aab7b8']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(countries, investment, color=colors, edgecolor='white', width=0.55)

# Value labels
for bar, val in zip(bars, investment):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
            f'${val}B', ha='center', va='bottom', fontsize=13, fontweight='bold', color='#2c3e50')

# Annotate the multiples
ax.annotate('US invests ~24x the UK\nand ~12x China',
            xy=(0, 109), xytext=(0.6, 90),
            fontsize=11, fontweight='bold', color='#1a5276',
            ha='left')

ax.set_ylabel('Private AI Investment, 2024 (USD Billions)', fontsize=11, labelpad=10)
ax.set_title('The Investment Gap: Private AI Investment by Country, 2024',
             fontsize=13, fontweight='bold', pad=15)
ax.set_ylim(0, 125)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=11)

fig.text(0.12, 0.01, 'Source: Stanford HAI, AI Index Report 2025.',
         fontsize=8, color='grey', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(FIG / 'chart2_investment_gap.png', dpi=200, bbox_inches='tight')
plt.close()
print("Chart 2 saved.")
