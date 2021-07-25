import discord
import os
import match
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

adminUserCommands = ["!adminusercancelset", 
"!adminuserincrementscore", 
"!adminuserdqplayer", 
"!adminuserresetset", 
"!adminuserresetmatch", 
"!adminuserremovefromqueue"]

adminChannelCommands = ["!adminchannelsetqueue", 
"!adminchannelsetmatch",
"!adminchannelsetflair"]

adminTextCommands = ["!adminconfigclearqueue",
"!adminconfigsetdsr",
"!adminconfigsetmdsr",
"!adminconfigsettsr",
"!adminconfigsetnodsr",
"!adminconfigsetmultimatchchannel",
"!adminconfigsetsinglematchchannel",
"!adminconfigsetbancount",
"!adminconfigaddstarter",
"!adminconfigremovestarter"
"!adminconfigaddcp",
"!adminconfigremovecp",
"!adminconfigaddstaffrole",
"!adminconfigremovestaffrole",
"!adminconfigsetrankingrole",
"!adminconfigsendflairmessage",
"!adminconfigsetflairmessage"]

adminInitServer = "!admininitserver"
adminHelp = "!adminhelp"

adminCommands = adminUserCommands + adminChannelCommands + adminTextCommands

@client.event
async def on_ready():   
    # QA PURGE
    channel = client.get_channel(867109176152162324)
    await channel.purge(limit=100)
    
    channel = client.get_channel(867109161212706826)
    await channel.purge(limit=100)

    channel = client.get_channel(867109141134573609)
    await channel.purge(limit=100)

    channel = client.get_channel(867109072108912652)
    await channel.purge(limit=1)

    # DEV PURGE

    channel = client.get_channel(867024058175979550)
    await channel.purge(limit=100)
    
    channel = client.get_channel(865882258636406804)
    await channel.purge(limit=100)

    channel = client.get_channel(865882224553623552)
    await channel.purge(limit=100)

    channel = client.get_channel(865593981164847115)
    await channel.purge(limit=1)

    print('We have logged in as {0.user}'.format(client))
    
    message = await channel.send("React to me! \nUse our commands that you can find by typing \"!matchhelp\"")
    await message.add_reaction("🥏")
    
    match.ready(863389639901052969, message.id)

    queue_to_match.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!char') and isinstance(message.channel, discord.channel.DMChannel):
        await match.validateChar(client, message)
    elif not isinstance(message.channel, discord.channel.DMChannel):
        adminChannelId = match.GuildSettings.getAdminChannelId(message.guild.id)
        queueChannelId = match.GuildSettings.getQueueChannelId(message.guild.id)

        if message.content == '!match' and queueChannelId != 0 and message.channel.id == queueChannelId:
            await match.queue(client, message)

        if message.content == '!unmatch' and queueChannelId != 0 and message.channel.id == queueChannelId:
            await match.unqueue(client, message)

        if message.content == "!matchhelp" and queueChannelId != 0 and message.channel.id == queueChannelId:
            print("HELP!")

        # ADMIN Commands

        if message.content.startswith('!admin'):
            guild = client.get_guild(message.guild.id)
            roles = match.getAdminRankingRoles(client, message.guild.id)
            user = await guild.fetch_member(message.author.id)
            flag = False
            if roles and user.roles:
                for userRole in user.roles:
                    if userRole in roles:
                        flag = True
                        pass
            
            if flag:
                if message.content.startswith("!adminhelp"):
                    print("HELP!")
                elif message.content.startswith('!admininitserver'):
                    if len(message.raw_channel_mentions) == 1:
                        match.adminInitServer(message.guild.id, message.raw_channel_mentions[0])
                        adminChannelId = match.GuildSettings.getAdminChannelId(message.guild.id)
                        channel = client.get_channel(adminChannelId)
                        await channel.send("<@" + str(message.author.id) + ">, bot initialized! But you need to configure the following: \n\n - Queue channel;\n - Match channel;\n - Flair channel;\n - Flair message. \n\n Use our commands that you can find by typing \"!adminhelp\"!")
                elif adminChannelId != 0:
                    channel = client.get_channel(adminChannelId)
                    commandFlag = False
                    global adminCommands
                    for command in adminCommands:
                        if message.content.startswith(command):
                            commandFlag = True
                            pass

                    if not commandFlag:
                        await channel.send("<@" + str(message.author.id) + ">, unknown command!")
                    else:
                        guildId = message.guild.id
                        if message.content.startswith("!adminuser"):
                            if len(message.raw_mentions) != 1:
                                await channel.send("<@" + str(message.author.id) + ">, invalid command: please only mention one user!")
                            else:
                                player = message.raw_mentions[0]
                                if message.content.startswith('!adminuserremovefromqueue'):
                                    removeSuccessful = await match.adminRemoveFromQueue(client, player, guildId)
                                    if not removeSuccessful:
                                        await channel.send("<@" + str(message.author.id) + ">, this user is currently not in queue!")                            
                                else:
                                    matchFound = await match.getValidMatchAdmin(player, message.guild.id)
                                    if matchFound is None:
                                        await channel.send("<@" + str(message.author.id) + ">, this user is currently not in any matches!")
                                    else:
                                        if message.content.startswith('!adminusercancelset'):
                                            await match.adminCancelSet(client, matchFound)
                                        elif message.content.startswith('!adminuserincrementscore'):
                                            await match.adminIncrementScore(client, matchFound, player)
                                        elif message.content.startswith('!adminuserdqplayer'):
                                            await match.adminDQPlayerFromSet(client, matchFound, player)
                                        elif message.content.startswith('!adminuserresetset'):
                                            await match.adminResetSet(client, guildId, matchFound)
                                        elif message.content.startswith('!adminuserresetmatch'):
                                            await match.adminResetMatch(client, guildId, matchFound)

                        elif message.content.startswith("!adminchannel"):
                            if len(message.raw_channel_mentions) != 1:
                                await channel.send("<@" + str(message.author.id) + ">, invalid command: please only mention one channel!")
                            else:
                                newChannel = message.raw_channel_mentions[0]
                                if message.content.startswith('!adminchannelsetqueue'):
                                    match.adminSetQueueChannel(guildId, newChannel)
                                    await channel.send("<@" + str(message.author.id) + ">, the queue channel has been set to <#" + str(newChannel) + ">!")
                                elif message.content.startswith('!adminchannelsetmatch'):
                                    match.adminSetMatchChannel(guildId, newChannel)
                                    await channel.send("<@" + str(message.author.id) + ">, the match channel has been set to <#" + str(newChannel) + ">!")
                                elif message.content.startswith('!adminchannelsetflair'):
                                    match.adminSetFlairChannel(guildId, newChannel)
                                    await channel.send("<@" + str(message.author.id) + ">, the flair channel has been set to <#" + str(newChannel) + ">!")

                        elif message.content.startswith("!adminconfig"):
                            if message.content.startswith('!adminconfigclearqueue'):
                                await match.adminClearQueue(client, guildId)    
                            elif message.content.startswith('!adminconfigsetdsr'):
                                match.adminSetDSR(guildId)
                                await channel.send("<@" + str(message.author.id) + ">, the ruleset has DSR activated!")
                            elif message.content.startswith('!adminconfigsetmdsr'):
                                match.adminSetMDSR(guildId)
                                await channel.send("<@" + str(message.author.id) + ">, the ruleset has mDSR activated!")
                            elif message.content.startswith('!adminconfigsettsr'):
                                match.adminSetTSR(guildId)
                                await channel.send("<@" + str(message.author.id) + ">, the ruleset has TSR activated!")
                            elif message.content.startswith('!adminconfigsetnodsr'):
                                match.adminSetNoDSR(guildId)
                                await channel.send("<@" + str(message.author.id) + ">, the ruleset has no DSR activated!")
                            elif message.content.startswith('!adminconfigsetmultimatchchannel'):
                                match.adminSetMultiChannel(guildId)
                                await channel.send("<@" + str(message.author.id) + ">, the matchmaking is made by creating specific channels!")
                            elif message.content.startswith('!adminconfigsetsinglematchchannel'):
                                match.adminSetSingleChannel(guildId)
                                await channel.send("<@" + str(message.author.id) + ">, the matchmaking is only made in one single channel!")
                            elif message.content.startswith('!adminconfigsetbancount'):
                                await match.adminSetCounterPickBanCount(guildId, channel, message)
                            elif message.content.startswith('!adminconfigaddstarter'):
                                await match.adminAddStarter(guildId, channel, message)
                            elif message.content.startswith('!adminconfigremovestarter'):
                                await match.adminRemoveStarter(guildId, channel, message)
                            elif message.content.startswith('!adminconfigaddcp'):
                                await match.adminAddCP(guildId, channel, message)
                            elif message.content.startswith('!adminconfigremovecp'):
                                await match.adminRemoveCP(guildId, channel, message)
                            elif message.content.startswith('!adminconfigsendflairmessage'):
                                success = await match.adminSendFlairMessage(client, guildId, message)
                                if success:
                                    await channel.send("<@" + str(message.author.id) + ">, the flair message has been sent!")
                                else:
                                    await channel.send("<@" + str(message.author.id) + ">, the flair channel has not yet been set!")
                            elif message.content.startswith('!adminconfigsetflairmessage'):
                                await match.adminSetFlairMessage(guildId, channel, message)
                            else:
                                if len(message.raw_role_mentions) != 1:
                                    await channel.send("<@" + str(message.author.id) + ">, invalid command: please only mention one role!")
                                else:
                                    roleId = message.raw_role_mentions[0]
                                    if message.content.startswith('!adminconfigaddstaffrole'):
                                        success = match.adminAddStaffRole(client, guildId, roleId) 
                                        if success:
                                            await channel.send("<@" + str(message.author.id) + ">, added role successfully!")
                                        else:
                                            await channel.send("<@" + str(message.author.id) + ">, role already exists!")
                                    elif message.content.startswith('!adminconfigremovestaffrole'):
                                        success = match.adminRemoveStaffRole(guildId, guildId, roleId)
                                        if success:
                                            await channel.send("<@" + str(message.author.id) + ">, role removed successfully!")
                                        else:
                                            await channel.send("<@" + str(message.author.id) + ">, role not found!")
                                    elif message.content.startswith('!adminconfigsetrankingrole'):
                                        match.adminSetRankingRole(guildId)
                                        await channel.send("<@" + str(message.author.id) + ">, role has been set successfully!")


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    if payload.emoji.name == "🥏":
        await replace_role(payload, True)
    elif payload.emoji.name == "🔁":
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if isinstance(channel, discord.channel.DMChannel):
            await match.resendCharacter(client, message, payload.user_id)
    else:
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
    if payload.emoji.name == "🥏":
        await replace_role(payload, False)

@tasks.loop(seconds=10)
async def queue_to_match():
    await match.searchForMatch(client)

async def replace_role(payload, flag):
    if payload.channel_id != match.GuildSettings.getFlairChannelId(payload.guild_id) or payload.message_id != match.GuildSettings.getFlairMessageId(payload.guild_id):       
        return

    guild = client.get_guild(payload.guild_id)
    role = match.getRankingRole(client, payload.guild_id)
    if role is not None:
        user = await guild.fetch_member(payload.user_id)
        if flag:
            await user.add_roles(role)
        else:
            await user.remove_roles(role)


x = os.getenv('TOKEN')

client.run(x)
