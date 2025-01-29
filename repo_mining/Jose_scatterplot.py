"""
Name: Jose Alarcon, NSHE: 5005581810, CS472 GitHub Lab
Description: A file used to create a scatter plot from data
received from git commits. It also produces a file index
mapping to the terminal if needed.
"""
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib.colors import ListedColormap


def parse_file(file_path):
    # Parse:    "filename": [("author", "date"), ...]

    authors_dates = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().strip("()")
            if not line:
                continue
            parts = [p.strip(" '") for p in line.split(",")]
            filename, author, date = parts
            if filename not in authors_dates:
                authors_dates[filename] = []
            authors_dates[filename].append((author, date))
    return authors_dates


def parse_data(authors_dates):
    data = []
    for file, touches in authors_dates.items():
        for author, date in touches:
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            week = (date_obj - datetime.strptime("1970-01-01", "%Y-%m-%d")).days // 7
            data.append((file, week, author))
    df = pd.DataFrame(data, columns=["File", "Week", "Author"])
    return df


def scatter_plot(authors_dates, output_file):
    df = parse_data(authors_dates)
    df["FileIndex"] = pd.factorize(df["File"])[0]

    first_commit_week = df["Week"].min()
    df["WeekRelative"] = df["Week"] - first_commit_week

    # distinct colors for authors
    unique_authors = df["Author"].nunique()
    cmap = ListedColormap(plt.colormaps.get_cmap("tab20").resampled(unique_authors).colors)
    color_map = {author: cmap(i) for i, author in enumerate(df["Author"].unique())}

    # plot
    fig, ax = plt.subplots(figsize=(12, 8))
    for author in df["Author"].unique():
        author_data = df[df["Author"] == author]
        ax.scatter(
            author_data["FileIndex"],
            author_data["WeekRelative"],
            label=author,
            color=color_map[author],
            alpha=0.7,
        )

    # x-axis
    unique_files = pd.factorize(df["File"])[1]
    file_index_map = {i: file for i, file in enumerate(unique_files)}

    step = max(1, len(unique_files) // 20)
    xtick_positions = list(range(0, len(unique_files), step))

    ax.set_xticks(xtick_positions)
    ax.set_xticklabels(xtick_positions, rotation=90, fontsize=8)

    # labels and formatting
    plt.xlabel("File", fontsize=12)
    plt.ylabel("Weeks", fontsize=12)
    plt.title("Productivity Analysis", fontsize=14)

    # legend
    plt.legend(
        title="Authors",
        loc="upper left",
        bbox_to_anchor=(1, 1),
        fontsize=8,
        ncol=1,
        frameon=True,
    )

    # file save
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches="tight")
    print(f"Scatter plot saved to {output_file}")

    print("File Index Mapping:", file_index_map)


# Main
if __name__ == "__main__":
    input_file = "authors_file_touches_list.txt"
    output_file = "scatter_plot.png"

    authors_dates = parse_file(input_file)
    scatter_plot(authors_dates, output_file)

    # file index mapping produced on terminal if needed