import json
import requests
import csv
import pandas as pd
from datetime import datetime

def github_request(url, token):
    # takes url and authorization token, if request is succesful returns JSON
    response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status() 
    return response.json()

def get_info(repo, source_files, token):
    results = []
    page = 1
    while True:
        # fetches data for 100 commits
        commits_url = f'https://api.github.com/repos/{repo}/commits?page={page}&per_page=100'
        commits = github_request(commits_url, token)
        if not commits:
            break

        for c in commits:
            # examine each commit and extract author and date
            sha = c['sha']
            this_commit_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
            this_commit = github_request(this_commit_url, token)
            author = this_commit['commit']['author']['name']
            date = datetime.strptime(this_commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')

            # if filename is in the list of source files, add information to results
            for file in this_commit.get('files', []):
                filename = file['filename']
                if filename in source_files:
                    results.append({"filename": filename, "author": author, "date": date})

        page += 1
    return results

if __name__ == "__main__":
    repo = "scottyab/rootbeer"                          # repo name
    token = "01"  # github authentication token 
    source_files_path = "data/file_rootbeer.csv"        # path to csv

    # read from csv file 
    input = pd.read_csv(source_files_path)
    source_files = set(input['Filename'])

    author_results = get_info(repo, source_files, token)

    # write to csv file
    df_results = pd.DataFrame(author_results)
    output_path = f"data/Aviendha_authorsFileTouches.csv"
    df_results.to_csv(output_path, index=False, date_format='%Y-%m-%dT%H:%M:%SZ')

    print(f"wrote {len(author_results)} touches to {output_path}")
