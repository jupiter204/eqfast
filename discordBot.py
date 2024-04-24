import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
import asyncio
import eqfast
import eqreport

load_dotenv()
bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())
color_list = {'綠色': discord.Color.green(),
              '橙色': discord.Color.orange(), '紅色': discord.Color.red()}


@bot.event
async def on_ready():
    channel = bot.get_channel(988075822780915747)
    time = eqfast.init()
    num = eqreport.init()
    print(f'{bot.user} ready on!!!')
    i = 30
    while True:
        i += 1
        time, msg, area = eqfast.update(time)
        if msg != 0:
            print(msg + '\n' + area)
            await channel.send(f'{msg}\n{area}')
            # await channel.send('test')
        if i >= 30:
            i = 0
            num, color, msg, image, weburl, depth, loc, mag = eqreport.get(num)
            if msg != 0:
                embed = discord.Embed(title=f'第{num}號有感地震報告', color=color_list[color], url=weburl,
                                      timestamp=datetime.now(timezone(timedelta(hours=+8))))
                embed.add_field(name=msg, value='', inline=False)
                embed.add_field(name='芮氏規模', value=mag, inline=True)
                embed.add_field(name='震央深度', value=depth, inline=True)
                embed.add_field(name='震央位址', value=loc, inline=False)
                embed.set_image(url=image)
                embed.set_footer(text='以上資料由中央氣象署CWA提供')
                await channel.send(embed=embed)
        await asyncio.sleep(1)


bot.run(os.getenv('dctoken'))  # 搖一下
