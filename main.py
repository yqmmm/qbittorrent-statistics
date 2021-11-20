#!/usr/bin/env python

import datetime
import os
import tempfile

import matplotlib.pyplot as plt
import requests
from pushover import Client

PROM_URL = "http://localhost:9090"
QUERY = "qbittorrent_up_info_data_total"
PUSHOVER_USER_KEY = ""
PUSHOVER_API_KEY = ""

ENV_WITOUT_DEFAULT = ["PUSHOVER_USER_KEY", "PUSHOVER_API_KEY"]

for env_name in ["PROM_URL", "QUERY"]:
    value = os.environ.get(env_name)
    if value is not None:
        globals()[env_name] = value

for env_name in ["PUSHOVER_USER_KEY", "PUSHOVER_API_KEY"]:
    value = os.environ.get(env_name)
    if value is None:
        print(f"Please provide environment variable {env_name}")
        exit(-1)
    globals()[env_name] = value

current_ts = datetime.datetime.now().timestamp()
start_ts = current_ts - 24 * 60 * 60

response = requests.get(
    PROM_URL + "/api/v1/query_range",
    params={
        "query": QUERY,
        "start": start_ts,
        "end": datetime.datetime.now().timestamp(),
        "step": 60,
    },
)

values = response.json()["data"]["result"][0]["values"]

# Calculate total upload today
uploaded_bytes = 0

# Iterate values to handle qbittorrent restart
start_bytes = None
for (pt, pv), (nt, nv) in zip(values, values[1:]):
    if start_bytes is None:
        start_bytes = int(pv)

    # Experienced a restart
    if nv < pv:
        uploaded_bytes += int(pv) - start_bytes
        start_bytes = 0

uploaded_bytes = int(values[-1][1]) - start_bytes
uploaded_GB = uploaded_bytes / 1024 / 1024 / 1024

print(f"{uploaded_GB:.2f} GB")


def hour_of_day(ts):
    return (int(ts) - start_ts) / 60 / 60


# Calculate Speed per minute
speed_per_min_x = [hour_of_day(v[0]) for v in values[5:]]
speed_per_min_y = [
    ((int(b[1]) - int(a[1])) / 1024 / 1024) / (int(b[0]) - int(a[0]))
    for a, b in zip(values, values[5:])
]

x_time = list(map(lambda x: hour_of_day(x[0]), values))
y_upload = list(map(lambda x: int(x[1]) / 1024 / 1024 / 1024, values))

fig, ax1 = plt.subplots()

ax1.set_title("Last 24 Hours:")
ax1.set_xlabel("time (h)")

ax1.set_ylabel("Total uploaded (GB)", color="green")
ax1.plot(x_time, y_upload, color="green")

ax2 = ax1.twinx()
ax2.set_ylabel("Speed (MB/sec)", color="blue")
ax2.plot(speed_per_min_x, speed_per_min_y, color="blue")

img_fp = tempfile.NamedTemporaryFile(suffix=".png")
fig.savefig(img_fp)
img_fp.seek(0)


Client(
    PUSHOVER_USER_KEY,
    api_token=PUSHOVER_API_KEY,
).send_message(f"You have uploaded {uploaded_GB:.1f}GB today!", attachment=img_fp)
