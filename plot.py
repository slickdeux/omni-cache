import matplotlib.pyplot as plt
import numpy as np
import os

labels = ['Zipfian', 'True Scan', 'Mixed Workload']
lru_scores = [83.0, 0.0, 63.2]
arc_scores = [85.0, 0.0, 65.6]
omni_scores = [85.0, 0.0, 65.5]

x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width, lru_scores, width, label='LRU', color='#999999')
rects2 = ax.bar(x, arc_scores, width, label='ARC', color='#E06666')
rects3 = ax.bar(x + width, omni_scores, width, label='OmniCache', color='#6AA84F')

ax.set_ylabel('Hit Rate (%)')
ax.set_title('OmniCache vs ARC vs LRU: Hit Rate by Workload', fontsize=14, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.set_ylim(0, 100)

for rects in [rects1, rects2, rects3]:
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('omnicache_benchmark.png', dpi=300)
