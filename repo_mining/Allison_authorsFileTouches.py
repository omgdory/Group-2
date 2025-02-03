import json
import requests
import csv
import os

from datetime import datetime

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

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def getDateAuthor(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    file_types = ['.xml', '.kt', '.txt', '.java', '.cpp', '.gradle', '.so'] # source file extensions
    authors_dictionary = {}
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                date = datetime.strptime(shaObject['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
                author = shaObject['commit']['author']['name']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # Filter by file type
                    if any(filename.lower().endswith(ext) for ext in file_types):
                        if filename not in authors_dictionary:
                            authors_dictionary[filename] = []
                        authors_dictionary[filename].append((author, date))
                    # dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    # print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
    return authors_dictionary
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = []

# ["fd02a694b606c4120b8ca7bbe7ce29229376ee",
#               "16ce529bdb32263fb90a392d38b5f53c7ecb6b",
#              "8cea5715051869e98044f38b60fe897b350d4a"]

# Load csv created by Allison_CollectFiles.py
file = repo.split('/')[1]
fileInput = 'data/file_' + file + '.csv'
files_dictionary = {}

with open(fileInput, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        files_dictionary[row[0]] = int(row[1])

# Find authors and dates
authors_dictionary = getDateAuthor(files_dictionary, lstTokens, repo)

# Save authors and dates to csv
fileOutput = 'data/authorsFileTouches_' + file + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, touches in authors_dictionary.items():
    for author, date in touches:
        rows = [filename, author, date]
        writer.writerow(rows)
fileCSV.close()
print('Authors and dates have been recorded. Hopefully.')
