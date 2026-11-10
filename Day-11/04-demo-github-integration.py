# Program to count pull request creators on the Kubernetes GitHub repository.

import sys

import requests

# GitHub API returns up to 100 pull requests per page.
API_URL = "https://api.github.com/repos/kubernetes/kubernetes/pulls"
REQUEST_TIMEOUT = 10


def main():
    pr_creators = {}
    total_pull_requests = 0
    missing_logins = 0
    url = API_URL
    params = {"per_page": 100}

    while url:
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        except requests.exceptions.Timeout:
            print("Request timed out while contacting the GitHub API.", file=sys.stderr)
            return 1
        except requests.exceptions.ConnectionError:
            print("Could not connect to the GitHub API.", file=sys.stderr)
            return 1
        except requests.exceptions.RequestException as error:
            print(f"GitHub API request failed: {error}", file=sys.stderr)
            return 1

        if response.status_code in (403, 429):
            rate_limited = (
                response.status_code == 429
                or response.headers.get("X-RateLimit-Remaining") == "0"
                or "rate limit" in response.text.lower()
            )
            if rate_limited:
                reset_time = response.headers.get("X-RateLimit-Reset")
                message = "GitHub API rate limit reached."
                if reset_time:
                    message += f" Try again after Unix time {reset_time}."
                print(message, file=sys.stderr)
                return 1

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(
                f"GitHub API returned HTTP {response.status_code}: {error}",
                file=sys.stderr,
            )
            return 1

        try:
            pull_requests = response.json()
        except ValueError:
            print("GitHub API returned invalid JSON.", file=sys.stderr)
            return 1

        if not isinstance(pull_requests, list):
            print("GitHub API returned an unexpected response format.", file=sys.stderr)
            return 1

        for pull in pull_requests:
            total_pull_requests += 1
            user = pull.get("user") if isinstance(pull, dict) else None
            creator = user.get("login") if isinstance(user, dict) else None
            if not creator:
                missing_logins += 1
                continue
            pr_creators[creator] = pr_creators.get(creator, 0) + 1

        # Requests exposes GitHub's Link header as relations in response.links.
        next_page = response.links.get("next")
        url = next_page["url"] if next_page else None
        params = None  # The next URL already contains its pagination parameters.

    print("PR Creators and Counts:")
    for creator, count in sorted(
        pr_creators.items(), key=lambda item: (-item[1], item[0].lower())
    ):
        print(f"{creator}: {count} PR(s)")

    print(f"Total pull requests processed: {total_pull_requests}")
    if missing_logins:
        print(f"Pull requests without a user login: {missing_logins}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
