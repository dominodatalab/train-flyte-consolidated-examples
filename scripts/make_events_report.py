import csv
import io
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Read input
value = Path("/mnt/netapp-volumes/quick-start/event_counts.csv").read_text()
reader = csv.DictReader(io.StringIO(value))
rows = [(r["event_type"], int(r["count"])) for r in reader]
event_types = [r[0] for r in rows]
counts = [r[1] for r in rows]
fig, (ax_table, ax_bubble) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Event Report", fontsize=8, y=0.97)
# --- Table ---
ax_table.axis("off")
table_data = [[et, str(c)] for et, c in rows]
table = ax_table.table(
    cellText=table_data,
    colLabels=["Event Type", "Count"],
    cellLoc="center",
    loc="center",
)
table.auto_set_font_size(False)
table.set_fontsize(12)
# table.scale(1, 1.8)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor("#4472C4")
        cell.set_text_props(color="white", fontweight="bold")
    else:
        cell.set_facecolor("#D9E2F3" if row % 2 == 0 else "white")
    cell.set_edgecolor("#B0B0B0")
ax_table.set_title("Event Counts", fontsize=14, pad=12)
# --- Bubble chart ---
np.random.seed(0)
x = np.arange(len(event_types))
y = np.random.uniform(0.3, 0.7, size=len(event_types))
sizes = np.array(counts)
sizes_scaled = (sizes / sizes.max()) * 3000 + 200
colors = plt.cm.Set2(np.linspace(0, 1, len(event_types)))
ax_bubble.scatter(x, y, s=sizes_scaled, c=colors, alpha=0.75, edgecolors="grey", linewidths=1.5)
for i, (et, c) in enumerate(zip(event_types, counts)):
    ax_bubble.annotate(f"{et}\n({c})", (x[i], y[i]), ha="center", va="center", fontsize=3, fontweight="bold")
ax_bubble.set_xlim(-0.8, len(event_types) - 0.2)
ax_bubble.set_ylim(0, 1)
ax_bubble.axis("off")
ax_bubble.set_title("Event Distribution", fontsize=14, pad=12)
plt.tight_layout(rect=[0, 0, 1, 0.93])
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
plt.close(fig)
report = buf.getvalue()

# Write output
Path("/mnt/netapp-volumes/quick-start/event_report.png").write_bytes(report)