import json
import requests
import csv
import os

# ------------ User-defined PART: define what you consider “source file”. -------------
# Example approach: we only collect files if they end with .java or .kt for an Android/Java/Kotlin repo.
# You can expand or change this list as needed for the repo you’re analyzing.
SOURCE_FILE_EXTENSIONS = {".java", ".kt", ".py", ".cpp", ".h", ".c"}

# ------------------------------------------------------------------------------------

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lst_tokens, ct):
    jsonData = None
    try:
        # cycle through the list of tokens (to avoid rate-limits if multiple tokens exist)
        ct = ct % len(lst_tokens)
        headers = {'Authorization': f'Bearer {lst_tokens[ct]}'}
        request = requests.get(url, headers=headers)
        request.raise_for_status()
        jsonData = request.json()
        ct += 1
    except Exception as e:
        print(f"Error in request: {e}")
    return jsonData, ct

# @dict_files: dictionary {filename -> count of touches}
# @lst_tokens: list of tokens for GitHub
# @repo: string "owner/repo", e.g. "scottyab/rootbeer"
def countfiles(dict_files, lst_tokens, repo):
    ipage = 1  # pagination index
    ct = 0     # token counter

    try:
        while True:
            spage = str(ipage)
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            json_commits, ct = github_auth(commits_url, lst_tokens, ct)

            # If no more commits, break
            if not json_commits or len(json_commits) == 0:
                break

            # For each commit, get the file list (sha -> commit details)
            for commit_obj in json_commits:
                sha = commit_obj['sha']
                sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                sha_details, ct = github_auth(sha_url, lst_tokens, ct)
                if not sha_details:
                    continue

                files_json = sha_details.get('files', [])
                for fobj in files_json:
                    filename = fobj['filename']
                    # filter by extension
                    if is_source_file(filename):
                        dict_files[filename] = dict_files.get(filename, 0) + 1

            ipage += 1
    except Exception as e:
        print(f"Error receiving data: {e}")
        exit(0)

def is_source_file(filename):
    # check the extension
    # you could also do more advanced checks, for example .startswith() or analyzing file content
    lower_name = filename.lower()
    for ext in SOURCE_FILE_EXTENSIONS:
        if lower_name.endswith(ext):
            return True
    return False

# ------------------ Main Execution ------------------
# for example, scottyab/rootbeer
repo = 'scottyab/rootbeer'

# put your tokens here
lstTokens = []

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of source files: ' + str(len(dictfiles)))

repo_name = repo.split('/')[1]
fileOutput = f"data/file_{repo_name}_sourcefiles.csv"

with open(fileOutput, 'w', newline='', encoding='utf-8') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Touches"])

    bigcount = None
    bigfilename = None

    for filename, count in dictfiles.items():
        writer.writerow([filename, count])
        if bigcount is None or count > bigcount:
            bigcount = count
            bigfilename = filename

print(f'The source file "{bigfilename}" has been touched {bigcount} times.')
