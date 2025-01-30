import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from datetime import datetime

# x = file 
# y = weeks (have to get weeks from time data from csv)
# plot: when author touched
source_files_path = "data/Aviendha_authorsFileTouches.csv"  # path to csv file
df = pd.read_csv(source_files_path)

# get the week for the y-axis
df['date'] = pd.to_datetime(df['date'])
y = (df['date'] - df['date'].min()).dt.days / 7.0

# unsorted
files_unique = (df['filename'].unique())
authors_unique = (df['author'].unique())

# idex files and authors
file_index = {f: i for i, f in enumerate(files_unique)}
author_index= {a: i for i, a in enumerate(authors_unique)}

x = df['filename'].map(file_index)
authors = df['author'].map(author_index)

plt.figure(figsize=(10, 6))
cmap = cm.get_cmap('Paired', len(authors_unique)) 
# I can't decide which one I like 

scatter = plt.scatter(x, y, c=authors, cmap=cmap)

plt.xlabel("files")
plt.ylabel("weeks")
plt.tight_layout()
plt.show()
