import discord

client = discord.Client()

# queue of people who need help
queue = []
# dictionary of commands and their descriptions
commandList = ["!needhelp", "!cancelhelp", "!queue", "!ready", "!srccode", "!setrole <Role>", "!help"]
commandDict = {0: "Add yourself to the queue to get help from Mr. Reyes.",
               1: "Remove yourself from the queue to get help from Mr. Reyes.",
               2: "Get the queue of people waiting for help.",
               3: "Only Mr. Reyes can use this command, it pings and removes the first person in the help queue.",
               4: "Responds with a link to my source GitHub repository. Suggest edits if you think they're necessary!",
               5: "CURRENTLY UNUSABLE", # Allows users to claim that they are in mvc-la, calc-bc, or alg-2-elements for easy identification.
               6: "Lists recognized commands."}

@client.event
async def on_message(message):

    channel = message.channel
    content = message.content
    author = message.author
    guild = message.guild

    if author == client.user :
        return

    ### code block for handling text commands
    if content.startswith("!") and channel.name == "bot":
        global queue

        response = ""
        command = content.split(" ")[0]

        # marks the user as needing help
        if command == "!needhelp":
            if not author in queue:
                queue.append(author)
                response += author.nick + " is in queue for help."
            else:
                response += author.nick + " is already in queue for help."

        # unmarks the user as needing help
        if command == "!cancelhelp":
            if author in queue:
                queue.remove(author)
                response += author.nick + " is no longer in need of help."
            else:
                response += author.nick + "was not in the queue."

        # lists queue
        if command == "!queue":
            if len(queue) == 0:
                response += "No one in queue for help!"
            else:
                response += "```md\n"
                for i in range(0, len(queue)):
                    response += "[#" + str(i + 1) + "] <" + queue[i].nick + ">\n"
                response += "```"

        # ready
        if command == "!ready":
            if discord.utils.get(message.guild.roles, name = "teacher") in author.roles:
                if len(queue) > 0:
                    response += queue.pop(0).mention + " come back, Mr. Reyes is ready to help!"
                else:
                    response += "No one currently needs help!"
            else:
                response += "You are not authorized to use !ready."

        # src code
        if command == "!srccode":
            response += "https://github.com/fuzzyhappy/reyes-bot"

        # allows students to set their role
        if command == "!setrole":
            if len(content.split(" ")) >= 2:
                desiredRole = content.split(" ")[1]
                if desiredRole != "moderator" and desiredRole != "teacher":
                    await author.add_roles(discord.utils.get(author.guild.roles, name = desiredRole))
                    response += "You were successfully given the role " + desiredRole + "."
                elif desiredRole == "moderator" or desiredRole == "teacher":
                    response += "You are not authorized to request that role from this bot."
                else:
                    response += "Role not found, check for spelling mistakes, the only roles offered are mvc-la, calc-bc, and alg-2-elements."
            else:
                response += "You did not specify what role you wanted! The format for !setrole is !setrole <Role Name (case sensitive)>."

        # lists commands
        if command == "!help":
            response += "```md\n"
            for i in range(0, len(commandList)):
                response += commandList[i] + ":\n\t" + commandDict[i] + "\n"
            response += "```"

        # case where command wasn't recognized
        if len(response) == 0:
            response += "That wasn't a recognized command! Try !help to get the list of recognized commands!"
        await channel.send(response)

    elif content.startswith("!") and channel.name != "bot":
        await channel.send(author.nick + ", you're not allowed to use bot commands outside of #bot!")

@client.event
async def on_member_join(member):
    await discord.utils.get(member.guild.text_channels, id = 687446137887653892).send("Welcome! " + member.mention + " please set your nickname to your real name so we know who you are!")

TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
