import discord
from discord.ext import commands
from discord.ui import Button
from discord.ui import View
import pygsheets
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import asyncio
from send import email

gs_url = 'path'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "%", intents = intents)

@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

@bot.event
async def on_message(message):
    if message.content == '幫主早安':
        await message.channel.send('早安你好，操')
    elif message.content == '幫主等等吃啥':
        await message.channel.send('東京')
    elif message.content == '幫主很躁':
        await message.channel.send('操操操操操')
    elif message.content == '幫主兇屁阿':
        await message.channel.send('蛤')

    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    #建立button
    button1 =Button(label="人名",style=discord.ButtonStyle.green)
    button2 =Button(label="小家",style=discord.ButtonStyle.green)
    button3 =Button(label="所有社員",style=discord.ButtonStyle.green)
    # button4 =Button(label="特殊活動",style=discord.ButtonStyle.green)
    
    #寄給輸入人名對應的後端功能
    async def name_callback(interaction):
        #連接google sheet
        gc = pygsheets.authorize(service_file='/path')
        sht = gc.open_by_url(gs_url)
        df = pd.DataFrame(sht[0].get_all_records())
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        await ctx.send("請輸入收件者姓名：")
        recipient_msg = await bot.wait_for("message", check=check, timeout=60)
        names = recipient_msg.content.split()
        for name in names:
            filtered_df = df[df['幹部姓名'] == name]
        if len(filtered_df) > 0:
            emails = [filtered_df['email'].values[0]]
        
        await email(emails=emails,ctx=ctx,bot=bot)

    #寄給所有社員對應的後端功能
    async def all_callback(interaction):
        gc = pygsheets.authorize(service_file='path')
        sht = gc.open_by_url(gs_url)
        df = pd.DataFrame(sht[0].get_all_records())

        emails = df['email'].tolist()
        await email(bot=bot,emails=emails,ctx=ctx)
        
    #寄給小家成員對應的後端功能
    async def home_callback(interaction):
        gc = pygsheets.authorize(service_file='C:/Users/CreamPy/Desktop/dcbot/mitc-system-455c51321ebc.json')
        sht = gc.open_by_url(gs_url)
        df = pd.DataFrame(sht[0].get_all_records())
        
        button1 =Button(label="大白",style=discord.ButtonStyle.green)
        button2 =Button(label="社員專案",style=discord.ButtonStyle.green)
        button3 =Button(label="分享會",style=discord.ButtonStyle.green)

        async def white_callback(interaction):
            emails = (df.loc[df['小家名稱'] == "大白", 'email']).tolist()
            await email(emails=emails,ctx=ctx,bot=bot)

        async def project_callback(interaction):
            emails = (df.loc[df['小家名稱'] == "社員專案", 'email']).tolist()
            await email(emails=emails,ctx=ctx,bot=bot)
    
        async def share_callback(interaction):
            emails = (df.loc[df['小家名稱'] == "分喜會", 'email']).tolist()
            await email(emails=emails,ctx=ctx,bot=bot)

        button1.callback = white_callback
        button2.callback = project_callback
        button3.callback = share_callback    

        view=View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        
        await ctx.send(view = view)
        
    # 特殊活動對應的後端功能
    # async def activity_callback(interaction):
    #     button1 =Button(label="焦點工作坊",style=discord.ButtonStyle.green)
    #     button2 =Button(label="期初大會",style=discord.ButtonStyle.green)
    #     button3 =Button(label="藤林工作坊",style=discord.ButtonStyle.green)
    #     button4 =Button(label="藤林工作坊",style=discord.ButtonStyle.green)

    #     #不同的活動會接到資料庫裡不同的table，再根據資料庫的設計找到email透過email這個函式寄出
    #     async def act1_callback(interaction):
    #         await email(bot=bot,emails=emails,ctx=ctx)
    #     async def act2_callback(interaction):
    #         await email(bot=bot,emails=emails,ctx=ctx)
    #     async def act3_callback(interaction):
    #         await email(bot=bot,emails=emails,ctx=ctx)
    #     async def act4_callback(interaction):
    #         await email(bot=bot,emails=emails,ctx=ctx)

    #     button1.callback = act1_callback
    #     button2.callback = act2_callback
    #     button3.callback = act3_callback
    #     button4.callback = act4_callback

    #     view=View()
    #     view.add_item(button1)
    #     view.add_item(button2)
    #     view.add_item(button3)
    #     view.add_item(button4)
    #     await ctx.send("hi",view=view)
    
    #把上面寫好的功能接到button上
    button1.callback = name_callback
    button2.callback = home_callback
    button3.callback = all_callback
    # button4.callback = activity_callback

    #顯示button
    view=View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    # view.add_item(button4)
    
    await ctx.send("Hi!",view=view)
    
#啟動機器人
bot.run("key")