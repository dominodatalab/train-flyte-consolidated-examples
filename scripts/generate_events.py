import csv
import io
import random
from datetime import datetime, timedelta
from pathlib import Path

event_types = [
    "Download Files",
    "Download Folder",
    "View File",
    "Upload Files",
    "Create File",
    "Edit File",
    "Remove File",
    "Remove Files",
    "Rename File / Directory",
    "Rename Multiple Files / Directories",
    "Set Project Runtime Variable",
    "Unset Project Runtime Variable",
    "Set Environment Variable",
    "Unset Environment Variable",
    "Set User Environment Variable",
    "Unset User Environment Variable",
    "Create Environment",
    "Duplicate Environment",
    "Create Environment Revision",
    "Kill Environment Revision Build",
    "Set As Active Environment Revision",
    "Edit Environment",
    "Edit Environment Name",
    "Edit Environment Description",
    "Edit Environment Visibility",
    "Set Default Environment",
    "Archive Environment",
    "Edit Environment Active Pinning",
    "Edit Environment Subscription to Base",
]
start = datetime(2020, 1, 1)
buf = io.StringIO()
writer = csv.writer(buf)
writer.writerow(["timestamp", "event_type", "userid"])
for _ in range(250):
    ts = start + timedelta(seconds=random.randint(0, 60 * 60 * 24 * 365 * 6))
    writer.writerow([ts.isoformat(), random.choices(event_types, range(len(event_types))[::-1])[0], round(random.uniform(0, 1000), 2)])
random_data = buf.getvalue()

output = Path("/mnt/netapp-volumes/quick-start/events.csv")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(random_data)
print(random_data)