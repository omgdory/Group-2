import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime
from collections import defaultdict

def parse_isoformat(date_str):
    # date_str looks like '2023-02-10T14:12:07'
    return datetime.fromisoformat(date_str)

# Load data from the authorsFileTouches CSV
input_csv = "data/authorsFileTouches_rootbeer.csv"  # example path ( but i could change it i guess )

records = []
files_set = set()
authors_set = set()

with open(input_csv, 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename = row["filename"]
        author = row["author"]
        date_str = row["date"]
        dt = parse_isoformat(date_str)

        records.append((filename, author, dt))
        files_set.add(filename)
        authors_set.add(author)

# Convert sets to sorted lists so that we have a stable index
files_list = sorted(list(files_set))
authors_list = sorted(list(authors_set))

# Build helper mappings
file_to_index = { f: i for i, f in enumerate(files_list) }
author_to_index = { a: i for i, a in enumerate(authors_list) }

# We'll define time = number of weeks from earliest commit
earliest_date = min(r[2] for r in records)
def weeks_since_start(d):
    return (d - earliest_date).days / 7.0

# Prepare lists for plotting
x_vals = []
y_vals = []
colors = []

for (filename, author, commit_date) in records:
    week_val = weeks_since_start(commit_date)
    file_idx = file_to_index[filename]
    # color by author index
    author_idx = author_to_index[author]
    x_vals.append(week_val)
    y_vals.append(file_idx)
    colors.append(author_idx)

plt.figure(figsize=(10, 6))
# We can create a colormap or use a built-in one:
cmap = cm.get_cmap('tab10', len(authors_list))  # 'tab10' has 10 discrete colors

scatter = plt.scatter(x_vals, y_vals, c=colors, cmap=cmap, alpha=0.8)
plt.xlabel("Weeks since earliest commit")
plt.ylabel("Files (indexed)")
plt.title("Scatter: Weekly commits per file, colored by Author")

# Create a legend with each author’s color
# This approach:makeee fake points for each author in the legend
handles = []
for author, idx in author_to_index.items():
    handles.append(
        plt.Line2D([0], [0], marker='o', color=cmap(idx), label=author, linestyle='')
    )
plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
