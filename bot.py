import json

from discord.ext.commands.core import command
import urllib.request
import re
import io
import time
from multiprocessing.pool import ThreadPool
import discord
import requests
from discord.ext import commands
from runes import get_runes
from secret.secret_token import token_class

bot  = commands.Bot(command_prefix='d!')
dark_mode = False

@bot.event
async def on_ready():

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def opgg(ctx, *args):
    print("opgg command was used")
    arg_len = len(args)
    regions = ['oce', 'na', 'las', 'jp', 'br', 'tr', 'ru', 'eune', 'kr', 'lan', 'euw']
    default_region = regions[0]
    async with ctx.typing():
        if arg_len == 0:
            name = str(ctx.message.author).split('#')[0]
            if default_region == 'kr':
                await ctx.send(f"https://www.op.gg/summoner/userName={name}")
            else:
                await ctx.send(f"https://{default_region}.op.gg/summoner/userName={name}")
        
        elif arg_len >= 2 and args[0].lower() in regions:
            name = re.sub(r'\s' , r'+', ''.join(args[1:]))
            if args[0].lower() == 'kr':
                await ctx.send(f"https://www.op.gg/summoner/userName={name}")
            else:
                await ctx.send(f"https://{args[0].lower()}.op.gg/summoner/userName={name}")

        elif arg_len >= 1:
            name = re.sub(r'\s' , r'+',' '.join(args[0:]))
            await ctx.send(f"https://oce.op.gg/summoner/userName={name}")

        else:
            await ctx.send(f"Usage: /opgg [region] [name]")

@bot.command()
async def darkmode(ctx, *args):
    global dark_mode
    dark_mode ^= True
    await ctx.send(f"Dark Mode is {bool(dark_mode)}")

@bot.command()
async def build(ctx, *args):
    '''
    Build Command
    Lists builds for champion from op.gg

    Usage: /build [lane] [champion]
    '''
    print('Build cmd detected')
    if len(args) != 2:
        await ctx.send('Usage: /build [lane] [champion]')
    else:
        async with ctx.typing():
            global dark_mode
            prev_time = time.time()

            # start multiprocessing
            pool = ThreadPool(processes=4)
            rune_img = pool.apply_async(get_runes, args=(args[1], args[0], dark_mode))

            build_url = f'http://lol.lukegreen.xyz/build/{args[0]}/{args[1]}'
            build = ''

            if requests.get(build_url).status_code != 500:
                await ctx.send(f'Lane: {args[0].capitalize()}')
                await ctx.send(f'Champ: {args[1].capitalize()}')

                # get items
                with urllib.request.urlopen(build_url) as url:
                    data = json.loads(url.read().decode())
                    for num in range(1, 6):
                        build += f'Build {num}: '
                        for item in data[f'build_{num}']:
                            build += (item.lstrip("(\"\'")) + ', '
                        build += '\n'
                        build = re.sub(r'(,)[\s]$', '', build)
                await ctx.send(build)

                # send runes
                with io.BytesIO() as image_binary:
                    rune_img.get().save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(
                        file=discord.File(
                            fp=image_binary,
                            filename=f'{args[1]} runes.png'
                        )
                    )
                
                print(f"Took {time.time() - prev_time} seconds")
                await ctx.send(f"That took {time.time() - prev_time} seconds")
            else:
                await ctx.send('Please check the spelling of your command input.')

bot.run(token_class().get_token())


