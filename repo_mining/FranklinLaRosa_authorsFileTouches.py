import json
import requests
import csv
import os

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
        print(e)
    return jsonData, ct

# @dictFiles, dictionary of files from CollectFiles.py
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def collect_authors_and_dates(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    source_extensions = ['.java', '.kt', '.xml', '.gradle']  # Define source file extensions


    authors_dict = {}  # Structure: {filename: [(author, date), ...]}

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break

            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                author = shaObject['commit']['author']['name']
                date = shaObject['commit']['author']['date']

                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # Check if the file has a source extension
                    if any(filename.lower().endswith(ext) for ext in source_extensions):
                        if filename not in authors_dict:
                            authors_dict[filename] = []
                        authors_dict[filename].append((author, date))
                        print(f" DONE -> {filename}")

            ipage += 1
    except Exception as e:
        print(f"Error receiving data: {e}")
        exit(0)

    return authors_dict

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# Put your tokens here
lstTokens = [""]  

# Load the dictionary of files from CollectFiles.py
file = repo.split('/')[1]
fileInput = 'data/file_' + file + '.csv'
dictfiles = {}

with open(fileInput, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header
    for row in reader:
        dictfiles[row[0]] = int(row[1])

# Collect authors and dates
authors_dict = collect_authors_and_dates(dictfiles, lstTokens, repo)

# Write to CSV
fileOutput = 'data/authorsTouches_' + file + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, touches in authors_dict.items():
    for author, date in touches:
        rows = [filename, author, date]
        writer.writerow(rows)
fileCSV.close()

print('Authors and dates have been written to ' + fileOutput)
