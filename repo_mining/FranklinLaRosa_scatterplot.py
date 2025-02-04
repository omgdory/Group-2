import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_file_touches(csv_file):
    # Load CSV data
    data = pd.read_csv(csv_file)

    # Converting date to weeks 
    data['Date'] = pd.to_datetime(data['Date'])
    start_date = data['Date'].min()
    data['Week Number'] = ((data['Date'] - start_date).dt.days / 7).astype(int)

    # Count the occurrences of each file being touched
    file_touches = data['Filename'].value_counts()
    data['Touch Count'] = data['Filename'].map(file_touches)

    # Assign colors to each unique author
    authors = data['Author'].unique()
    color_map = plt.cm.rainbow(np.linspace(0, 1, len(authors)))
    author_colors = dict(zip(authors, color_map))

    # Plotting the scatter chart
    plt.figure(figsize=(15, 10))

    for author in authors:
        author_data = data[data['Author'] == author]
        plt.scatter(author_data['Touch Count'], author_data['Week Number'],
                    c=[author_colors[author]], label=author, alpha=0.6)

    # Set up plot labels, ticks, and title
    plt.xlabel('File')
    plt.ylabel('Weeks')
    plt.xticks(np.arange(0, data['Touch Count'].max() + 2, 2))
    plt.yticks(np.arange(0, data['Week Number'].max() + 50, 50))

    # Add grid and legend
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
    plt.grid(True, linestyle='--', alpha=0.5)

    # Show and save the plot
    plt.tight_layout()
    plt.show()
    plt.savefig('data/file_touches_scatter_updated.png', bbox_inches='tight')
    plt.close()

# Call the function with CSV file
csv_file = 'data/authorsTouches_rootbeer.csv'
plot_file_touches(csv_file)
