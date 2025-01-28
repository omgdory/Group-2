import subprocess

# Example list of source files (replace this with actual files from Part 2)
source_files = [
    "rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeer.java",
    "app/src/main/java/com/scottyab/rootbeer/sample/MainActivity.kt",
    "rootbeerlib/src/main/java/com/scottyab/rootbeer/sample/CheckForRootWorker.kt"
]

# Collect authors and dates for each file
for file in source_files:
    try:
        print(f"Authors and dates for {file}:")
        log_output = subprocess.check_output(
            ["git", "log", "--pretty=format:%an %ad", "--", file],
            text=True
        )
        print(log_output)
        print("-" * 40)
    except subprocess.CalledProcessError:
        print(f"Failed to retrieve log for {file}")