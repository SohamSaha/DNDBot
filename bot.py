import discord
import os
from discord.ext import commands
from datetime import datetime
from datetime import date
from discord.ext.tasks import loop
import desired_date as desired

bot = commands.Bot(command_prefix='d.')

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.command()
async def request(ctx, date, time):
    desired.REQUESTED_TIME = time
    desired.REQUESTED_DATE = date

@bot.command()
async def test(ctx):
    now = datetime.now()
    today = date.today()
    current_time = now.strftime("%H:%M")
    current_date = today.strftime("%m/%d/%y")
    print (current_date)
    print(current_time)
  

@loop(count=None, seconds=1)  #Will run forever every second
async def check_calendar():

  #Get the date and time from the Heroku system and format it appropriately
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  current_date = date.today()
  

check_calendar.start()
bot.run(os.environ['DND_API_KEY'])