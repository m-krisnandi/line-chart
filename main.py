import pandas as pd
import re
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {
        "Timestamp": [],
        "Bitrate": [],
        "Interval": []
    }

    timestamp = None
    for line in lines:
        if "Timestamp:" in line:
            timestamp = re.search(r"Timestamp: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line).group(1)
        elif re.match(r"\[\s*\d+\]", line):
            interval_match = re.search(r"(\d+\.\d+-\d+\.\d+)\s+sec", line)
            bitrate_match = re.search(r"(\d+\.\d+)\s+Mbits/sec", line)

            if interval_match and bitrate_match:
                interval = interval_match.group(1)
                bitrate = float(bitrate_match.group(1))

                data["Timestamp"].append(timestamp)
                data["Bitrate"].append(bitrate)
                data["Interval"].append(interval)

    return pd.DataFrame(data)

file_path = 'soal_chart_bokeh.txt'
df = parse_file(file_path)

# Convert Timestamp to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Create a ColumnDataSource from the DataFrame
source = ColumnDataSource(df)

p = figure(title="Network Speed Over Time", x_axis_label='Time', y_axis_label='Bitrate (Mbits/sec)',
           x_axis_type='datetime')

p.line('Timestamp', 'Bitrate', source=source, legend_label="Bitrate", line_width=2)

hover = HoverTool(tooltips=[("Bitrate", "@Bitrate Mbits/sec"), ("Interval", "@Interval")])
p.add_tools(hover)

# Show the results
output_file("network_speed_line_chart.html")
show(p)
