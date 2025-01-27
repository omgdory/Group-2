# generates a scatter plot (using matplotlib) of weeks vs file 
# variables where the points are shaded according to author variable.

import pandas as pd
import matplotlib.pyplot as plt
  
#Data collected from scottyab/rootbeer
csvFileName = "commitInfo.csv"
# Read file
dataFrame = pd.read_csv(csvFileName)
# Create a unique list of authors to map each one to a color
authors = dataFrame['Name'].unique()
# Get colormap with 20 distinct colors to use
colors = plt.colormaps['tab20']
# Create a color map for the authors
authorColorMap = {author: colors(i) for i, author in enumerate(authors)}

for _, row in dataFrame.iterrows():
    author = row['Name']
    color = authorColorMap[author]
    plt.scatter(row['File_Variable'], row['Week_Number'], color=color)
# Labels and title
plt.ylabel('Week Number')
plt.xlabel('File Variable')
plt.title('File Variable VS Weeks')
plt.tight_layout()
plt.show()
