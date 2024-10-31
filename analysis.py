import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
from tenacity import retry, wait_exponential, stop_after_attempt
from datetime import datetime

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
BASE_URL = "https://api.github.com"

def clean_company_name(company):
    if company:
        company = company.strip()
        if company.startswith('@'):
            company = company[1:]
        return company.upper()
    return ""

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def fetch_with_retry(url):
    print(f"Fetching data from {url} at {datetime.now()}")
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response

def fetch_users_in_shanghai(min_followers=200):
    users = []
    page = 1
    while True:
        url = f"{BASE_URL}/search/users?q=followers:>{min_followers}+location:Shanghai&per_page=100&page={page}"
        response = fetch_with_retry(url)
        data = response.json()

        if 'items' in data and data['items']:
            for item in data['items']:
                user_details_response = fetch_with_retry(item['url'])
                user_details = user_details_response.json()
                users.append({
                    'login': user_details.get('login', ''),
                    'name': user_details.get('name', ''),
                    'company': clean_company_name(user_details.get('company', '')),
                    'location': user_details.get('location', ''),
                    'email': user_details.get('email', ''),
                    'hireable': user_details.get('hireable', ''),
                    'bio': user_details.get('bio', ''),
                    'public_repos': user_details.get('public_repos', 0),
                    'followers': user_details.get('followers', 0),
                    'following': user_details.get('following', 0),
                    'created_at': user_details.get('created_at', '')
                })
            page += 1
        else:
            break

    return users


def fetch_repositories_for_user(username, max_repos=500):
    repos = []
    url = f"{BASE_URL}/users/{username}/repos?per_page=100"
    
    while url and len(repos) < max_repos:
        try:
            print(f"Fetching repositories for {username} from {url}")
            response = fetch_with_retry(url)
            data = response.json()
            
            for repo in data:
                repos.append({
                    'login': username,
                    'full_name': repo.get('full_name', ''),
                    'created_at': repo.get('created_at', ''),
                    'stargazers_count': repo.get('stargazers_count', 0),
                    'watchers_count': repo.get('watchers_count', 0),
                    'language': repo.get('language', ''),
                    'has_projects': repo.get('has_projects', False),
                    'has_wiki': repo.get('has_wiki', False),
                    'license_name': repo['license']['key'] if repo.get('license') else ''
                })
            
            url = response.links.get('next', {}).get('url')
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories for {username}: {e}")
            break

    return repos

# Main function to create CSV files
def create_csv_files():
    users = fetch_users_in_shanghai()
    users_df = pd.DataFrame(users)
    users_df.to_csv("users.csv", index=False)
    print("Users data saved to users.csv")
    
    all_repos = []
    for user in users:
        repos = fetch_repositories_for_user(user['login'])
        all_repos.extend(repos)
    
    repos_df = pd.DataFrame(all_repos)
    repos_df.to_csv("repositories.csv", index=False)
    print("Repositories data saved to repositories.csv")

# Run the script
if __name__ == "__main__":
    create_csv_files()
