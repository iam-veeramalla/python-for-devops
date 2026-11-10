# Dictionaries and Sets

## GitHub pull request reporting

The `04-demo-github-integration.py` script counts pull requests by creator in the Kubernetes repository. It uses the existing `requests` dependency.

Install the dependency and run the script from the repository root:

```bash
python -m pip install requests
python Day-11/04-demo-github-integration.py
```

The GitHub API returns at most 100 pull requests per page. The script follows the API's pagination links until there are no more pages, then prints contributors from highest to lowest count and the total number of pull requests processed. Pull requests without a user login are included in the total and reported separately.

Each HTTP request has a 10-second timeout so a stalled connection does not hang indefinitely. The script reports HTTP/API errors, connection problems, invalid JSON, and rate limits clearly; unauthenticated GitHub API requests have rate limits, so retry after the time shown when one is reached.
