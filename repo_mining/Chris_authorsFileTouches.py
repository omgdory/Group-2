import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")


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


def is_source_file(filename):
    # source files
    source_extensions = ['.java', '.kt', '.xml', '.gradle']
    return any(filename.lower().endswith(ext) for ext in source_extensions)


def collect_file_touches(lsttokens, repo):
    # Structure: {filename: [(author, date), ...]}
    file_touches = {}
    ipage = 1
    ct = 0

    try:
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if len(jsonCommits) == 0:
                break

            for commit in jsonCommits:
                sha = commit['sha']
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']

                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                for file_obj in shaDetails['files']:
                    filename = file_obj['filename']
                    if is_source_file(filename):
                        if filename not in file_touches:
                            file_touches[filename] = []
                        file_touches[filename].append((author, date))
                        print(f"Processing: {filename} by {author}")

            ipage += 1

    except Exception as e:
        print(f"Error receiving data: {e}")
        return file_touches

    return file_touches


# GitHub repo
repo = 'scottyab/rootbeer'
lstTokens = ["BlahBlahBlahBlahBlahBlah"]  # Replace tokens when committing to github!!!!

file_touches = collect_file_touches(lstTokens, repo)

# Write to CSV
file = repo.split('/')[1]
output_file = f'data/author_touches_{file}.csv'

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Author", "Date"])

    for filename, touches in file_touches.items():
        for author, date in touches:
            writer.writerow([filename, author, date])

print(f"Data written to {output_file}")