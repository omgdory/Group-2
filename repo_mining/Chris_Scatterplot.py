import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_scatter_plot(csv_file):
    df = pd.read_csv(csv_file)

    # Convert dates to weeks since project start
    df['Date'] = pd.to_datetime(df['Date'])
    project_start = df['Date'].min()
    df['Weeks'] = ((df['Date'] - project_start).dt.total_seconds() / (7 * 24 * 60 * 60)).astype(int)

    # Get unique authors and assign colors
    authors = df['Author'].unique()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(authors)))
    author_colors = dict(zip(authors, colors))

    # Count file touches
    file_touch_counts = df['Filename'].value_counts()

    # Create scatter plot
    plt.figure(figsize=(15, 10))

    for author in authors:
        author_data = df[df['Author'] == author]
        plt.scatter(author_data['Weeks'],
                    [file_touch_counts[f] for f in author_data['Filename']],
                    c=[author_colors[author]],
                    label=author,
                    alpha=0.6)

    plt.xlabel('Weeks Since Project Start')
    plt.ylabel('Total File Touches')
    plt.title('File Touches Over Time by Authors')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save the plot
    plt.savefig('data/file_touches_scatter.png', bbox_inches='tight')
    plt.close()


# Use the scatter plot
csv_file = 'data/author_touches_rootbeer.csv'
create_scatter_plot(csv_file)