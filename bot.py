import discord
import os
import pytz
import mongo as mong
from pytz import timezone
from discord.ext import commands
from datetime import datetime, date, timedelta
from discord.ext.tasks import loop


bot = commands.Bot(command_prefix='.')
channel = bot.get_channel(os.environ['DND_CHANNEL'])

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.remove_command("help")
@bot.command(pass_context=True)
async def help(ctx):
    await ctx.send('You just put a date and time in the format of mm/dd/YYYY HH:mm')

@bot.command()
async def request(ctx, date, time):
    mong.update_record('Desired Time', 'component' , 'requested_date', 'value', date)
    mong.update_record('Desired Time', 'component' , 'requested_time', 'value', time)

@loop(count=None, seconds=60)
async def check_calendar():
    #Get the values of the desired date and time from the database
    db_date = mong.get_value('Desired Time', 'component', 'requested_date', 'value')
    db_time = mong.get_value('Desired Time', 'component', 'requested_time', 'value')
    #Get the values from the dictionary
    formatted_date = db_date['value']
    formatted_time = db_time['value']
    #Compile the date and time into a date and time object for manipulation
    date_time_compiled = str(formatted_date) + ' ' + str(formatted_time)
    date_time_obj = datetime.strptime(date_time_compiled, '%m/%d/%Y %H:%M') 
    #Strip and format the date and time for manipulation
    db_date_stripped = date_time_obj.date()
    db_time_stripped = date_time_obj.time()
    db_date_stripped_formatted = db_date_stripped.strftime("%m/%d/%Y")
    db_time_stripped_formatted = db_time_stripped.strftime("%H:%M")
    #Check to see the date before the desired date
    yesterday_check = db_date_stripped - timedelta(days = 1)
    yesterday_check_formatted = yesterday_check.strftime("%m/%d/%Y")
    #Check to see if one hour before desired time
    hour_left_check = date_time_obj - timedelta(hours = 1)
    hour_left_check_time = hour_left_check.time()
    hour_left_check_time_formatted = hour_left_check_time.strftime("%H:%M")
    #Get today's date and time and format them
    now = datetime.now()
    today = date.today()    
    current_time = now.astimezone(timezone('US/Pacific')).strftime("%H:%M")
    current_date = today.strftime("%m/%d/%Y")
    
    #If there are exactly 24 hours left (1 day before) then remind everybody
    if  (current_date == yesterday_check_formatted):
        if (current_time == db_time_stripped_formatted):
            await channel.send(mong.get_campaign_users() + ' there are 24 hours left before the next sesion')
    #If it is the current date, remind people one hour before and when it starts
    elif (current_date == db_date_stripped_formatted):
        if (current_time == db_time_stripped_formatted):
            await channel.send(mong.get_campaign_users() + ' It is time for the next session')
        elif (current_time == hour_left_check_time_formatted) :
            await channel.send(mong.get_campaign_users() + ' 1 hour left before the next session')

@check_calendar.before_loop
async def before_check_calendar():
    await bot.wait_until_ready()  # Wait until bot is ready

check_calendar.start()
bot.run(os.environ['DND_API_KEY'])