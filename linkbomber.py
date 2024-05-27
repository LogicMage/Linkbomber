import discord
import re
import json

with open('conf.json', 'r') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

globalScan = config.get("globalScan", True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for ?bomb"))

@client.event
async def on_message(message):
    url_pattern = re.compile(r'https?://[^\s]+')
    clean_url_pattern = re.compile(r'([^\?]+)(\?igshid=[^\&\s]*|\?t=[^\&\s]*|\?s=[^\&\s]*|\?si=[^\&\s]*|\?pd=[^\&\s]*).*')
    
    async def clean_url(url):
        match = clean_url_pattern.match(url)
        if match:
            return match.group(1)
        return url
    
    if message.author == client.user:
        return
    
    if message.content.startswith('?about'):
        await message.channel.send('Source identifiers are modifications made to URLs that deanonymize your activity on the Internet. Say your friend shares a link to a YouTube video with you: `https://youtu.be/MMN3AeMYReI?si=a7FZbzfRshKfKhJq`. When you click on a link with a URL parameter like `?si=a7FZbzfRshKfKhJq`, YouTube now knows that there is a connection between the account that generated the link and the account that clicked on it.\n\nSay now that your friend shares the link on Instagram. Google uses crawlers to look for links containing source identifiers on other platforms and will make a connection between their Instagram account and YouTube account. Now two accounts are tied back to you. Source identifiers perpetually create associations in this way.\n\nTracking IDs like these are not necessary for a website to be displayed or work correctly and should therefore be removed.\n\nTo better protect yourself against tracking elements, I recommend installing the ClearURLs extension (https://docs.clearurls.xyz/) to your browser of choice with a couple of clicks.')
    
    if message.content.startswith('?toggle'):
        if config["globalScan"] == False:
            config["globalScan"] = True
            await message.channel.send("Now scanning every message.")
        else:
            config["globalScan"] = False
            await message.channel.send("No longer scanning every message.")

    if config["globalScan"] == False:
        if message.content.startswith('?bomb'):

            if message.reference and message.reference.resolved:
                referenced_message = message.reference.resolved
                urls = url_pattern.findall(referenced_message.content) #find a url in the message using the regex pattern
                if urls: #if there's a url in the message...
                    clean_urls = []
                    for url in urls:
                        clean_url = await clean_url(url)
                        clean_urls.append(clean_url)
                    if urls == clean_urls:
                        await message.channel.send("I couldn't find any trackers in the last link sent.")
                    else:
                        await message.channel.send(f'I have removed the tracking element(s) in that link: <{" ".join(clean_urls)}>')
                else:
                    await message.channel.send('I found no link in the referenced message. ')
                return

            async for msg in message.channel.history(limit=20):
                if msg.author == client.user:
                    continue
                urls = url_pattern.findall(msg.content) 
                if urls: 
                    clean_urls = []
                    for url in urls:
                        clean_url = await clean_url(url)
                        clean_urls.append(clean_url)
                    if urls == clean_urls:
                        await message.channel.send("I couldn't find any trackers in the last link sent.")
                    else:
                        await message.channel.send(f'I have removed the tracking element(s) in that link: <{" ".join(clean_urls)}>')
                    return

            await message.channel.send('No links found in recent history (20 messages).')
    else:
        if message.author == client.user:
            return
        urls = url_pattern.findall(message.content)
        if urls:
            clean_urls = []
            for url in urls:
                clean_url = await clean_url(url)
                clean_urls.append(clean_url)
            if urls != clean_urls:
                await message.channel.send(f'I have removed the tracking element(s) in that link: <{" ".join(clean_urls)}>')
            return

client.run(config["botToken"])