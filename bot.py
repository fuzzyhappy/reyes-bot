import discord
import collections

client = discord.Client()

#queue of people who need help
queue = []

@client.event
async def on_message(message):
    global queue

    channel = message.channel
    content = message.content
    author = message.author
    guild = message.guild

    if author == client.user :
        return

    ### code block for handling text commands
    if content.startswith("!"):

        response = ""
        command = content.split(" ")[0]
        # marks the user as needing help
        if command == "!needhelp":
            queue.append(author)
            response += author.name + " is in queue for help."
        # lists queue
        if command == "!queue":
            if len(queue) == 0:
                response += "No one in queue for help!"
            else:
                response += "```md" + "\n"
                for i in range(0, len(queue)):
                    response += "[#" + str(i + 1) + "] <" + queue[i].name + ">\n"
                response += "```"
        if command == "!officeopen":



        if not len(response) > 0:
            response += "That wasn't a recognized command!"
        await channel.send(response)


TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
