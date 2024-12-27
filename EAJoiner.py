from discord.ext import commands
import os, datetime, re, json, time, webbrowser

print("Version 1.5 by enzomtp")

def log(message, error=False):
    if error:
        mess = "\n".join([f"[❌ {datetime.datetime.now().strftime('%d/%m/%Y %H:%M.%S')}] {line}" for line in message.split('\n')])
        tmess = f"\033[91m{mess}\033[0m"
    else:
        mess = "\n".join([f"[✅ {datetime.datetime.now().strftime('%d/%m/%Y %H:%M.%S')}] {line}" for line in message.split('\n')])
        tmess = f"\033[92m{mess}\033[0m"
    print(tmess)
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(mess + "\n")

# Verify and create config.json file if it doesn't exist
if not os.path.exists("config.json"):
    with open("config.json", "w") as file:
        json.dump({
            "token": "",
            "channels": [],
            "count": 0,
            "rate_limit": 120,
            "keywords": []
        }, file, indent=4)
    log("Please fill out the config.json file", True)
    time.sleep(5)
    exit()
else:
    with open("config.json", "r") as file:
        config = json.load(file)

def save_config(key, value):
    config[key] = value
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

bot = commands.Bot("EAJoiner>", self_bot=True)

@bot.command()
async def count(c):
    if not c.author.id == bot.user.id:
        return
    await c.send(config["count"])

@bot.event
async def on_ready():
    log(f'Connected to discord with: {bot.user.name}')

last = datetime.datetime.now()-datetime.timedelta(seconds=config["rate_limit"])

@bot.event
async def on_message(message):
    global last
    if message.channel.id in config["channels"]:
        if last + datetime.timedelta(seconds=config["rate_limit"]) <= datetime.datetime.now():
            if 'https://www.roblox.com/games/15532962292' in message.content or 'http://www.roblox.com/games/15532962292' in message.content:
                    # Find the first matching keyword (case-insensitive)
                    keyword = next(
                        (word for word in config['keywords'] if word.lower() in message.content.lower()), 
                        None
                    )
                    if keyword:
                        last = datetime.datetime.now()
                        LinkCode = re.search(r'privateServerLinkCode=(.*)', message.content).group(1)
                        joinlink = f'roblox://experiences/start?placeId=15532962292&linkCode={LinkCode}'
                        webbrowser.open(joinlink)
                        log(f"=====Joined server with link code: {LinkCode} with the following keyword: \033[1m\033[4m{keyword}\033[24m\033[22m. Message content is the following=====\n{message.content}\n=================================================================End of message content=================================================================")
                        save_config("count", config["count"]+1)
                    else:
                        log(f"====No keyword found. Message content is the following====\n{message.content}\n===================End of message content===================", True)
            else:
                log(f"====Invalid link. Message content is the following====\n{message.content}\n================End of message content================", True)
        else:
            remaining_time = (last + datetime.timedelta(seconds=config["rate_limit"])) - datetime.datetime.now()
            log(f"Rate limit reached. Waiting {remaining_time.seconds} seconds until next check", True)

bot.run(config["token"])