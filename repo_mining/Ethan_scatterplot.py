import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Load the CSV file
csvfile_path = "data/Ethan_authorsfiletouches.csv"
df = pd.read_csv(csvfile_path)

# Convert dates to weeks
#  - assuming the first commit is time zero since project start
df['Date'] = pd.to_datetime(df['Date'])
df['Week'] = (df['Date'] - df['Date'].min()).dt.days // 7  # Converts days to weeks

# Sort files
#  - by the first time they were touched
unique_files = df['Filename'].unique()
file_mapping = {file: idx for idx, file in enumerate(unique_files)}
df['FileIndex'] = df['Filename'].map(file_mapping)

# Assign unique colors to each author
authors = df['Author'].unique()
color_map = {author: cm.plasma(i / len(authors)) for i, author in enumerate(authors)}

max_weeks = df['Week'].max()  # Determine the max week

# -- Plot --
plt.figure(figsize=(15, 10))
for author in authors:
    subset = df[df['Author'] == author]
    plt.scatter(subset['FileIndex'], subset['Week'], color=color_map[author], label=author, alpha=0.8, edgecolors='black')

# -- Formatting --
ytick = np.arange(0, max_weeks + 50, 50)
plt.xticks(ticks=range(len(unique_files)), labels=unique_files, rotation=90, fontsize=8)  # Rotate for readability
plt.yticks(ytick)  # Set y-ticks at fixed intervals of 50
plt.xlabel("files", fontsize=12)
plt.ylabel("weeks", fontsize=12)
plt.title("Author File Activities Over Time", fontsize=14)
plt.legend(title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Save and show the scatter plot
plt.tight_layout()
plt.savefig("Ethan_scatterplot_fig1.png", dpi=300)
plt.show()
