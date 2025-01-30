import json
import requests
import csv
import os

# Ensure data directory exists for output
if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# ====
# Function that will determine if a file is a source file
#  - Source files typically contain executable code so this will filter files based on their extensions.
def file_filter(filename):
    src_file_extension = {'.py', '.java', '.c', '.cpp', '.h', '.js', '.go', '.rb', '.kt'}
    return any(filename.lower().endswith(exten) for exten in src_file_extension)
# ====

# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo

# ====
# Function to collect all files in the repo
def collect_files(lsttokens, repo):
    commitCount = {} # Dictionary to store the number of times each file was modified
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            # Fetch commits from the repo
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'
            jsonCommits, ct = github_auth(commits_url, lsttokens, ct)

            # break out of the while loop
            if not jsonCommits:
                break  # No more commits

            # Iterate through the commits to extract file changes
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                filesjson = shaDetails.get('files', [])
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if file_filter(filename):  # Only collect source files based off extension
                        commitCount[filename] = commitCount.get(filename, 0) + 1
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    return commitCount
# ====
# Function to get authors and dates for each source file
def get_authors_and_dates(file_list, lsttokens, repo):
    authors_data = {}
    ct = 0  # Token counter

    for filename in file_list:
        commits_url = f"https://api.github.com/repos/{repo}/commits?path={filename}&per_page=100"
        jsonCommits, ct = github_auth(commits_url, lsttokens, ct)

        for commit in jsonCommits:
            author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
            date = commit.get("commit", {}).get("author", {}).get("date", "Unknown")

            if filename not in authors_data:
                authors_data[filename] = []

            authors_data[filename].append((author, date))

    return authors_data
# ====

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["BLANK"]

# ====
# Collect source files from the repository
# - This will basically redo our adapted CollectFiles.py script again
print("Collecting source files...")
source_files = collect_files(lstTokens, repo)
print(f"Total source files found: {len(source_files)}")

# Fetch commit authors and timestamps for each source file
print("Fetching commit authors and dates...")
authors_data = get_authors_and_dates(source_files.keys(), lstTokens, repo)


fileOutput = 'data/Ethan_authorsfiletouches.csv'
# Save/write data to CSV
with open(fileOutput, 'w', newline='') as e:
    writer = csv.writer(e)
    writer.writerow(["Filename", "Author", "Date"])

    for filename, touches in authors_data.items():
        for author, date in touches:
                writer.writerow([filename, author, date])
    
e.close()
print(f"Data has been saved/written. You can find it here: {fileOutput}")
# ====
