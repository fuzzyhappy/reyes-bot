import discord

client = discord.Client()

# queue of people who need help
queue = []
# dictionary of commands and their descriptions
commandList = ["!needhelp", "!cancelhelp", "!queue", "!srccode", "!setcourse <Course>", "!help"]
teacherCommands = ["!ready", "!skip", "!resolve <(optional) Name>", "!clear"]
commandDict = {0: "Add yourself to the queue to get help from Mr. Reyes.",
               1: "Remove yourself from the queue to get help from Mr. Reyes.",
               2: "Get the queue of people waiting for help.",
               3: "Responds with a link to my source GitHub repository. Suggest edits if you think they're necessary!",
               4: "Allows users to claim that they are in mvc-la, calc-bc, or alg-2-elements for easy identification.",
               5: "Lists recognized commands."}
teachCommandDict = {0: "Pings the first person in the help queue.",
                    1: "Skips the first person in the help queue.",
                    2: "Signals that Mr. Reyes has answered their question.\n\t* If no name is given, the first person in the queue is resolved.",
                    3: "Clears the queue of all people who need help. Be careful, this is permanent."}

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
                response += "```css\n"
                for i in range(0, len(queue)):
                    response += "[#" + str(i + 1) + "] <" + queue[i].nick + ">\n"
                response += "```"

        # ready
        if command == "!ready":
            if discord.utils.get(message.guild.roles, name = "teacher") in author.roles:
                if len(queue) > 0:
                    response += queue[0].mention + " come back, Mr. Reyes is ready to help!"
                else:
                    response += "No one currently needs help!"
            else:
                response += "You are not authorized to use !ready."

        if command == "!skip":
            if discord.utils.get(message.guild.roles, name = "teacher") in author.roles:
                if len(queue) == 0:
                    response += "There's nobody in the queue!"
                elif len(queue) > 1:
                    response += queue[0].nick + " is now second in the help queue. First in queue is " + queue[1].nick + "."
                    queue[0], queue[1] = queue[1], queue[0]
                else:
                    response += queue[0].nick + " is the only one in the help queue!"
            else:
                response += "You are not authorized to use !skip."

        if command == "!resolve":
            if discord.utils.get(message.guild.roles, name = "teacher") in author.roles:
                if len(queue) > 0:
                    contentSplit = content.split(" ")
                    if len(contentSplit) > 1:
                        target = discord.utils.get(message.guild.members, nick = contentSplit[1])
                        if target in queue:
                            queue.remove(target)
                            response += target.nick + " had their question answered."
                        else:
                            response += target.nick + " is not in the help queue."
                    else:
                        response += queue.pop(0).nick + " had their question answered."
                else:
                    response += "You aren't helping anybody currently."

            else:
                response += "You are not authorized to use !resolve."

        if command == "!clear":
            if discord.utils.get(message.guild.roles, name = "teacher") in author.roles:
                if len(queue) > 0:
                    queue.clear()
                    response += "You have cleared the queue."
                else:
                    response += "Nobody is in the help queue currently."
            else:
                response += "You are not authorized to use !clear."

        # src code
        if command == "!srccode":
            response += "https://github.com/fuzzyhappy/reyes-bot"

        # allows students to set their role
        if command == "!setcourse":
            if len(content.split(" ")) >= 2:
                desiredRole = content.split(" ")[1]
                if desiredRole != "moderator" and desiredRole != "teacher" and discord.utils.get(message.guild.roles, name = desiredRole) in message.guild.roles:
                    if not discord.utils.get(message.guild.roles, name = desiredRole) in author.roles:
                        await author.add_roles(discord.utils.get(author.guild.roles, name = desiredRole))
                        response += "You were successfully given the role " + desiredRole + "."
                    else:
                        response += "You already are in the course " + desiredRole + "."
                elif desiredRole == "moderator" or desiredRole == "teacher":
                    response += "You are not authorized to request that role from this bot."
                else:
                    response += "Role not found, check for spelling mistakes, the only courses offered are mvc-la, calc-bc, and alg-2-elements."
            else:
                response += "You did not specify what course you wanted! The format for !setcourse is !setcourse <Course Name (case sensitive)>."

        # lists commands
        if command == "!help":
            response += "```css\n"
            response += "[GENERAL COMMANDS]\n"
            for i in range(0, len(commandList)):
                response += commandList[i] + ":\n\t* " + commandDict[i] + "\n"
            if discord.utils.get(message.guild.roles, name = "teacher") in author.roles:
                response += "[TEACHER COMMANDS]\n"
                for i in range(0, len(teacherCommands)):
                    response += teacherCommands[i] + ":\n\t* " + teachCommandDict[i] + "\n"
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
