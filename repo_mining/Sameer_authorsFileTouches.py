import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
# from CollectFiles
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

# Source code files
# languages used from repo
sourceFiles = {".java", ".kt", ".cpp", ".h", ".c"}

def findSourceFile(filename):
    for ext in sourceFiles:
        if filename.endswith(ext):
            return True
    return False

# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
# from CollectFiles with modifications to collect author and date info
# returns commitInfo a dict with format filename: (author1, date1), (author2, date2)
def countfiles(lsttokens, repo):
    # replace dictFiles with empty dict
    commitInfo={} 
    ipage = 1  # url page counter
    ct = 0  # token counter
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if not jsonCommits or len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                commitAuthor = shaObject['commit']['author']['name']
                commmitDate = shaObject['commit']['author']['date']
                for filenameObj in shaDetails['files']:
                    filename = filenameObj['filename']
                    if findSourceFile(filename):

                        # initialize commitInfo as list
                        if filename not in commitInfo:
                            commitInfo[filename]=[]
                        # for each filename: append pair of author name and date worked on
                        commitInfo[filename].append((commitAuthor,commmitDate))
                        print(filename)                   
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
    # add return the dict for traversing
    return commitInfo



# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

# GitHub repo
repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
commitInfo = countfiles(lstTokens,repo)
# change this to the path of your file
fileOutput = 'data/fileAuthorTouch_' + file + '.csv'
# title of rows
rows = ["Filename", "Author", "Date"]

# Open the file and print out the sourcecode file names
# for each file name: write author name and date as a pair
# filename: (author1, date1), (author2, date2)
with open(fileOutput, 'w',) as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(rows)
    for fileName, authorDate in commitInfo.items():
        for author, date in authorDate:
            writer.writerow([fileName,author,date])
