import json
import requests
import csv
import os
from datetime import datetime

def github_auth(url, lst_tokens, ct):
    try:
        ct = ct % len(lst_tokens)
        headers = {'Authorization': f'Bearer {lst_tokens[ct]}'}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        ct += 1
        return r.json(), ct
    except Exception as e:
        print(f"Error: {e}")
        return None, ct

def load_sourcefiles(csv_path):
    source_files = set()
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_files.add(row['Filename'])
    return source_files

def collect_authors_and_dates(repo, source_files, lst_tokens):
    page = 1
    ct = 0
    results = []  # we’ll store a list of dicts: {"filename":..., "author":..., "date":...}

    while True:
        commits_url = f'https://api.github.com/repos/{repo}/commits?page={page}&per_page=100'
        data, ct = github_auth(commits_url, lst_tokens, ct)
        if not data or len(data) == 0:
            break

        for commit_obj in data:
            sha = commit_obj['sha']
            commit_details_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
            commit_details, ct = github_auth(commit_details_url, lst_tokens, ct)
            if not commit_details:
                continue

            # Extract the commit author info (could be commit_details['commit']['author'] or top-level .['author'])
            # best to handle potential missing fields
            author_login = None
            if 'author' in commit_obj and commit_obj['author']:
                author_login = commit_obj['author']['login']  # the GitHub username
            else:
                # fallback if the commit is from a merged or unknown author
                author_login = commit_details['commit']['author']['name']

            # commit date
            # commit_details['commit']['author']['date'] assumeme "2022-01-01T12:34:56Z"
            commit_date_str = commit_details['commit']['author']['date']
            commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')

            # files in this commit
            files_changed = commit_details.get('files', [])
            for fobj in files_changed:
                filename = fobj['filename']
                # only record if it’s in our source-files set
                if filename in source_files:
                    results.append({
                        "filename": filename,
                        "author": author_login,
                        "date": commit_date
                    })

        page += 1
    return results

if __name__ == "__main__":
    # example usage:
    repo = "scottyab/rootbeer"
    repo_name = repo.split('/')[1]

    # same tokens as before
    lstTokens = []

    # Path to the CSV created by our adapted CollectFiles script
    sourcefiles_csv = f"data/file_{repo_name}_sourcefiles.csv"
    source_files = load_sourcefiles(sourcefiles_csv)

    # collect authors & dates
    author_date_records = collect_authors_and_dates(repo, source_files, lstTokens)

    # write out to a CSV
    # e.g.: data/authorsFileTouches_<repoName>.csv
    output_path = f"data/authorsFileTouches_{repo_name}.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(["filename", "author", "date"])
        for r in author_date_records:
            writer.writerow([r["filename"], r["author"], r["date"].isoformat()])

    print(f"Done! Wrote {len(author_date_records)} touches to {output_path}")
