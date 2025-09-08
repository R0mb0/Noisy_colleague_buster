import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the CSV file
df = pd.read_csv('event_log.csv', parse_dates=['timestamp_iso'])

# Remove weekends
df['weekday'] = df['timestamp_iso'].dt.weekday
df = df[df['weekday'] < 5]

# Graph 1: Volume of triggers over time
plt.figure(figsize=(10,4))
plt.plot(df['timestamp_iso'], df['noise_dbfs'], marker='o', linestyle='-', color='tab:blue', lw=1)
plt.title('Trigger Volume Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Triggered Volume (dBFS)')
plt.grid(True)
plt.tight_layout()
plt.savefig('trigger_volume_vs_time.png')
plt.close()

# Graph 2: Daily trigger count
daily_counts = df.groupby(df['timestamp_iso'].dt.date).size()
plt.figure(figsize=(10,4))
plt.plot(daily_counts.index, daily_counts.values, marker='o', color='tab:red', lw=2)
plt.title('Number of Trigger Events Per Day')
plt.xlabel('Date')
plt.ylabel('Trigger Count')
plt.grid(True)
plt.tight_layout()
plt.savefig('trigger_count_per_day.png')
plt.close()