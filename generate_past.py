import random
import csv
from datetime import datetime, timedelta

def parse_date(date_str):
    """
    Converts 'DD_MM_YYYY' into a Python datetime object.
    Example: '20_11_2024' -> datetime(2024, 11, 20)
    """
    day, month, year = date_str.split('_')
    return datetime(int(year), int(month), int(day))

# 1) Set up your known data points
data_points = [
     {
        "date": "30_01_2024",
        "metrics": {
            "discord": 18,
            "reddit": 25,
            "tg": 0,
            "x": 0
        }
    },
     {
        "date": "10_02_2024",
        "metrics": {
            "discord": 22,
            "reddit": 56,
            "tg": 0,
            "x": 21
        }
    },
    {
        "date": "10_04_2024",
        "metrics": {
            "discord": 30,
            "reddit": 1000,
            "tg": 200,
             "x": 15
        }
    },
    {
        "date": "21_06_2024",
        "metrics": {
            "reddit": 6602,
            "x": 1350,
            "discord": 2860,
            "tg": 400,
        }
    },
    {
        "date": "01_10_2024",
        "metrics": {
            "reddit": 7350,
            "discord": 3390,
            "tg": 734,
            "x": 1690
        }
    },
    {
        "date": "20_10_2024",
        "metrics": {
            "reddit": 7554,
            "discord": 3600,
            "tg": 927,
            "x": 1950
        }
    },
    {
        "date": "20_11_2024",
        "metrics": {
            "reddit": 14700,
            "discord": 5200,
            "tg": 1480,
            "x": 3160
        }
    },
    {
        "date": "20_12_2024",
        "metrics": {
            "discord": 6550,
            "reddit": 19200,
            "x": 4334,
            "tg": 2167
        }
    },
    {
        "date": "22_12_2024",
        "metrics": {
            "discord": 7610,
            "reddit": 21200,
            "x": 5160,
            "tg": 2453
        }
    },
    {
        "date": "31_12_2024",
        "metrics": {
            "discord": 7743,
            "reddit": 22248,
            "x": 5516,
            "tg": 2580
        }
    },
    {
        "date": "20_01_2025",
        "metrics": {
            "discord": 8388,
            "reddit": 23832,
            "x": 6330,
            "tg": 2784
        }
    }, 
    {
        "date": "21_01_2025",
        "metrics": {
            "discord": 8440,
            "reddit": 24000,
            "x": 6400,
            "tg": 2788
        }
    }, 
    {
        "date": "26_01_2025",
        "metrics": {
            "discord": 8680,
            "reddit": 24300,
            "x": 6620,
            "tg": 2857
        }
    }
]

# 2) Convert to a structure keyed by actual datetime
known_data = {}
for dp in data_points:
    dt = parse_date(dp["date"])
    known_data[dt] = dp["metrics"]

# Sort the dates in ascending order
sorted_dates = sorted(known_data.keys())

# 3) Gather all unique metric names
all_metrics = set()
for dt in sorted_dates:
    for m in known_data[dt].keys():
        all_metrics.add(m)
all_metrics = sorted(all_metrics)  # e.g. ["discord", "reddit", "tg", "x"]

# 4) Build a day-by-day list of datetimes from the earliest to the latest
start_date = sorted_dates[0]
end_date   = sorted_dates[-1]

day_list = []
current = start_date
while current <= end_date:
    day_list.append(current)
    current += timedelta(days=1)

# 5) Prepare a final structure: daily_results[date][metric] = value
daily_results = {dt: {} for dt in day_list}

def interpolate_with_positive_noise(val1, val2, fraction, noise_scale=0.03):
    """
    - val1, val2: known start/end values (ints or floats)
    - fraction: how far along we are between them (0..1)
    - noise_scale: fraction of abs(val2 - val1) for the upper bound of uniform noise
    - returns an integer value

    Always adds *positive* noise between 0 and noise_scale * difference.
    """
    base = val1 + fraction * (val2 - val1)
    diff = abs(val2 - val1)
    # positive noise from 0 to noise_scale * diff
    noise = random.uniform(0, noise_scale * diff)
    # final value as integer
    return int(round(base + noise))

# For each metric, walk through consecutive known segments
for metric in all_metrics:
    # Collect (date, value) pairs for this metric
    known_pairs = []
    for dt in sorted_dates:
        if metric in known_data[dt]:
            known_pairs.append((dt, known_data[dt][metric]))

    # If the metric never appears, skip
    if not known_pairs:
        continue

    # We'll handle each segment between known_pairs[i] and known_pairs[i+1]
    for i in range(len(known_pairs) - 1):
        (d1, v1) = known_pairs[i]
        (d2, v2) = known_pairs[i+1]

        delta_days = (d2 - d1).days
        for offset in range(delta_days + 1):  # +1 to include d2
            current_day = d1 + timedelta(days=offset)
            fraction = offset / float(delta_days) if delta_days != 0 else 0
            interpolated_value = interpolate_with_positive_noise(v1, v2, fraction)
            daily_results[current_day][metric] = interpolated_value

# 6) (Optional) Fill truly missing metrics if needed
#    For now, if a metric wasn't in any segment, it remains None.

# 7) Print to console (optional)
print("Date, " + ", ".join(all_metrics))
for d in sorted(daily_results.keys()):
    vals = []
    for m in all_metrics:
        val = daily_results[d].get(m, None)
        if val is not None:
            vals.append(str(val))  # already integer
        else:
            vals.append("N/A")
    print(d.strftime("%Y-%m-%d") + ", " + ", ".join(vals))

# 8) Write to a CSV file
csv_filename = "interpolated_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # Write header row
    writer.writerow(["Date"] + list(all_metrics))

    # Write each daily row
    for d in sorted(daily_results.keys()):
        row = [d.strftime("%Y-%m-%d")]
        for m in all_metrics:
            val = daily_results[d].get(m, None)
            row.append(str(val) if val is not None else "N/A")
        writer.writerow(row)

print(f"\nWrote daily results with interpolation (+ positive noise) to '{csv_filename}'.")
