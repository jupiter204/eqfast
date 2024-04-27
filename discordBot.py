import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
import eqfast
import eqreport

load_dotenv()
bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())
color_list = {'綠色': discord.Color.green(), '黃色': discord.Color.gold(),
              '橙色': discord.Color.orange(), '紅色': discord.Color.red()}


@bot.event
async def on_ready():
    global channel, time, num
    channel = bot.get_channel(988075823871434848)
    time = eqfast.init()
    num = eqreport.init()
    print(f'{bot.user} ready on!!!')
    fast.start()
    report.start()


@tasks.loop(seconds=1)
async def fast():
    timestr = datetime.now(timezone(timedelta(hours=+8)))
    global time
    time, msg, area = eqfast.update(time)
    print('fast check')
    if msg != 0:
        print(f'{timestr}\tfast:第{time}號地震警報')
        await channel.send(f'{msg}\n{area}')


@tasks.loop(seconds=30)
async def report():
    timestr = datetime.now(timezone(timedelta(hours=+8)))
    global num
    num, color, msg, image, weburl, depth, loc, mag = eqreport.get(num)
    print('report check')
    if msg != 0:
        print(f'{timestr}\treport:第{num}號有感地震報告')
        embed = discord.Embed(title=f'第{num}號有感地震報告', color=color_list[color], url=weburl,
                              timestamp=timestr)
        embed.add_field(name=msg, value='', inline=False)
        embed.add_field(name='芮氏規模', value=mag, inline=True)
        embed.add_field(name='震央深度', value=depth, inline=True)
        embed.add_field(name='震央位址', value=loc, inline=False)
        embed.set_image(url=image)
        embed.set_footer(text='以上資料由中央氣象署CWA提供')
        await channel.send(embed=embed)


bot.run(os.getenv('dctoken'))  # 搖一下
