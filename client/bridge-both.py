import asyncio
import websockets
import json
import re
from atproto import Client, client_utils
from mastodon import Mastodon

## Creds:
atname = "username.bsky.social" #enter your username on BlueSky
atapi = "api-123-abc" #enter your app specific password
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
                    if len(content) < 300:
                        #AT/BlueSky Posting
                        print(f"Received Post: {content}")
                        at_post = content
                        client = Client()
                        profile = client.login(atname, atapi)
                        text = client_utils.TextBuilder().text(at_post)
                        post = client.send_post(text)
                        #AP Posting
                        print('Posting to AT Protocol')
                        print(f"Received Post: {content}")
                        ap_post = content
                        mastodon = Mastodon(
                            access_token = mastoapi,
                            api_base_url = mastourl
                        )
                        tooter = mastodon.toot(ap_post)
                        print('Posting to Masto API')

                    elif 300 <= len(content) < 500: #change 500 to your mastodon api compatible server's posting length'
                        # AT Post
                        at_post_long = (f"This post was bridged from Nostr to AT via NIPY Bridge, however, the post exceeded the BlueSky character limit. View the post at: https://njump.me/{post_id}") #BlueSky currently limits posts to 300 characters. Nostr does not.
                        print(at_post_long)
                        at_post = content
                        client = Client()
                        profile = client.login(atname, atapi)
                        text = client_utils.TextBuilder().text(at_post_long)
                        post = client.send_post(text)
                        print('Posting to AT Protocol')
                        #AP Posting
                        print(f"Received Post: {content}")
                        ap_post = content
                        mastodon = Mastodon(
                            access_token = mastoapi,
                            api_base_url = mastourl
                        )
                        tooter = mastodon.toot(ap_post)
                        print('Posting to Masto API')


                    else:
                        #AT Post
                        at_post_long = (f"This post was bridged from Nostr to AT via NIPY Bridge, however, the post exceeded the BlueSky character limit. View the post at: https://njump.me/{post_id}") #BlueSky currently limits posts to 300 characters. Nostr does not.
                        print(at_post_long)
                        at_post = content
                        client = Client()
                        profile = client.login(atname, atapi)
                        text = client_utils.TextBuilder().text(at_post_long)
                        post = client.send_post(text)
                        print('Posting to AT Protocol')
                        #AT Post
                        ap_post_long = (f"This post was bridged from Nostr to Activity Pub via NIPY Bridge, however, the post exceeded the instance's character limit. View the post at: https://njump.me/{post_id}") #Mastodon currently limits posts 500 characters by default. Nostr does not.
                        print(ap_post_long)
                        mastodon = Mastodon(
                            access_token = mastoapi,
                            api_base_url = mastourl
                        )
                        tooter = mastodon.toot(ap_post_long)
                        print('Posting to Masto API')

    except websockets.exceptions.ConnectionClosed as e:
        print("Connection closed")

async def main():
    server = await websockets.serve(handle_connection, "localhost", 4200)
    print("Bridge started on ws://localhost:4200")
    await server.wait_closed()

asyncio.run(main())
