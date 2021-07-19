import discord
import os
import match
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

class Main:
    reactionMessageId = 0
    reactionChannelId = 0
    reactionEmote = "🥏"

@client.event
async def on_ready():   
    channel = client.get_channel(865882258636406804)
    await channel.purge(limit=100)

    channel = client.get_channel(865882224553623552)
    await channel.purge(limit=100)

    channel = client.get_channel(865593981164847115)
    await channel.purge(limit=1)

    print('We have logged in as {0.user}'.format(client))
    
    message = await channel.send("React to me!")
    await message.add_reaction(Main.reactionEmote)

    Main.reactionMessageId = message.id
    Main.reactionChannelId = channel.id
    
    match.ready()

    queue_to_match.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!match' and message.channel.id == match.MatchStat.queueChannelId:
        await match.queue(client, message)

    if message.content == '!unmatch' and message.channel.id == match.MatchStat.queueChannelId:
        await match.unqueue(client, message)
    
    if message.content.startswith('!char ') and isinstance(message.channel, discord.channel.DMChannel):
        await match.validateChar(client, message)

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    await replace_role(payload, True)
    matchFound = await match.getValidMatch(payload)
    if matchFound is None:
        return

    if matchFound.status != match.MatchStatus.END and matchFound.forfeitMessage == payload.message_id and (payload.emoji.name == "🤝" or payload.emoji.name == "🏳️"):
        await match.tieOrForfeit(client, payload, matchFound)
    elif matchFound.chooser == payload.user_id and matchFound.message == payload.message_id:
        if matchFound.status == match.MatchStatus.STRIKING:
            await match.stageStriking(client, payload, matchFound)
        elif matchFound.status == match.MatchStatus.PLAYING:
            await match.victoryDecision(client, payload, matchFound)
        elif matchFound.status == match.MatchStatus.RESULTS:
            await match.victoryConfirm(client, payload, matchFound)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == client.user.id:
        return
    await replace_role(payload, False)

@tasks.loop(seconds=10)
async def queue_to_match():
    await match.searchForMatch(client)

async def replace_role(payload, flag):
    if payload.channel_id != Main.reactionChannelId or payload.message_id != Main.reactionMessageId:       
        return
    if payload.emoji.name == Main.reactionEmote:
        guild = await client.fetch_guild(payload.guild_id)
        role = await match.getRankingRole(guild)
        user = await guild.fetch_member(payload.user_id)
        if flag:
            await user.add_roles(role)
        else:
            await user.remove_roles(role)


x = os.getenv('TOKEN')
if x is None:
    x = ''

client.run(x)
