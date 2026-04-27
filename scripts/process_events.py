import csv
import io
from collections import Counter
from pathlib import Path
# Read input
value = Path("/mnt/netapp-volumes/quick-start/events.csv").read_text()

reader = csv.DictReader(io.StringIO(value))
counts = Counter(row["event_type"] for row in reader)
buf = io.StringIO()
writer = csv.writer(buf)
writer.writerow(["event_type", "count"])
for event_type, count in counts.most_common():
    writer.writerow([event_type, count])
event_counts = buf.getvalue()

# Write output
Path("/mnt/netapp-volumes/quick-start/event_counts.csv").write_text(event_counts)
print(event_counts)