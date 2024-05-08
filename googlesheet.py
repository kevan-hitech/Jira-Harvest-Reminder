import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Token
TOKEN_PATH = "/home/kevan/jiraserver/credentials/token.json"
# API Scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "14cM_JQguuJfztJQizVR4Crt-KWlNeGcVFJiFm24BRfg"
RANGE_NAME = "Weekly Harvest Review Assignments"
# RANGE_NAME = "Weekly Harvest Review Assignments!A:E"


class GoogleSheet:
    def __init__(self) -> None:
        self.token_path = TOKEN_PATH
        self.scopes = SCOPES
        self.spreadsheet = SPREADSHEET_ID
        self.range = RANGE_NAME

    def credentials(self):
        """
        Generate or use existing credentials to the Google API
        """

        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(
                self.token_path,
                self.scopes
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.token_path,
                    self.scopes
                )
                creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(self.token_path, "w") as token:
            token.write(creds.to_json())
        return creds

    def get_spreadsheet(self):
        """
        Call the Sheets API and grab the sheet
        """

        try:
            service = build("sheets", "v4", credentials=self.credentials())
            sheet = service.spreadsheets()
            result = (sheet.values().get(
                spreadsheetId=self.spreadsheet,
                range=self.range
                )
                .execute())
            values = result.get("values", [])

            if not values:
                print("No data found")
                return

            return values

        except HttpError as err:
            print(err)


# MAIN
if __name__ == "__main__":
    values = GoogleSheet().get_spreadsheet()
    for row in values:
        client = row[0]
        client_lead = row[1]
