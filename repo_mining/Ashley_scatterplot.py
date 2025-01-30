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
#Setting the figure's size
plt.figure(figsize=(10,6))
# Get colormap with 20 distinct colors to use
colors = plt.colormaps['tab20']
# Create a color map for the authors
authorColorMap = {author: colors(i) for i, author in enumerate(authors)}

authorTrackerList = []
#Plotting the scatterplot
for _, row in dataFrame.iterrows():
    author = row['Name']
    color = authorColorMap[author]
    #x-axis=file variable (represents unique file) y-axis=week number
    #If author is not already in the legend, then add them
    if not author in authorTrackerList:
        plt.scatter(row['File_Variable'], row['Week_Number'], color=color, label=author)
        authorTrackerList.append(author)
    else:
        #Else, plot like normal
        plt.scatter(row['File_Variable'], row['Week_Number'], color=color)
    
# Labels and title
plt.ylabel('Week Number')
plt.xlabel('File Variable')
plt.title('File Variable VS Weeks')
#Moving Legend to outside the scatterplot
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.tight_layout()
plt.show()
