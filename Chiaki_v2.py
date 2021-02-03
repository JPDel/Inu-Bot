import discord
import discord.utils
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import datetime
#from datetime import datetime

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
	print('Wan! My name is {0.user}'.format(client))

@client.command()
async def foo(ctx, arg):
	await ctx.send(arg)

@client.command()
async def sf(ctx):
	await ctx.send("It's Simmons' fault :rolling_eyes:")

@client.command()
async def roll(ctx, arg):
	returnString = ""
	dice = arg.split("d")
	for i in range(len(dice)):
		dice[i] = (int)(dice[i])

	for x in range(dice[0]):
		roll = random.randint(1, dice[1])
		returnString = returnString + str(roll)+", "
	returnString = returnString[:-2]
	await ctx.send(returnString)

@client.command()
async def uprising(ctx): # Counts days/hours/mins since last KFC uprising
	uprising = open("uprising.txt", "r")
	dateandtime = uprising.readline().split('T')
	uprising.close()

	uprisingtime = dateandtime[1].split(':')
	uprisingdate = dateandtime[0].split('-')

	uprisingdate = datetime.datetime(int(uprisingdate[0]), int(uprisingdate[1]), int(uprisingdate[2]))
	uprisingtime = datetime.time(int(uprisingtime[0]), int(uprisingtime[1]))

	newuprisingdate = datetime.datetime.combine(uprisingdate.date(), uprisingtime)

	now = datetime.datetime.now()
	diff = now -  newuprisingdate

	returnsplit = str(diff).split(", ")
	returnstring = ''
	if len(returnsplit) == 1:
		returntime = returnsplit[0].split(':')
		returnstring = "It has been 0 days, " + returntime[0] + " hours, and " + returntime[1] + " minutes since the last KFC uprising"
		await ctx.send(returnstring)
		await ctx.send("Gamers rise up!")
	else:
		returntime = returnsplit[1].split(':')
		returnstring = "It has been " + returnsplit[0] + ", " + returntime[0] + " hours, and " + returntime[1] + " minutes since the last KFC uprising"
		await ctx.send(returnstring)


@client.command()
async def uprisingupdate(ctx, arg):
	await ctx.send('arg must be "date in iso format i.e. 2020-10-14"+space+"time i.e. 22:45"')
	uprising = open("uprising.txt", "w")
	dateandtime = arg.split(' ')
	uprisingdate = dateandtime[0].split('-')
	uprisingtime = dateandtime[1].split(':')
	uprisingdate = datetime.datetime(int(uprisingdate[0]), int(uprisingdate[1]), int(uprisingdate[2]))
	uprisingtime = datetime.time(int(uprisingtime[0]), int(uprisingtime[1]))
	newuprisingdate = datetime.datetime.combine(uprisingdate.date(), uprisingtime)
	uprising.write(newuprisingdate.isoformat())
	uprising.close()


@client.command()
async def role(ctx, *, role: discord.Role):
	user = ctx.message.author

	alumni = discord.utils.get(ctx.guild.roles, name="alumni") #Same as ctx.guild.get_role(role_id)
	curr_mem = discord.utils.get(ctx.guild.roles, name="members")
	design = discord.utils.get(ctx.guild.roles, name="design")
	programming = discord.utils.get(ctx.guild.roles, name="programming")
	art = discord.utils.get(ctx.guild.roles, name="art")
	sound = discord.utils.get(ctx.guild.roles, name="sound")

	team_roles = [design, programming, art, sound]

	if role not in team_roles:
		await ctx.send("Please only attempt to add a team role to yourself")
		return

	if alumni not in user.roles:
		for i in team_roles:
			if i in user.roles:
				await user.remove_roles(i)

		await user.add_roles(role)
		await user.add_roles(curr_mem)

	else:
		await ctx.send("You've already been set as an alumni. If this is a mistake, please contact an officer.")

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	# Compliments tracks
	if message.content.startswith('https://soundcloud.com') or message.content.startswith('soundcloud.com'):
		await asyncio.sleep(15)
		await message.channel.send("That's a banger")

	await client.process_commands(message)

client.run('Insert token here')
