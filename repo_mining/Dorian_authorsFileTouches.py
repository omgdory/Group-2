from datetime import datetime
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
        pass
        print(e)
    return jsonData, ct

# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def count_authorsFileTouches(lsttokens, repo):
    file_author_date = []
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
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                if not shaDetails:
                    break
                # help from jose
                for file in shaDetails.get('files', []):
                    filename = file['filename']
                    validFile = False
                    extensions = [".java", ".kt", ".cpp", ".c"]
                    for extension in extensions:
                        if filename.endswith(extension):
                            validFile = True
                    if validFile:
                        author = shaObject['commit']['author']['name']
                        # convert date to datetime object (help from aviendha)
                        date = shaObject['commit']['author']['date']
                        # date = datetime.strptime(shaObject['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
                        # create entry if it does not already exist
                        file_author_date.append((filename, author,date))
            ipage += 1
        return file_author_date
    except Exception as e:
        print("Error receiving data")
        print(e)
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
lstTokens = ["secret :^)"]

file_author_date = count_authorsFileTouches(lstTokens, repo)
print('Total number of touches: ' + str(len(file_author_date)))

file = "authorsFileTouches"
# change this to the path of your file
fileOutput = '../data/file_' + file + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for file, author, date in file_author_date:
    rows = [file, author, date]
    writer.writerow(rows)
fileCSV.close()
print('Authors and touch dates successfully written to ' + fileOutput)