import base64
import httplib2
import os

from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools


def send_email(sender, to, subject, body):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # File path of the client_secret.json downloaded from the Developer Console
    client_secret_file = dir_path + '/client_id.json'

    # https://developers.google.com/gmail/api/auth/scopes will provide you with all scopes available
    oauth_scope = 'https://www.googleapis.com/auth/gmail.compose'

    # File Location for storing the credentials
    storage = Storage(dir_path + '/gmail.storage')

    # Starting OAuth flow for retrieving credentials
    flow = flow_from_clientsecrets(client_secret_file, scope=oauth_scope)
    http = httplib2.Http()

    # Retrieving credentials from the storage location if available, else generating them
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, http=http)

    # Authorizing httplib2.Http object with the credentials
    http = credentials.authorize(http)

    # Building Gmail service from discovery
    gmail_service = build('gmail', 'v1', http=http)

    # creating a message to send
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    # Sending email
    try:
        message = (gmail_service.users().messages().send(userId="me", body=body).execute())
        print('sent message ID: {}'.format(message['id']))
        return message
    except Exception as e:
        print('message send error {}'.format(e))
        return {}
