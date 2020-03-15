import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description='Classroom helper bot')
students = []

@bot.command()
async def needhelp(ctx):
    if ctx.message.channel.name == "bot":
        author = ctx.author
        if not author in students:
            students.append(author)
            await ctx.send(author.nick + " is now in queue for help.")
        else:
            await ctx.send(author.nick + " is already in the queue for help!")
    else:
        await ctx.send("Please only use bot commands in #bot!")

@bot.command()
async def cancelhelp(ctx):
    if ctx.message.channel.name == "bot":
        author = ctx.author
        if author in students:
            students.remove(author)
            await ctx.send(author.nick + " no longer needs help.")
        else:
            await ctx.send(author.nick + " was not in need of help in the first place!")
    else:
        await ctx.send("Please only use bot commands in #bot!")

@bot.command()
async def queue(ctx):
    if ctx.message.channel.name == "bot":
        if len(students) == 0:
            await ctx.send("There is nobody in the help queue!")
        else:
            embed = discord.Embed(title="Help queue", description="People who currently need help from the teacher.", color = 0xff6a57)
            for i in range(0, len(students)):
                embed.add_field(name = "#" + str(i + 1) + " " + students[i].nick, value = students[i].status)
            await ctx.send(embed = embed)
    else:
        await ctx.send("Please only use bot commands in #bot!")

@bot.command()
async def ready(ctx):
    if ctx.message.channel.name == "bot":
        if discord.utils.get(ctx.guild.roles, name = "teacher") in ctx.author.roles:
            if len(students) > 0:
                await ctx.send(students[0].mention + " come back, " + ctx.author.nick + " is ready to help!")
            else:
                await ctx.send("No one currently needs help!")
        else:
            await ctx.send("You are not authorized to use !ready.")
    else:
        await ctx.send("Please only use bot commands in #bot!")

@bot.command()
async def skip(ctx):
    if ctx.message.channel.name == "bot":
        if discord.utils.get(ctx.guild.roles, name = "teacher") in ctx.author.roles:
            if len(students) == 0:
                await ctx.send("There's nobody in the queue!")
            elif len(students) > 1:
                await ctx.send(students[0].nick + " is now second in the help queue. First in queue is " + students[1].nick + ".")
                students[0], students[1] = students[1], students[0]
            else:
                await ctx.send(students[0].nick + " is the only one in the help queue!")
        else:
            await ctx.send("You are not authorized to use !ready.")
    else:
        await ctx.send("Please only use bot commands in #bot!")

@bot.command()
async def resolve(ctx, target=None):
    if ctx.message.channel.name == "bot":
        if discord.utils.get(ctx.guild.roles, name = "teacher") in ctx.author.roles:
            if target == None:
                if students == 0:
                    await ctx.send("You currently aren't helping anybody.")
                else:
                    await ctx.send(students.pop(0).nick + " had their question answered.")
            else:
                resolved = discord.utils.get(ctx.guild.members, nick = target)
                if resolved in students:
                    await ctx.send(resolved.nick + " had their question answered")
                    students.remove(resolved)
                else:
                    await ctx.send(resolved.nick + "does not need their question answered")
        else:
            await ctx.send("You are not authorized to use !ready.")
    else:
        await ctx.send("Please only use bot commands in #bot!")

@bot.command()
async def clear(ctx):
    if ctx.message.channel.name == "bot":
        if discord.utils.get(ctx.guild.roles, name = "teacher") in ctx.author.roles:
            students.clear()
            await ctx.send("The help queue is cleared.")
        else:
            await ctx.send("You are not authorized to use !ready.")
    else:
        await ctx.send("Please only use bot commands in #bot!")

@bot.command()
async def srccode(ctx):
    await ctx.send("https://github.com/fuzzyhappy/reyes-bot")

@bot.command()
async def setcourse(ctx, role = None):
    if ctx.message.channel.name == "bot":
        if role == None:
            await ctx.send("You did not specify what course you want to be put in!")
        else:
            desiredRole = discord.utils.get(ctx.guild.roles, name = role)
            if desiredRole.name != "moderator" and desiredRole.name != "teacher" and not desiredRole in ctx.author.roles:
                await ctx.author.add_roles(desiredRole)
                await ctx.send("You were successfully put in course " + desiredRole.name + ".")
            elif desiredRole in ctx.author.roles:
                await ctx.send("You are already in " + desiredRole.name + ".")
            else:
                await ctx.send("This bot is not authorized to give out those roles.")
    else:
        await ctx.send("Please only use bot commands in #bot!")

bot.remove_command("help")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="the mover", description="A bot to help with online teaching on Discord during the quarantine.", color=0x389afc)

    embed.add_field(name="**GENERAL COMMANDS:**", value="These commands can be used by anyone.", inline=False)
    embed.add_field(name="!needhelp", value="Add yourself to the students to get help from Mr. Reyes.", inline=False)
    embed.add_field(name="!cancelhelp", value="Remove yourself to the students to get help from Mr. Reyes.", inline=False)
    embed.add_field(name="!queue", value="Get the students of people waiting for help.", inline=False)
    embed.add_field(name="!srccode", value="Responds with a link to my source GitHub repository. Suggest edits if you think they're necessary!", inline=False)
    embed.add_field(name="!setcourse <Course>", value="Allows users to claim that they are in mvc-la, calc-bc, or alg-2-elements for easy identification.", inline=False)

    if (discord.utils.get(ctx.guild.roles, name = "teacher") in ctx.author.roles):
        embed.add_field(name="**TEACHER EXCLUSIVE COMMANDS:**", value="These commands can only be used by teachers.", inline=False)
        embed.add_field(name="!ready", value="Pings the first person in the help students.", inline=False)
        embed.add_field(name="!skip", value="Skips the first person in the help students.", inline=False)
        embed.add_field(name="!resolve <(Optional) Name>", value="Signals that Mr. Reyes has answered their question. If no name is given, the first person in the students is resolved.", inline=False)
        embed.add_field(name="!clear", value="Clears the students of all people who need help. Be careful, this is permanent.", inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    await discord.utils.get(member.guild.text_channels, name = "general").send("Welcome! " + member.mention + " please set your nickname to your real name so we know who you are!")

TOKEN = open("secret").read().rstrip()
bot.run(TOKEN)
