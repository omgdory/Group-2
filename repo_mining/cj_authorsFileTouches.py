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

def file_extensions(filename):
    file_extensions_source = ['.java', '.py', '.h', '.c', '.cpp', '.js', '.gradle', '.kt', '.xml', '.go', '.rb']
    return any(filename.lower().endswith(extension) for extension in file_extensions_source)

# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def count_file_touches(lsttokens, repo):
    file_touches = {}
    ipage = 1  # url page counter
    ct = 0  # token counter

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
                author = shaObject['commit']['author']['name']
                date = shaObject['commit']['author']['date']

                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                for file_obj in shaDetails['files']:
                    filename = file_obj['filename']
                    if file_extensions(filename):
                        if filename not in file_touches:
                            file_touches[filename] = []
                        file_touches[filename].append((author, date))
                        print(f"Processing: {filename} by {author}")

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    return file_touches
# GitHub repo
repo = 'scottyab/rootbeer'

lstTokens = ["ehhhidkjim"]

file_touches = count_file_touches(lstTokens, repo)
output = "data/cj_authorsFileTouches.csv"

with open(output, 'w', newline='') as e:
    writer = csv.writer(e)
    writer.writerow(["Filename", "Author", "Date"])

    for filename, touches in file_touches.items():
        for author, date in touches:
            writer.writerow([filename, author, date])

e.close()

print(f"Data written to {output}")