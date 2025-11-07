import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import csv
import random
import requests
import webserver
import cronitor

load_dotenv()

# scientific_name,common_name,meaning,diet,length_m,weight_kg,height_m,locomotion,geological_period,lived_in,behavior_notes,first_discovered,fossil_location,notable_features,intelligence_level,source_link,row_index
DINO_DATA = []

# IMPORT DINO DATA
with open('./data/dino_facts.csv', 'r', newline='') as dinoDataFile:
	reader = csv.reader(dinoDataFile)
	for row in reader:
		DINO_DATA.append(row)

# DISCORD BOT
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='dino_bot.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# init bot
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# HEARTBEAT
key = os.getenv('CRON_API_KEY')
heartbeat_id = os.getenv('HEARTBEAT_KEY')

cronitor.api_key = key
monitor = cronitor.Monitor(heartbeat_id)

CRON_HEARTBEAT_URL = f"https://cronitor.link/p/{key}/{heartbeat_id}"

@tasks.loop(minutes=5)
async def send_heartbeat():
	try:
		monitor.ping(message="Bot refreshed for updates or restarted.")
		requests.get(CRON_HEARTBEAT_URL)
		print(f"Bot health check background job sent successfully.")
	except Exception as e:
		print(f"Failed to send heartbeat: {e}")
# HANDLING EVENTS

# on ready
@bot.event
async def on_ready():
	webserver.keep_alive()

	if not send_heartbeat.is_running():
		send_heartbeat.start()
	
	print(f'Bot is running {bot.user}')


# member join
@bot.event
async def on_member_join(member):
	await member.send(f'Welcome to the server, {member.mention}! I can\'t wait to share some epic awesome dino facts with you! 🦖')

# message
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

# COMMANDS
@bot.command()
async def dino(ctx):
	dino = random.randint(1, len(DINO_DATA) - 1)

	dino_science_name = DINO_DATA[dino][0]
	dino_common_name = DINO_DATA[dino][1]
	dino_meaning = DINO_DATA[dino][2]
	dino_diet = DINO_DATA[dino][3]
	dino_length = DINO_DATA[dino][4]
	dino_weight = DINO_DATA[dino][5]
	dino_height = DINO_DATA[dino][6]
	dino_locomotion = DINO_DATA[dino][7]
	dino_geological_period = DINO_DATA[dino][8]
	dino_lived_in = DINO_DATA[dino][9]
	dino_behavior_notes = DINO_DATA[dino][10]
	dino_first_discovered = DINO_DATA[dino][11]
	dino_fossil_location = DINO_DATA[dino][12]
	dino_notable_features = DINO_DATA[dino][13]
	dino_intelligence_level = DINO_DATA[dino][14]
	dino_source_link = DINO_DATA[dino][15]
	dino_eats = ""
	dino_moves = ""

	if dino_diet == "Carnivore":
		dino_eats = "meat"
	elif dino_diet == "Herbivore":
		dino_eats = "plants"
	else:
		dino_eats = "both meat and plants"

	if dino_locomotion == "Bipedal":
		dino_moves = "walking on two legs 🚶‍♂️"
	else:
		dino_moves = "walking on four legs 🦵🦵🦵🦵"

	message = f'''RANDOM DINO FACT!!!

You got a {dino_common_name} (scientific name: {dino_science_name})! 🦖
{dino_common_name} got its name beacuse of the following (non descriptive) peice of information that I found: {dino_meaning.lower()}

{dino_common_name} is a {dino_diet.lower()}. That means {dino_common_name} likes to eat {dino_eats}.

{dino_common_name} is about {dino_length} meters long, and weighs around {dino_weight} kilograms. It stands about {dino_height} meters tall.

{dino_common_name} is {dino_locomotion.lower()}. That means {dino_common_name} gets around by {dino_moves}.

{dino_common_name} lived during the {dino_geological_period} period, in what is now {dino_lived_in}.
The {dino_common_name} is known for the following non descriptive fact: {dino_notable_features.lower()}.
Some interesting behavior notes about the {dino_common_name} are as follows: {dino_behavior_notes.lower()}.

{dino_common_name} was first discovered in {dino_first_discovered}, with fossils found in {dino_fossil_location}.
{dino_common_name} has an intelligence rating of: {dino_intelligence_level.lower()}.

For more information about {dino_common_name}, check out its wikipedia here: {dino_source_link}'''

	await ctx.send(f"{message}")



@bot.command()
async def draven(ctx):
	message = '''
RANDOM DRAVEN FACT!!!

I am always nearby

I hunt when you aren't looking

I'm behind you

I'm behind you

I'm behind you

I'm behind you

I'm behind you

I'm behind you

I'm behind you

For more information turn around!!! 😈
'''
	await ctx.send(f"{message}")

# run bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
