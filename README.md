### YouTube Live Chat Notifier

---

This Python script allows you to monitor the live chat of a YouTube video and receive notifications on WhatsApp for specific messages or events.

#### Requirements:

- Python 3
- Google API client library (`google-api-python-client`)
- Google Auth Library (`google-auth`)
- Google OAuth Library (`google-auth-oauthlib`)
- `requests` library

#### Installation:

1. Install the required libraries:

   ```
   pip install -r requirements.txt
   ```

2. Ensure you have `configure.py` with your `phone_number` and `api_key` for WhatsApp API.

3. Ensure you have `credentials.json` with your Google API credentials.

#### Usage:

Run the script with the following command:

```
python chat_youtube.py <youtube_live_url> <author_name_to_search>
```

- `<youtube_live_url>`: The URL of the YouTube live stream with live chat enabled.
- `<author_name_to_search>`: The name of the author whose messages you want to monitor.

#### Description:

- The script authenticates the YouTube API using OAuth 2.0 and fetches the live chat ID of the provided YouTube live stream URL.
  
- It then continuously monitors the live chat of the specified video and prints incoming messages.
  
- If a message from the specified author is found, it sends a notification to the provided WhatsApp number using the CallMeBot API.

- It also detects Google Forms or Docs links in the messages and notifies when they are posted.

#### Limitations:

- The script must be kept running during the live stream to monitor the chat continuously.
  
- The YouTube live stream must have live chat enabled and accessible via the YouTube Data API.

#### Note:

- Ensure that the provided YouTube video URL is live and has active chat.

- Make sure your Google API credentials are valid and have the necessary permissions for accessing the YouTube Data API.

- Check the WhatsApp API usage limits to avoid rate limiting issues.

- Ensure that the `configure.py` and `credentials.json` files are correctly set up with your API keys and credentials respectively.