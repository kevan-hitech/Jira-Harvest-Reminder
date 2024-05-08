from typing import Dict, Any
from fastapi import FastAPI
from datetime import datetime
import uvicorn
# Custom module
from googlesheet import GoogleSheet
from jirahelper import create_issue, create_issue_subtask
from timechecker import monthly_review, weekly_review

app = FastAPI()
clientlist = GoogleSheet().get_spreadsheet()[1::]


@app.post("/jira/harvestreview")
async def jira_onboarding(jiradata: Dict[str, Any]):
    """
    Review if weekly and/or monthly Harvest Review need to be sent out
    """
    try:
        month = jiradata["month"]
        day = jiradata["day"]
        year = jiradata["year"]
        date = datetime(year, month, day)
    except KeyError:
        date = datetime.now()

    print(date)
    return_message = []

    # Weekly Harvest Post
    weekly = weekly_review(date)

    # Either return the range of return nothing
    if weekly:
        # Post
        message = f"Weekly Harvest Review | {weekly}"
        return_message.append(message)
        key = create_issue(message)
        for client in clientlist:
            client_name = client[0]
            client_lead = client[1]
            create_issue_subtask(key, client_name, client_lead, weekly)
    else:
        return_message.append("No Weekly Post")

    # Monthly Harvest Post
    monthly = monthly_review(date)

    # Either return the range or return nothing
    if monthly:
        # Post
        message = f"Monthly Harvest Review | {monthly}"
        return_message.append(message)
        key = create_issue(message)
        for client in clientlist:
            client_name = client[0]
            client_lead = client[1]
            create_issue_subtask(key, client_name, client_lead, monthly)
    else:
        return_message.append("No Monthly Post")

    return {"message": return_message}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
