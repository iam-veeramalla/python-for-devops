import requests

def list_github_pull_requests(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    response = requests.get(url)
    if response.status_code == 200:
        pull_requests = response.json()
        print(f"Pull requests for repository {owner}/{repo}:")
        for pr in pull_requests:
            username = pr['user']['login']  # Extracting the username
            print(f"#{pr['number']}: {pr['title']} - {pr['html_url']} (by {username})")
    else:
        print(f"Failed to retrieve pull requests. Status code: {response.status_code}")

# Replace 'owner' and 'repo' with the GitHub repository owner and repository name
list_github_pull_requests('iam-veeramalla', 'terraform-zero-to-hero')
