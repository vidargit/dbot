import nextcord
from nextcord.ext import commands, tasks


token = 'OTIzNDE1MDU4MTYyMjgyNTU2.YcPrSg.mU2CzF2H8YqDTe6UF4MPdjNtMDU'
#https://discord.com/api/oauth2/authorize?client_id=923415058162282556&permissions=8&scope=bot

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='v/', intents=intents)

bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game('Commands: v/'))
	print(f"logged in {bot.user}")

@bot.event
async def on_message(message):
	try:
		if message.content.startswith('v/cls'):
			if message.author.guild_permissions.manage_messages:
				await message.delete()
				_, limit = message.content.split()
				await message.channel.purge(limit=int(limit))
			else:
				await message.channel.send("PermissionError (You can't use this command)")
			await bot.process_commands(message)
		elif str(message.channel.id) in {"922734690157338624", "922759065124368414"}:
			if message.author != bot.user:
				embed = nextcord.Embed(description=f"""This is a place to answer {message.author.mention} questions.
		
{message.author.mention} has a question...
It says {message.content}!""", color=0xff9d00)
				embed.set_footer(text="If you open the thread as a joke, be careful as you may be punished.")
				thread = await message.channel.create_thread(name=f"Q of {message.author.name}", type=nextcord.ChannelType.public_thread)
				await thread.send(embed=embed)
		else:
			pass
	except AttributeError:
		message.channel.send("ThreadError (Something wrong while making thread)")
	await bot.process_commands(message)


@bot.command(name="user")
async def userinfo(ctx, member: nextcord.Member = None):
	if not member:
		member = ctx.message.author
	embed = nextcord.Embed(colour=nextcord.Colour.purple(),timestamp=ctx.message.created_at,
			title=f"{member}의 정보")
	roles = [role.mention for role in member.roles[1:]]
	embed.set_thumbnail(url=member.avatar.url)
	embed.set_footer(text=f"{ctx.author} used the command")
	embed.add_field(name="Name:", value=member.mention)
	embed.add_field(name="ID:", value=member.id)
	embed.add_field(name="NickName:", value=member.display_name)
	embed.add_field(name="Account Creation Time:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	embed.add_field(name="Server Entry Time:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
	embed.add_field(name="Roles:", value="".join(roles))
	embed.add_field(name="Top-Level Role:", value=member.top_role.mention)
	embed.add_field(name="Is Bot:", value=member.bot)
	await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
	embed = nextcord.Embed(title=f'''Pong! {round (bot.latency * 1000)} ms''')
	await ctx.send(embed=embed)

@bot.command(name="help")
async def help(ctx, option=None):
	if option:
		if option == 'vidar':
			embed = nextcord.Embed(title="Vidar", description="""
It is made with 'Python'.
But It has been developed yet.""")
			await ctx.send(embed=embed)

		else:
			embed = nextcord.Embed(title="Command Not Found", description=f"""
We don't have solution about "{option}" yet.
Sorry.""")
			await ctx.send(embed=embed)

	else:
		embed = nextcord.Embed(title="""Usage : v/help <argument>""")
		await ctx.send(embed=embed)

bot.run(token)