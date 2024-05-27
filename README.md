# Linkbomber
This is a self-hostable bot built off of discord.py. Quick and hacky. I wrote it from scratch, tested, and deployed in about an hour.

# Usage
Install requirements.txt with `pip install -r requirements.txt`. Paste your token in conf.json. Then run `python3 linkbomber.py`. Enjoy your squeaky clean links!

# Limitations
This was a project intended for use on a single server. If I get a chance I'd like to revisit this as some point in the future to add persistent server profiles detailing which ones want automatic linting and vice versa. As it stands running `??toggle` affects this feature globally in all servers for that instance.

In addition to a limited set of blacklisted filters there are also a handful of edge cases this bot doesn't cover, including the ability to parse multiple links in a message. I'd also like a more streamlined way to add and disable custom Regex rules.