import asyncio
import websockets
import json
from atproto import Client, client_utils

## Creds:
atname = "username.bsky.social" #enter your username on BlueSky
atapi = "api-123-abc" #enter your app specific password

async def handle_connection(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
#            print(message)  # debug, print all incoming data

            if data[0] == "EVENT" and data[1].get("kind") == 1:
                tags = data[1].get("tags", [])
                if any(tag[0] == "e" for tag in tags):
                    continue #avoid bridging replies

                content = data[1].get("content")
                post_id = data[1].get("id")

                if content:
                    if len(content) > 300:
                        at_post_long = (f"This post was bridged from Nostr to AT via a yet named bridge, however, the post exceeded the character limit. View the post at: https://njump.me/{post_id}") #BlueSky currently limits posts to 300 characters. Nostr does not.
                        print(at_post_long)
                        at_post = content
                        client = Client()
                        profile = client.login(atname, atapi)
                        text = client_utils.TextBuilder().text(at_post_long)
                        post = client.send_post(text)
                        print('Posting to AT Protocol')

                    else:
                        print(f"Received Post: {content}")
                        at_post = content
                        client = Client()
                        profile = client.login(atname, atapi)
                        text = client_utils.TextBuilder().text(at_post)
                        post = client.send_post(text)
                        print('Posting to AT Protocol')

    except websockets.exceptions.ConnectionClosed as e:
        print("Connection closed")

async def main():
    server = await websockets.serve(handle_connection, "localhost", 4200)
    print("Bridge started on ws://localhost:4200")
    await server.wait_closed()

asyncio.run(main())
