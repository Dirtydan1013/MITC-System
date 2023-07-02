import discord
from discord.ext import commands
import pygsheets
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import asyncio

gs_url = 'gs_url'

# 連接discord bot
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

#機收信件資訊
@bot.command()
async def 我要寄信(ctx):
    #連接google sheet
    gc = pygsheets.authorize(service_file='/path')
    sht = gc.open_by_url(gs_url)
    df = pd.DataFrame(sht[0].get_all_records())

    #開始接收
    await ctx.send("了解，操")
    await ctx.send("請輸入郵件標題，操：")

    
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        title_msg = await bot.wait_for("message", check=check, timeout=60)
        title = title_msg.content
 
        await ctx.send("請輸入郵件內容，操：")
        content_msg = await bot.wait_for("message", check=check, timeout=60)
        detail = content_msg.content

        await ctx.send("請輸入收件者姓名，操：")
        recipient_msg = await bot.wait_for("message", check=check, timeout=60)
        if recipient_msg.content == "所有幹部":
            emails = df['email'].tolist()
        else:
          names = recipient_msg.content.split()
          for name in names:
           filtered_df = df[df['幹部姓名'] == name]
           if len(filtered_df) > 0:
            emails = [filtered_df['email'].values[0]]
            print(emails)

        # 在這裡將輸入的資訊傳送到後端執行相關操作
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = title #郵件標題
        content["from"] = "example@gmail.com"  #寄件者
        content.attach(MIMEText(detail))  #郵件內容

        #寄信
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("example@gmail.com", "gmail_key")  # 登入寄件者gmail
                for email in emails:
                  content["to"] = email #一個一個寄
                  smtp.send_message(content)  # 寄送郵件
                print("Complete!")

            except Exception as e:
                print("Error message: ", e)
                
        await ctx.send("郵件資訊已收到，將進行後續處理，操。")

    except asyncio.TimeoutError:
        await ctx.send("輸入超時，請重新嘗試，操。")


bot.run("discord_key")