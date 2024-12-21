# nipy-bridge                                 

*Just want a post broadcaster? Check out [NI.PY](https://github.com/0n4t3/nipy)*

A very hacky mess of spegatti code written by me and ChatGPT. This tool acts as a local Nostr relay capable of translating your posts on Nostr to other protocols for bridging/cross posting. 

**Warning: This tool does not verify cryptographic signatures and is for running locally only. DO NOT place it on a publically accessible server!**

A Nostr to AT (Bluesky) &amp; Activity Pub local bridge which can be run on a PC or Android device and added as a relay to a Nostr client.

You're probably better off using regular bridges such as [Mostr](https://mostr.pub), [Bridgy Fed](https://fed.brid.gy/), and the upcoming [Eclipse.Pub](https://eclipse.pub/). They won't require you to host/run anything, they'll have two way communication in most cases, and you won't be relying on my janky code.

### So then, what's this?

Mostly just a proof of concept/personal experiment. Still, it lets you use a standard account instead of a bridge account across multiple protocols. Having a 'normal' account:

* Gets around bridge jankiness. Sometimes bridged @s won't go through if it's not a reply to somebody else, DMs often don't work, and in the case of BlueSky your posts will often by cut off.

* No bridge blocking. Some servers block bridges, but your account here is just a standard account on a standard server.

* Minimal commitment. You don't need to hand off your NSEC and API keys on AP/AT can be revoked. You can log into your AP/AT accounts normally while using the bridge to reply or check notifications, and at any point you can revoke the API keys you gave the script and just have a regular account to use normally. 

## How It Works
The NIPY Bridge is a python script that can be run via console on PC or Termux on Android. Once added as a relay to a Nostr client it listens for nevents your client posts, parses the json of the incoming events, and then procedes in a couple different ways.

) If the post exceeds a character limit it posts a short message along the lines of `This post was bridged from Nostr with NIPY Bridge, however, it exceeded the character limit of [Protocol]. You can read it here at https://njump.me/[nevent]"`

) If the post is a reply to an existing post it disregards it. This is only bridging your posts so it would be useless to have a reply to a missing post on another protocol. Reposts are also disregarded.

) If the post is not a reply, and is under the character limit, it takes the text of the post and posts it to your account on the other protocol.

Quote posts do get bridged over, but with an njump.me link instead of the quoted post's content. Embedded media (images, videos, etc) on the Nostr side will only show up as links on the AT/AP side of things (e.g. https://example.com/tree.jpg instead of actually embedding the image in the post). It's not perfect, but it still works I guess.

## Installation
1: Navigate to the scripts folder and download your preferred script (Only AP via the Mastodon API, only AT via the BlueSky API, or both combined). 

2: Install dependencies with pip `pip install atproto mastodon.py json websockets`

3: Add your api keys. Do so on lines 8+9 for the AT or AP only version or lines 9-12 for the version that posts on both. 

4: If you are posting to AP then set the maximum character limit to your server's limit. It defaults to 500, and can be changed on line 28 on the AP only version or line 31+50 on the AT+AP version. 

5: (Optional) Create a bash/powershell alias to start the script (if you intend to start via the command line) or a desktop shortcut if you intend to start by running the file. 

6: Start the script, open your client, and add the script as a relay (generally should be `wss://localhost:4200`). Try a test post, and assuming it works, whenever you intend to bridge a post just make sure the script is running and post normally. 

## Known Issues

#### Amethyst
For whatever reason, adding this as a local relay to Amythest fails to work. Adding it as a normal relay, however, works fine. 

#### Gossip
Gossip cannot handle localhost urls. Creating a custom host, however, resolves the issue. 
