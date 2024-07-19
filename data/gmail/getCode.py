import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def getCode():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "gmail/clientcred.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        result = service.users().messages().list(maxResults = 1, userId='me').execute() 
        messages = result.get('messages')


        print(messages)

        for msg in messages: 
            txt = service.users().messages().get(userId='me', id=msg['id']).execute() 
    
            try: 
                msnip = txt["snippet"]
                result = re.search("\d{6}",msnip)
                finresult = result.group(0)
                print(finresult) 
                return finresult

            except:
                print("error")
                pass

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    getCode()