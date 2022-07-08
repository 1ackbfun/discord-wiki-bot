import re
import json
from urllib import parse
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


def read_config() -> dict:
    result = None
    try:
        with open(r'./config.json', 'r', encoding='utf8') as f:
            result = json.loads(f.read())
            f.close()
            print(f'[INFO] Read config file successed')
    except Exception as e:
        print(f'[ERROR] Read config file failed\n{e}')
        exit(1)
    return result


CONFIG = read_config()


def urlencode(keyword: str) -> str:
    return parse.quote(keyword).replace('%20',
                                        '_').replace('%23', '#').replace(
                                            '%2B', '+').replace('%3A', ':')


@bot.event
async def on_ready():
    print('[INFO] Bot is ready')


@bot.event
async def on_message(ctx):
    #print(ctx.channel)
    match_res = re.match(r'.*\[\[(.+)\]\].*', ctx.content, re.M | re.I)
    if match_res:
        await ctx.channel.send(CONFIG["WIKI_URL"] +
                               urlencode(match_res.group(1)))
    match_res = re.match(r'.*\{\{(.+)\}\}.*', ctx.content, re.M | re.I)
    if match_res:
        await ctx.channel.send(
            f'{CONFIG["WIKI_URL"]}Template:{urlencode(match_res.group(1))}')


def main() -> None:
    bot.run(CONFIG["TOKEN"])
    return


if __name__ == '__main__':
    main()
