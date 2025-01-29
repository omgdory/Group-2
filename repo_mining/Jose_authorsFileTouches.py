"""
Name: Jose Alarcon, NSHE: 5005581810, CS472 GitHub Lab
Description: This file gathers git commits on a specific project.
It then prints this information for easy parsing to .txt file
"""
import json
import requests

def github_auth(url, token):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        return json.loads(response.content)
    except Exception as e:
        print(f"Exception: {e}")
        return None


def authors_and_dates(repo, token):
    authors_dates = {}
    ipage = 1

    while True:
        commits_url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'
        print(f"Fetching commits from: {commits_url}")

        commits = github_auth(commits_url, token)
        if commits is None or len(commits) == 0:
            break

        for commit in commits:
            sha = commit['sha']
            commit_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
            commit_data = github_auth(commit_url, token)
            if not commit_data:
                continue

            for file in commit_data.get('files', []):
                filename = file['filename']
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']
                if filename not in authors_dates:
                    authors_dates[filename] = []
                authors_dates[filename].append((author, date))

        ipage += 1

    return authors_dates



# Main: PRINT TO FILE
repo = 'scottyab/rootbeer'
token = " "

authors_dates = authors_and_dates(repo, token)

data = []

for file_name, touches in authors_dates.items():
    for author, date in touches:
        data.append((file_name, author, date))

output_file = "authors_file_touches_list.txt"
with open(output_file, "w") as file:
    for entry in data:
        file.write(f"{entry}\n")

print(f"Data has been written to {output_file}")
