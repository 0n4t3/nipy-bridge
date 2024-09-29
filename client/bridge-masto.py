import asyncio
import websockets
import json
import re
from mastodon import Mastodon

## Creds:
mastoapi = "123abc" #enter your Activity Pub account API key
mastourl = "https://example.com" #enter the url of your Mastodon API compatible fedi server


async def handle_connection(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
#            print(message)  # debug, print all incoming data

            if data[0] == "EVENT" and data[1].get("kind") == 1:
                tags = data[1].get("tags", [])
                if any(tag[0] == "e" for tag in tags):
                    continue #avoid bridging replies

                raw_content = data[1].get("content")
                post_id = data[1].get("id")
                content = re.sub(r'nostr:(\S+)', r'https://njump.me/\1', raw_content)

                if content:
                    if len(content) > 500: # change this to whatever your server's character length is
                        ap_post_long = (f"This post was bridged from Nostr to Activity Pub via NIPY Bridge, however, the post exceeded the instance's character limit. View the post at: https://njump.me/{post_id}") #Mastodon currently limits posts 500 characters by default. Nostr does not.
                        print(ap_post_long)
                        mastodon = Mastodon(
                            access_token = mastoapi,
                            api_base_url = mastourl
                        )
                        tooter = mastodon.toot(ap_post_long)
                        print('Posting to Masto API')

                    else:
                        print(f"Received Post: {content}")
                        ap_post = content
                        mastodon = Mastodon(
                            access_token = mastoapi,
                            api_base_url = mastourl
                        )
                        tooter = mastodon.toot(ap_post)
                        print('Posting to Masto API')

    except websockets.exceptions.ConnectionClosed as e:
        print("Connection closed")

async def main():
    server = await websockets.serve(handle_connection, "localhost", 4200)
    print("Bridge started on ws://localhost:4200")
    await server.wait_closed()

asyncio.run(main())
