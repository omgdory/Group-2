import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csvfile = 'data/cj_authorsFileTouches.csv'
df = pd.read_csv(csvfile)

df['Date'] = pd.to_datetime(df['Date'])
df['Week'] = (df['Date'] - df['Date'].min()).dt.days // 7

authors = df['Author'].unique()
colors = plt.cm.rainbow(np.linspace(0, 1, len(authors)))
author_colors = dict(zip(authors, colors))

file_touch_count = df['Filename'].value_counts()

plt.figure(figsize=(15, 10))
for author in authors:
    author_df = df[df['Author'] == author]
    plt.scatter(author_df['Week'], [file_touch_count[f] for f in author_df['Filename']], c=author_colors[author], label=author, alpha=0.7, edgecolors='black')

plt.xlabel('weeks', fontsize=20)
plt.ylabel('File Touch Count', fontsize=20)
plt.xticks(rotation=90)
plt.yticks(fontsize=20)
plt.title("Author touchs over time", fontsize=20)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig('cj_scatterplot.png', bbox_inches='tight')
plt.show()