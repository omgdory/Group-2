import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
from datetime import datetime

# get data from file
dataFileDirectory = '../data/file_authorsFileTouches.csv'
dataFileContents = pd.read_csv(dataFileDirectory)

# assign specific color to each author
authors = []
for a in dataFileContents['Author']:
  if a not in authors:
    authors.append(a)

# https://stackoverflow.com/questions/4971269/how-to-pick-a-new-color-for-each-plotted-line-within-a-figure
n = len(authors)
colors = cm.rainbow(np.linspace(0, 1, n))

author_to_color = dict()
for i in range(len(authors)):
  author_to_color[authors[i]] = colors[i]

dataFileContents['AuthorColors'] = dataFileContents['Author'].apply(lambda x: author_to_color[x])

# with help from aviendha
dataFileContents['Date'] = pd.to_datetime(dataFileContents['Date'])
# only show first five letters of source file name (excluding path)
dataFileContents['Filename'] = dataFileContents['Filename'].apply(lambda x: x.split('/')[-1][0:5])
y = (dataFileContents['Date'] - dataFileContents['Date'].min()).dt.days / 7.0
plt.scatter(dataFileContents['Filename'], y, c=dataFileContents['AuthorColors'])

plt.xlabel('file')
plt.ylabel('weeks')
plt.title('file touches vs weeks touched')

plt.show()
