# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands

# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
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
    
bot.run("discord_key")