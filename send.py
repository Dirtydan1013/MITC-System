from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import asyncio

async def email(bot,ctx,emails):
        #開始接收
        await ctx.send("請輸入郵件標題：")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            title_msg = await bot.wait_for("message", check=check, timeout=60)
            title = title_msg.content
    
            await ctx.send("請輸入郵件內容：")
            content_msg = await bot.wait_for("message", check=check, timeout=60)
            detail = content_msg.content

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
                    smtp.login("example@gmail.com", "aailwwzfjgjmdqdr")  # 登入寄件者gmail
                    for email in emails:
                        content["to"] = email #一個一個寄
                    smtp.send_message(content)  # 寄送郵件
                    print("Complete!")

                except Exception as e:
                    print("Error message: ", e)

            await ctx.send("郵件資訊已收到，將進行後續處理。")

        except asyncio.TimeoutError:
            await ctx.send("超時囉你這小王八蛋")