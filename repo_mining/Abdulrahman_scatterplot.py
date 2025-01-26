import matplotlib.pyplot as plt

# Example data (replace with real data from your CSV or output)
weeks = [1, 5, 10, 15, 20]  # Example weeks when files were touched
files = [
    "RootBeer.java",
    "MainActivity.kt",
    "Utils.java",
    "toolChecker.cpp",
    "CheckForRootWorker.kt"
]
authors = ["Alice", "Bob", "Charlie", "Alice", "Bob"]  # Example authors

# Map authors to unique colours
author_colours = {"Alice": "red", "Bob": "blue", "Charlie": "green"}
colours = [author_colours[author] for author in authors]

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(weeks, files, c=colours, s=100)
plt.xlabel("Weeks")
plt.ylabel("Files")
plt.title("File Touches by Authors")
plt.grid(True)

# Add legend
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=author)
           for author, color in author_colours.items()]
plt.legend(handles=handles, title="Authors")

# Show the plot
plt.show()
