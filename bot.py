# Token and server ID
TOKEN = "<TOKEN>"
SERVER_ID = "<SERVER ID>"


# Import libraries
import time
try:
    import requests
except ModuleNotFoundError:
    import os
    os.system("pip install requests")
    import requests


# Get all ban entries
print("Getting ban entries...")
resp = requests.get(f"https://discord.com/api/v9/guilds/{SERVER_ID}/bans", headers={
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "Unban Bot (https://www.reddit.com/r/discordapp/comments/1641uu9/how_to_unban_all_banned_users/, 1.0)"
})
if resp.status_code == 401:
    print("Failed to get ban entries (Unauthorized). Are you sure you entered the correct token?")
    exit()
elif resp.status_code == 403:
    print("Failed to get ban entries (Missing Permissions). Are you sure I have the 'Ban Members' permission?")
    exit()
elif resp.status_code == 400:
    print("Failed to get ban entries (Bad Request). Are you sure you entered a server ID?")
    exit()
elif resp.status_code != 200:
    print(f"An unknown error occurred! {resp.status_code}: {resp.text}")
    exit()
else:
    try:
        ban_entries = resp.json()
    except Exception as e:
        print("An exception occurred while trying to decode ban entries: {e}")
        exit()
    else:
        print(f"Successfully got {len(ban_entries)} ban entries!")


# Unban all users
for ban_entry in ban_entries:
    user_id = ban_entry["user"]["id"]
    username = ban_entry["user"]["username"]
    resp = requests.delete(f"https://discord.com/api/v9/guilds/{SERVER_ID}/bans/{user_id}", headers={
        "Authorization": f"Bot {TOKEN}",
        "User-Agent": "Unban Bot (https://www.reddit.com/r/discordapp/comments/1641uu9/how_to_unban_all_banned_users/, 1.0)"
    })
    if resp.status_code == 204:
        print(f"Successfully unbanned {username} ({user_id})!")
    else:
        print(f"Failed to unban {username} ({user_id})! {resp.status_code}: {resp.text}")
    if int(resp.headers.get("X-RateLimit-Remaining", 0)) < 1:
        seconds = float(resp.headers.get("X-RateLimit-Reset-After", 5))
        print(f"Waiting {seconds} seconds for ratelimit to reset...")
        time.sleep(seconds)


print("Complete!")
