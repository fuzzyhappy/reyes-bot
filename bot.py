import discord

client = discord.Client()


@client.event
async def on_message(message):

    channel = message.channel
    content = message.content
    author = message.author
    guild = message.guild

    if author == client.user :
        return

    await channel.send("DETECTED MESSAGE")


TOKEN = open("secret").read().rstrip()
client.run(TOKEN)
