import discord
import requests
from discord.ext import commands 
import logging 
from dotenv import load_dotenv
import os 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents= intents)

@bot.event
async def on_ready() :
    print(f"ready,{bot.user.name}")
if not token:
    raise SystemExit("DISCORD_TOKEN not set in environment")
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello, {ctx.author.mention}")
@bot.command()
async def weather(ctx):
    API_KEY = "e8f8aa082737265ec61c8e7b296be0ac"
    def get_weather():
        city = entry.get()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=vi"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            result(text="Không tìm thấy thành phố rồi… baka!")
        else:
            tempC = data["main"]["temp"]
            tempK = tempC + 273
            tempF = tempC * 2 + 30
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
        result = (
            f" Thành phố: {city}\n"
            f" Nhiệt độ: {tempC} °C {tempK}°K {tempF} °F \n"
            f" Độ ẩm: {humidity} %\n"
            f" Thời tiết: {desc}"
        )
        
bot.run(token, log_handler=handler, log_level=logging.DEBUG)