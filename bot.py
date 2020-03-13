import discord
import collections
import enum

client = discord.Client()

# queue of people who need help
queue = []
# dictionary of commands and their descriptions
commandList = ["!needhelp", "!cancelhelp", "!queue", "!ready", "!srccode", "!help"]
commandDict = {0: "Add yourself to the queue to get help from Mr. Reyes.",
               1: "Remove yourself from the queue to get help from Mr. Reyes.",
               2: "Get the queue of people waiting for help.",
               3: "Only Mr. Reyes can use this command and it pings the first person in the help queue.",
               4: "Responds with a link to my source GitHub repository. Suggest edits to Evan if you think they're necessary!",
               5: "Lists recognized commands."}

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
        if command == "!cancelhelp" and author in queue:
            queue.remove(author)
            response += author.nick + " is no longer in need of help."
        # lists queue
        if command == "!queue":
            if len(queue) == 0:
                response += "No one in queue for help!"
            else:
                response += "```md\n"
                for i in range(0, len(queue)):
                    response += "[#" + str(i + 1) + "] <" + queue[i].nick + ">\n"
                response += "```"
        if command == "!ready" and author.nick == "Mr. Reyes":
            response += "Mr. Reyes is ready to help students! " + queue.pop(0).mention + " come back, Mr. Reyes is ready to help!"
        if command == "!srccode":
            reponse += "https://github.com/fuzzyhappy/reyes-bot"

        if command == "!help":
            response += "```md\n"
            for i in range(0, len(commandList)):
                response += commandList[i] + ":\n\t" + commandDict[i] + "\n"
            response += "```"


        if not command in commandList:
            response += "That wasn't a recognized command! Try !help to get the list of recognized commands!"
        await channel.send(response)
    elif content.startswith("!") and channel.name != "bot":
        await channel.send(author.nick + ", you're not allowed to use bot commands outside of #bot!")

#@bot.event
#async def on_member_join(member):
    #await

TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
