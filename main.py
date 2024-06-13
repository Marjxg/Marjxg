import os
import requests
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME = os.getenv('GITHUB_USERNAME')

headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

repos_url = f'https://api.github.com/user/repos'
repos_params = {
    'visibility': 'all',
    'affiliation': 'owner',
    'per_page': 100
}

repos = []
page = 1
while True:
    repos_params['page'] = page
    response = requests.get(repos_url, headers=headers, params=repos_params)
    data = response.json()
    if not data:
        break
    repos.extend(data)
    page += 1

languages = defaultdict(int)
total_size = 0

for repo in repos:
    languages_url = repo['languages_url']
    repo_languages = requests.get(languages_url, headers=headers).json()
    for language, size in repo_languages.items():
        languages[language] += size
        total_size += size

# Calculate percentages
language_percentages = {language: (size / total_size) * 100 for language, size in languages.items()}

# Print or write the results to a file
with open('README.md', 'a') as file:
    for language, percentage in language_percentages.items():
        file.write(f'- **{language}**: {percentage:.2f}%\n')
