# nipy-bridge

Very much a work in progress, check back later.

**Warning: This tool does not verify cryptographic signatures (yet) and is for running locally only. DO NOT place it on a publically accessible server!**

A Nostr to AT/Bluesky &amp; Activity Pub (coming soon) local bridge. This is a work in progress, but can be run on a PC or Android device and then added as a relay to a Nostr client.

To Do (First)
* Create a version that'll post to AT & AP simultaniously
* Write a better readme

To Do (Later)
* Seperate out post lengths for AT & Activity Pub
* Verify cryptographic signatures so it can be remotely hosted


To Do (potentially)
* Get replies (or notifications of replies) from other networks on Nostr

## About & Use Case
This script is designed to run as a local relay which allows a Nostr client to communicate with the BlueSky and Mastodon APIs. It's a bit different from the existing bridges such as [Mostr](https://mostr.pub/) or [Bridgy Fed](https://fed.brid.gy/) which duplicate your account on the respective other protocols. In most cases those bridges are exactly what you're looking for, and if those meet your needs check them out first. However, there are some pros and cons to this setup vs those bridges depending on the use case you're looking for.

**Standard Bridges:**
* No need to host anything
* Replies on remote protocols show up as replies in Nostr. On NIPY Bridge, as things currently stand, you'll need to actually login to the other service to see replies or read posts on that protocol.
* Most bridges are developed by much better developers than me, so you can generally feel safer from jank.

**NIPY Bridge:**
* You control the account you bridge to. Or, well, more accuratly your PDS &/or AP Instance controls the account you're posting to. This means that you can reply, message, and do other normal interactions that are sometimes limited by bridges.
* Bridges are often blocked, while an account used via NIPY Bridge is just a standard account.
* Your username is normal. While on a normal bridge it's [npub].mostr.pub.brid.gy or [npub].mostr.pub, on here you can select whatever username you'd like.
* At the end of the day your 'bridged' account is a normal account, so if you find this setup annoying or just want to use another protocol normally you can always just shutdown the local relay and use or migrate the account like you could any other.

**A Few additonal things to note:**
* Unlike NIPY, this does not require you hand over your NSEC to my spegatti code. While you will need a BlueSky &/or Mastodon API key, API keys can be revoked and don't have the same control over an account as an NSEC would. *Also, if you're mainly on Nostr, you're probably somewhat less worried about a bridged account's security then your NSEC.*
* While it may be a pro or a con depending on who's reading this, using NIPY Bridge means you don't need to worry about somebody else's server going down - although you need to worry about your own device(s) having issues instead.


## How It Works
The NIPY Bridge is just a python script that can be run via console on PC or Termux on Android. Once added as a relay to a Nostr client it listens for nevents your client posts, parses the json of the incoming events, and then procedes in a couple different ways.

) If the post exceeds a character limit it posts a short message along the lines of `This post was bridged from Nostr with NIPY Bridge, however, it exceeded the character limit of [Protocol]. You can read it here at https://njump.me/[nevent]"`

) If the post is a reply to an existing post it disregards it. This is only bridging your posts so it would be useless to have a reply to a missing post on another protocol. Reposts are also disregarded.

) If the post is not a reply, and is under the character limit, it takes the text of the post and posts it to your account on the other protocol.

Quote posts do get bridged over, but with an njump.me link instead of the quoted post's content. Embedded media (images, videos, etc) on the Nostr side will only show up as links on the BlueSky/AP side of things (e.g. https://example.com/tree.jpg instead of actually embedding the image in the post). It's not perfect, but it still works I guess.

## Installation

todo

