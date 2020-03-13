import discord
import collections

client = discord.Client()

# queue of people who need help
queue = []
# dictionary of commands and their descriptions
commandList = ["!needhelp", "!cancelhelp", "!queue", "!help"]
commandDict = {0: "Add yourself to the queue to get help from Mr. Reyes.",
               1: "Remove yourself from the queue to get help from Mr. Reyes.",
               2: "Get the queue of people waiting for help.",
               3: "Lists recognized commands."}

@client.event
async def on_message(message):

    channel = message.channel
    content = message.content
    author = message.author
    guild = message.guild

    if author == client.user :
        return

    ### code block for handling text commands
    if content.startswith("!"):
        global queue

        response = ""
        command = content.split(" ")[0]
        # marks the user as needing help
        if command == "!needhelp" and not author in queue:
            if not author in queue:
                queue.append(author)
                response += author.name + " is in queue for help."
            else:
                response += author.name + " is already in queue for help."
        if command == "!cancelhelp" and author in queue:
            queue.remove(author)
            response += author.name + " is no longer in need of help."
        # lists queue
        if command == "!queue":
            if len(queue) == 0:
                response += "No one in queue for help!"
            else:
                response += "```md\n"
                for i in range(0, len(queue)):
                    response += "[#" + str(i + 1) + "] <" + queue[i].name + ">\n"
                response += "```"
        #if command == "!ready" and author.roles:
        if command == "!help":
            response += "```md\n"
            for i in range(0, len(commandList)):
                response += commandList[i] + ":\n\t" + commandDict[i] + "\n"
            response += "```"

        if not len(response) > 0:
            response += "That wasn't a recognized command! Try !help to get the list of recognized commands!"
        await channel.send(response)


TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
