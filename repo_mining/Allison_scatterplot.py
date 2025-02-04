import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def scatter_plot(csv_file):
    dataframe = pd.read_csv(csv_file)

    # Convert time to weeks
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    start = dataframe['Date'].min()
    dataframe['Weeks'] = ((dataframe['Date'] - start).dt.days / 7).astype(int)

    # Count file touches
    file_touch_counts = dataframe['Filename'].value_counts()

    # Assign colors to authors
    authors = dataframe['Author'].unique()
    colors = plt.cm.plasma(np.linspace(0, 1, len(authors)))
    author_colors = dict(zip(authors, colors))

    # Create scatter plot
    plt.figure(figsize=(15, 10))

    for author in authors:
        author_data = dataframe[dataframe['Author'] == author]
        plt.scatter(author_data['Weeks'],
                    [file_touch_counts[f] for f in author_data['Filename']],
                    c=[author_colors[author]],
                    label=author,
                    alpha=0.6)

    plt.xlabel('Weeks')
    plt.ylabel('File Touches')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save the plot
    plt.savefig('data/file_touches_scatter.png', bbox_inches='tight')
    plt.close()


# Use the scatter plot
csv_file = 'data/authorsFileTouches_rootbeer.csv'
scatter_plot(csv_file)