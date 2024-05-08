import json as JSON
import requests
import os


# jiraapi.py - Handles Jira API HTTPS request handling

# Jira API key
HEADERS = {
    'Authorization': os.environ['JIRAPASS'],
    'Content-Type': 'application/json'
    }


def get_issue(issue):
    """
    Get Jira Issue data
    """

    url = "https://hitechnyc.atlassian.net/rest/api/3/issue/%s" % issue
    payload = {}
    headers = HEADERS

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def create_issue(summary):
    """
    Send Jira API POST data to generate subtasks
    """
    url = "https://hitechnyc.atlassian.net/rest/api/3/issue"

    payload = JSON.dumps({
    "fields": {
        "reporter": {
        "id": "557058:f58131cb-b67d-43c7-b30d-6b58d40bd077"
        },
        "project": {
        "id": "10041"
        },
        "issuetype": {
        "id": "10007"
        },
        "description": {
        "content": [
            {
            "content": [
                {
                "text": summary,
                "type": "text"
                }
            ],
            "type": "paragraph"
            }
        ],
        "type": "doc",
        "version": 1
        },
        "summary": summary
    },
    "update": {}
    })

    headers = HEADERS
    response = requests.request("POST", url, headers=headers, data=payload)

    res = (response.json())
    print(res)
    return res["key"]


def create_issue_subtask(key, client, clientlead, timerange):
    """
    Send Jira API POST data to generate subtasks
    """
    url = "https://automation.atlassian.com/pro/hooks/d5b5f3820a4b86953d6022e1cd0bdf42a0ce568d?issue=%s" % (key)

    payload = JSON.dumps({
        "data": {
            "key": key,
            "client": client,
            "clientlead": clientlead,
            "timerange": timerange,
            }
    })

    headers = HEADERS
    print(key, client, clientlead, timerange)
    response = requests.request("POST", url, headers=headers, data=payload)
