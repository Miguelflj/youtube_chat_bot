from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import re
import time
import sys
import requests
from urllib.parse import quote
import configure

phone_number = configure.phone_number
api_key = configure.api_key

print(phone_number)
print(api_key)

def send_wpp_message(phone_number, api_key,message=None):
    url=f'https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={quote(message)}&apikey={api_key}'
    response = requests.get(url)


# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_authenticated_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def get_live_chat_id(youtube, video_id):
    # Call the YouTube API to get live chat details
    live_broadcasts = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_id
    ).execute()

    live_broadcast = live_broadcasts['items'][0]
    live_chat_id = live_broadcast['liveStreamingDetails']['activeLiveChatId']
    return live_chat_id

def is_google_form(message):
    # Regular expression to match Google Docs and Google Forms URLs
    pattern = r"https://(docs|forms)\.google\.com/(forms|document)/[a-zA-Z0-9_-]+"
    return re.search(pattern, message) is not None


def list_live_chat_messages(youtube, live_chat_id, phone_number, api_key,author_search,page_token=None,):
    
    request = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part=["snippet","authorDetails"],
        pageToken=page_token
    )
    response = request.execute()
    messages = response.get('items', [])


    for item in messages:
        author = item['authorDetails']['displayName']
        try:
            message = item['snippet']['displayMessage']
        except:
            message=''
        print(f"{author}:{message}")
        
        if author == author_search:
            send_wpp_message(phone_number,api_key,message)

        if is_google_form(message):
            print(f"posted a Google Docs form: {message}")
            
    next_page_token = response.get('nextPageToken')

    return messages, next_page_token

def main(phone_number, api_key):
    if(len(sys.argv) >= 3):
        youtube = get_authenticated_service()

        # Replace 'VIDEO_URL' with the YouTube video URL
        video_url = sys.argv[1]
        author_search = sys.argv[2:]
        author_search = ' '.join(author_search)
        # Extract video ID from URL
        video_id = video_url.split('=')[-1]
       
        live_chat_id = get_live_chat_id(youtube, video_id)
        print("Live Chat ID:", live_chat_id)

        # Continuously monitor live chat until the end of the live stream
        next_page_token = None
        while True:
            messages, next_page_token = list_live_chat_messages(youtube, live_chat_id,phone_number, api_key,author_search,page_token=next_page_token)
            time.sleep(5)
   
    else:
        print("Do you need pass url from youtube live with live chat!")

if __name__ == "__main__":
    main(phone_number, api_key)
