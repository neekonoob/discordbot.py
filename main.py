import threading
import discord
import requests
from discord.ext import commands 
import logging 
from dotenv import load_dotenv
from flask import Flask
import os 
#web server 
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive! 👀"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if not token:
    print("❌ DISCORD_TOKEN is missing")
    SystemExit(1)
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
async def weather(ctx, *, city: str):
    API_KEY = os.getenv("OPENWEATHER_API_KEY") or "e8f8aa082737265ec61c8e7b296be0ac"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=vi"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
    except Exception:
        await ctx.send("Lỗi khi kết nối dịch vụ thời tiết.")
        return

    if resp.status_code != 200 or data.get("cod") != 200:
        await ctx.send("Không tìm thấy thành phố rồi… baka!")
        return

    tempC = data["main"]["temp"]
    tempK = tempC + 273.15
    tempF = tempC * 9/5 + 32
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"]

    result = (
        f"Thành phố: {city}\n"
        f"Nhiệt độ: {tempC} °C / {tempK:.2f} K / {tempF:.2f} °F\n"
        f"Độ ẩm: {humidity}%\n"
        f"Thời tiết: {desc}"
    )
    await ctx.send(result)
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.run(token)
bot.run(token, log_handler=handler, log_level=logging.DEBUG)