from flask import Flask, request, jsonify
from requests.auth import HTTPBasicAuth
import requests
import json

app = Flask(__name__)

def createJIRA():
  #please enter your url - change the url to your jira url
    url = "https://akshay05pakhanati.atlassian.net/rest/api/3/issue"
#please enter your API_Token
    API_TOKEN = "*provide your API_TOKEN here"
  #*change to your gmail id under auth section.*
    auth = HTTPBasicAuth("akshay05pakhanati@gmail.com", API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "fields": {
            "description": {
                "content": [
                    {
                        "content": [
                            {
                                "text": "My first jira ticket",
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            },
            "project": {
              #*please provide your jira project key value I have given mine* 
                "key": "AK"
            },
            "issuetype": {
                "id": "10007"
            },
            "summary": "First JIRA Ticket"
        },
        "update": {}
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    return response

@app.route('/createJira', methods=['POST'])
def handle_webhook():
    # Verify that the request is from GitHub
    if request.headers.get('X-GitHub-Event') == 'issue_comment':
        payload = request.json
        comment = payload['comment']['body']

        # Check if the comment contains "/jira"
        if "/jira" in comment:
            response = createJIRA()
            if response.status_code == 201:
                return jsonify({'message': 'Jira issue created successfully'}), 200
            else:
                return jsonify({'message': 'Failed to create Jira issue', 'status_code': response.status_code}), 500
        else:
            return jsonify({'message': 'No action required'}), 200
    else:
        return jsonify({'message': 'Invalid webhook event'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

