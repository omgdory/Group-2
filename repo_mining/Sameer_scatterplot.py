import pandas as pd
import matplotlib.pyplot as plt

# load the CSV file
file_path = 'data/fileAuthorTouch_rootbeer.csv'
file = pd.read_csv(file_path)

# convert date column to datetime format
file['Date'] = pd.to_datetime(file['Date'])

# assign numerical values to filenames for plotting and authors for coloring
file['FileID'], _ = pd.factorize(file['Filename'])
file['AuthorID'], author_labels = pd.factorize(file['Author'])

# create scatter plot with color based on AuthorID
plt.figure(figsize=(10, 6))
scatter = plt.scatter(file['Date'], file['FileID'], c=file['AuthorID'], alpha=0.8, marker='o')

# add colorbar with author labels
cbar = plt.colorbar(scatter)
cbar.set_label('Author Index')
cbar.set_ticks(range(len(author_labels)))
cbar.set_ticklabels(author_labels)

# customize the plot
plt.xlabel('Date')
plt.ylabel('Source Files')
plt.title('File Modifications Over Time')
plt.grid(True)

# show plot
plt.show()
