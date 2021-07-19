import discord
import random
from enum import Enum
from datetime import datetime
from datetime import timedelta

waitingQueue = []
listOfMatches = []

lockedQueue = False

class QueuedPlayer:
    def __init__(self, userId):
        self.userId = userId
        self.expiration = datetime.utcnow() + timedelta(minutes=30)

class MatchStat:
    queueChannelId = 0
    matchChannelId = 0

class MatchStatus(Enum):
    CHARACTER = 0
    STRIKING = 1
    PLAYING = 2
    RESULTS = 3
    END = 4

class Ruleset:
    starters = ["Battlefield", "Final Destination", "Smashville", "Pokémon Stadium 2", "Town & City"]
    counterPicks = ["Small Battlefield", "Yoshi's Story", "Lylat Cruise", "Kalos Pokémon League"]
    characters = {
        "Mario": ["mario", "number1"], #1
        "Donkey Kong": ["dk", "donkey", "donkey_kong", "donkeykong"], #2
        "Link": ["link", "link1", "botw_link", "botwlink", "botw"], #3
        "Samus": ["samus"], #4
        "Dark Samus": ["dsamus", "samuse", "darksamus", "dark_samus"], #4e
        "Yoshi": ["yoshi"], #5
        "Kirby": ["kirby"], #6
        "Fox": ["fox", "spacie1", "melee"], #7
        "Pikachu": ["pika", "pikachu", "rat1", "smash64"], #8
        "Luigi": ["luigi", "number2"], #9
        "Ness": ["ness", "pk1"], #10
        "Captain Falcon": ["falcon", "captain", "cap", "captainfalcon", "captain_falcon"], #11
        "Jigglypuff": ["puff", "purin", "jigglypuff", "jigg", "jiggly"], #12
        "Peach": ["peach", "princesspeach", "princess_peach"], #13
        "Daisy": ["daisy", "princessdaisy", "princess_daisy", "hiimdaisy", "princess2"], #13e
        "Bowser": ["bowser", "koopa", "kingkoopa", "king_koopa"], #14
        "Ice Climbers": ["icies", "climbers", "iceclimbers", "ice_climbers"], #15
        "Sheik": ["sheik"], #16
        "Zelda": ["zelda", "princesszelda", "princess_zelda", "wisdom"], #17
        "Dr. Mario": ["doc", "docmario", "doc_mario", "dr", "drmario", "dr_mario"], #18
        "Pichu": ["pichu", "rat2"], #19
        "Falco": ["falco", "spacie2"], #20
        "Marth": ["marth", "swordie1"], #21
        "Lucina": ["lucina", "swordie1e"], #21e
        "Young Link": ["yink", "young", "link2", "younglink", "young_link", "ootlink", "oot_link", "oot", "courage"], #22
        "Ganondorf": ["ganon", "ganondorf", "kingofevil", "king_of_evil", "power"], #23
        "Mewtwo": ["mew2", "mewtwo", "m2"], #24
        "Roy": ["roy", "roy1", "ourboy", "swordie2"], #25
        "Chrom": ["chrom", "swordie2e"], #25e
        "Mr. Game & Watch": ["gnw", "g&w", "gew", "gandw", "g_and_w", "gw", "gameandwatch", "game_and_watch", "mrgameandwatch", "mr_game_and_watch"], #26
        "Meta Knight": ["metaknight", "meta_knight", "mk", "brawl"], #27
        "Pit": ["pit"], #28
        "Dark Pit": ["pit2", "pitoo", "dpit", "darkpit", "dark_pit", "blackpit", "black_pit"], #28e
        "Zero Suit Samus": ["samus2", "zss", "zero", "zerosuit", "zerosuitsamus", "zero_suit", "zero_suit_samus"], #29
        "Wario": ["wario", "waluigi", "waaaa"], #30
        "Snake": ["snake", "solid", "solidsnake", "solid_snake"], #31
        "Ike": ["ike", "swordie3"], #32
        "Pokémon Trainer": ["pt", "pokemon", "pokémon", "pokemontrainer", "pokémontrainer", "pokemon_trainer", "pokémon_trainer", "squirtle", "zenigame", "ivysaur", "ivy", "fushigisou", "charizard", "zard", "zardop", "lizardon"], #33-35
        "Diddy Kong": ["diddy", "diddykong", "diddy_kong"], #36
        "Lucas": ["lucas", "pk2"], #37
        "Sonic": ["sonic", "ur2slow"], #38
        "King Dedede": ["d3", "dedede", "ddd", "kingdedede", "king_dedede", "kingddd", "king_ddd"], #39
        "Olimar": ["olimar", "captainolimar", "captain_olimar", "alph"], #40
        "Lucario": ["lucario"], #41
        "R.O.B.": ["rob", "r.o.b.", "robot"], #42
        "Toon Link": ["tink", "toon" , "link3", "toonlink", "toon_link", "ww_link", "wwlink", "ww"], #43
        "Wolf": ["wolf", "spacie3"], #44
        "Villager": ["villager"], #45
        "Mega Man": ["megaman", "mm", "rock", "rockman", "mega_man", "rock_man"], #46
        "Wii Fit Trainer": ["wft", "wii", "wiifit", "wiifittrainer", "wii_fit_trainer"], #47
        "Rosalina & Luma": ["rosalina", "princessrosalina", "princess_rosalina", "rosa", "luma", "rosalina", "rosetta", "rosalinaluma", "rosalinanluma", "rosalina&luma", "rosalina_and_luma"], #48
        "Little Mac": ["mac", "lilmac", "lil_mac", "littlemac", "little_mac"], #49
        "Greninja": ["gren", "greninja", "gekkouga"], #50
        "Mii Brawler": ["miibrawler", "mii_brawler", "brawler", "mii1"], #51
        "Mii Swordfighter": ["miiswordfighter", "miiswordie", "mii_swordfighter", "mii_swordie", "swordfighter", "swordie", "mii2"], #52
        "Mii Gunner": ["miigunner", "mii_gunner", "gunner", "mii3"], #53
        "Palutena": ["palu", "palutena", "washingmachine"], #54
        "PAC-MAN": ["pac", "pacman", "pac_man"], #55
        "Robin": ["robin", "swordie4"], #56
        "Shulk": ["shulk"], #57
        "Bowser Jr.": ["bowserjr", "bowser_jr", "koopajr", "koopa_jr", "princekoopa", "prince_koopa", "ludwig", "larry", "morton", "wendy", "iggy", "roy2", "royk", "roykoopa", "roy_koopa", "lemmy"], #58
        "Duck Hunt": ["duckhunt", "dh", "duck", "duckhuntduo", "duck_hunt_duo", "fakebanjo"], #59
        "Ryu": ["ryu", "shoto"], #60
        "Ken": ["ken", "shotoe"], #60e
        "Cloud": ["cloud", "strife", "cloudstrife", "cloud_strife"], #61
        "Corrin": ["corrin", "corn", "swordie5"], #62
        "Bayonetta": ["bayo", "bayonetta", "sm4sh"], #63
        "Inkling": ["inkling", "inklinggirl", "inklingboy", "inkling_girl", "inkling_boy"], #64
        "Ridley": ["ridley"], #65
        "Simon": ["simon", "belmont", "simonbelmont", "simon_belmont"], #66
        "Richter": ["richter", "belmonte", "richterbelmont", "richter_belmont"], #66e
        "King K. Rool": ["krool", "rool", "kkr", "kingkrool", "king_krool"], #67
        "Isabelle": ["isabelle", "isa", "belle", "bell", "is_a_belle", "shizue"], #68
        "Incineroar": ["incineroar", "incin", "gaogaen"], #69
        "Piranha Plant": ["piranhaplant", "piranha_plant", "plant", "plantgang"], #70
        "Joker": ["joker", "arsene", "ultimate"], #71
        "Hero": ["hero", "luminary", "eight", "erdrick", "solo", "slotmachine", "goku", "trunks", "c17"], #72
        "Banjo & Kazooie": ["banjo", "kazooie", "bk", "banjokazooie", "banjo&kazooie", "banjonkazooie", "banjo_kazooie", "banjo_and_kazooie", "bear_and_bird"], #73
        "Terry": ["terry", "bogard", "terrybogard", "terry_bogard"], #74
        "Byleth": ["byleth", "swordie6"], #75
        "Min Min": ["minmin", "min_min"], #76
        "Steve": ["steve", "alex", "zombie", "enderman", "ender", "herobrine", "trump"], #77
        "Sephiroth": ["sephiroth", "seph"], #78
        "Pyra / Mythra": ["pyra", "mythra", "pyramythra", "pyra_mythra", "pm", "aegis"], #79-80
        "Kazuya": ["kazuya", "mishima", "kazuyamishima", "kazuya_mishima", "devil"], #81
        "Random": ["random", "?", "idk", "jesustakethewheel"] #random
    }
    isDSR = False
    isMDSR = True
    isTSR = False
    dsrMaxBans = 2
    noDSRMaxBans = 3

class ScrapMatch:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

class Match:
    def __init__(self, message, guild, player1, player2, chooser, isBo5, promotion):
        self.message = message
        self.guild = guild
        self.forfeitMessage = 0
        self.player1 = player1
        self.player2 = player2
        self.winner = []
        self.tie = False
        self.surrendered = False
        self.score1 = 0
        self.score2 = 0
        self.player1chars = []
        self.player2chars = []
        self.chooser = chooser
        self.status = MatchStatus.CHARACTER
        self.round = 1
        self.isBo5 = isBo5
        self.bans = []
        self.dsrBans = []
        self.lastWon1 = ""
        self.lastWon2 = ""
        self.promotion = promotion

    def incrementScore(self):
        if Ruleset.isDSR:
            self.dsrBans.append(self.bans[0])

        if self.winner[-1] == self.player1:
            self.score1 += 1
            if Ruleset.isMDSR or Ruleset.isTSR:
                self.lastWon1 = self.bans[0]
        elif self.winner[-1] == self.player2:
            self.score2 += 1
            if Ruleset.isMDSR or Ruleset.isTSR:
                self.lastWon2 = self.bans[0]
        
        self.chooser = self.winner[-1]
        if (self.isBo5 and (self.score1 == 3 or self.score2 == 3)) or (self.score1 == 2 or self.score2 == 2):
            self.status = MatchStatus.END
        else:
            self.status = MatchStatus.STRIKING
            self.round += 1
            self.bans = []

    def forfeit(self, player):
        self.status = MatchStatus.END
        if player == self.player1:
            self.score1 = -1
            self.score2 = 0
            self.winner = [self.player2]
        elif player == self.player2:
            self.score1 = 0
            self.score2 = -1
            self.winner = [self.player1]
        self.surrendered = True

    def tieScore(self):
        self.status = MatchStatus.END
        self.score1 = 0
        self.score2 = 0
        self.winner = []
        self.tie = True

def ready():
    MatchStat.queueChannelId = 865882258636406804
    MatchStat.matchChannelId = 865882224553623552

async def getRankingRole(guild):
    myRole = discord.utils.get(guild.roles,name="Ranking1v1")
    if myRole is None:
        await guild.create_role(name="Ranking1v1", colour=discord.Colour(0xff5555))
        myRole = discord.utils.get(guild.roles,name="Ranking1v1")
    
    return myRole

async def queue(client, strMsg):
    flag = checkUserInQueue(strMsg)
    if flag:
        queueChannelId = client.get_channel(MatchStat.queueChannelId)
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you are already in waiting queue, please wait for your opponent!")
        return

    flag = checkExistingMatch(strMsg)
    if flag:
        queueChannelId = client.get_channel(MatchStat.queueChannelId)
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you are already in a match, please finish your match!")
    else:
        queueChannelId = client.get_channel(MatchStat.queueChannelId)
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you have been added to the queue, waiting for opponent...")
        global waitingQueue
        queuedPlayer = QueuedPlayer(strMsg.author.id)
        waitingQueue.append(queuedPlayer)

async def unqueue(client, strMsg):
    queueChannelId = client.get_channel(MatchStat.queueChannelId)
    flag = checkExistingMatch(strMsg)
    if flag:
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you are already in a match, please finish your match!")
        return

    flag = False
    if waitingQueue:
        for user in waitingQueue:
            if user.userId == strMsg.author.id:
                await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you have been removed from the queue by request!")
                waitingQueue.remove(user)
                flag = True
                pass

    if not flag:
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you are not in any queue!")
    

async def searchForMatch(client):
    global waitingQueue
    global lockedQueue
    if not lockedQueue:
        count = len(waitingQueue)
        if count >= 2:
            lockedQueue = True           
            scrapMatches = await try_match(client)
            if scrapMatches:
                for scrapMatch in scrapMatches:
                    await sendMessage(client, player1=scrapMatch.player1.userId, player2=scrapMatch.player2.userId)

                    waitingQueue.remove(scrapMatch.player1)
                    waitingQueue.remove(scrapMatch.player2)
                
            lockedQueue = False
        elif count == 1:
            if datetime.utcnow() >= waitingQueue[0].expiration:
                await removeFromQueue(client, waitingQueue[0])

async def try_match(client):
    global waitingQueue
    for queuedPlayer in waitingQueue:
        if datetime.utcnow() >= queuedPlayer.expiration:
            await removeFromQueue(client, queuedPlayer)

    # db connection and handling

    scrapMatches = [ScrapMatch(waitingQueue[0], waitingQueue[1])]
    return scrapMatches

async def removeFromQueue(client, queuedPlayer):
    global waitingQueue
    queueChannelId = client.get_channel(MatchStat.queueChannelId)
    await queueChannelId.send("<@" + str(queuedPlayer.userId) + ">, we couldn't find you an opponent for ranked and you have been removed from the queue, please try again later.")
    waitingQueue.remove(queuedPlayer)


async def sendMessage(client, match=None, player1=0, player2=0):
    matchChannelId = client.get_channel(MatchStat.matchChannelId)

    if match is None:
        title = "Round 1!"
        playerChosen = choosePlayer(player1, player2)       
        description = "<@" + str(player1) + "> vs. <@"+ str(player2) +">! Check your DMs to pick your character!"
        fields = []
        mainMessage = "Get ready for the next battle! \n"
    else:
        title = "Round " + str(match.round) + "!"
        if match.status == MatchStatus.CHARACTER:
            if match.round == 1: 
                description = "<@" + str(match.player1) + "> vs. <@"+ str(match.player2) +">! Check your DMs to pick your character!"
                fields = []
                mainMessage = "Choose your character <@" + str(match.player2) + ">! \n"
            else:
                description = "<@" + str(match.player1) + "> vs. <@"+ str(match.player2) +">! Check your DMs to pick your character!"
                fields = []
                mainMessage = "Choose your character <@" + str(match.chooser) + ">!"
        elif match.status == MatchStatus.STRIKING:
            if match.round == 1:
                count = len(match.bans)
                if count == 3:
                    description = "<@"+str(match.chooser)+"> ban your last stage! Then both players will play on the remaining one!"
                else:
                    description = "<@"+str(match.chooser)+"> ban your next stage!"
            else:
                count = len(match.bans)
                if Ruleset.isDSR or Ruleset.isMDSR or Ruleset.isTSR:
                    maxBans = Ruleset.dsrMaxBans
                else:
                    maxBans = Ruleset.noDSRMaxBans

                if count == maxBans:
                    description = "<@"+str(match.chooser)+"> pick your stage!"
                else:
                    description = "<@"+str(match.chooser)+"> ban your next stage!"

            listOfBans = arrangeBans(match)
            fields = arrangeBanFields(listOfBans)
            mainMessage = "Striking phase! \n"
        elif match.status == MatchStatus.PLAYING:
            mainMessage = "Face-off! \n"
            listOfBans = arrangeBans(match)
            description = "Now playing on: **" + listOfBans[0] + "** \n At the end of your round, <@" + str(match.chooser) + "> please report the result and your opponent will verify it afterwards."
            fields = arrangePlayFields(client, match)
        elif match.status == MatchStatus.RESULTS:
            if match.chooser == match.player1:
                match.chooser = match.player2
            elif match.chooser == match.player2:
                match.chooser = match.player1

            mainMessage = "Is <@" + str(match.winner[-1]) + "> the winner? \n"
            description = "Confirm your result <@" + str(match.chooser) + ">!"
            fields = []
        elif match.status == MatchStatus.END:
            if match.tie:
                title = "NO CONTEST!"
                mainMessage = "TIE! <@" + str(match.player1) + "> and <@" + str(match.player2) + "> agreed to a tie. \n"
                description = "How anticlimatic..."
            else:
                title = "GAME!"
                if match.winner[-1] == match.player1:
                    winner = match.player1
                    loser = match.player2
                elif match.winner[-1] == match.player2:
                    winner = match.player2
                    loser = match.player1

                mainMessage = "<@" + str(winner) + "> is the winner of this set! Congratulations! GGs! \n"
                if match.forfeit:
                    description = "Not like this, <@" + str(loser) + ">..."
                else:
                    description = "Better luck next time <@" + str(loser) + ">! Don't be salty and shake your opponent's hand!"
            fields = []

    if match is None:
        mainMessageSuffix = "**<@" + str(player1) + ">** vs. **<@"+ str(player2) +">** \n **Score**: 0 - 0"
    else:
        if match.status == MatchStatus.END:
            if match.tie:
                mainMessageSuffix = "**<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">** \n **Score**: TIE"
            elif match.surrendered:
                if match.score1 == -1:
                    score1 = "DQ"
                    score2 = "W"
                elif match.score2 == -1:
                    score1 = "W"
                    score2 = "DQ"
                mainMessageSuffix = "**<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">** \n **Score**: " + score1 + " - " + score2
            else:
                characters1 = buildCharacterList(match.player1chars)
                characters2 = buildCharacterList(match.player2chars)
                mainMessageSuffix = "**<@" + str(match.player1) + ">** *(" + characters1 + ")* vs. **<@"+ str(match.player2) +">** *(" + characters2 + ")* \n **Score**: " + str(match.score1) + " - " + str(match.score2)

        elif match.player1chars and match.player2chars and len(match.player1chars) == match.round and len(match.player2chars) == match.round:
            mainMessageSuffix = "**<@" + str(match.player1) + ">** *(" + match.player1chars[match.round - 1] + ")* vs. **<@"+ str(match.player2) +">** *(" + match.player2chars[match.round - 1] + ")* \n **Score**: " + str(match.score1) + " - " + str(match.score2)
        else:
            mainMessageSuffix = "**<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">** \n **Score**: " + str(match.score1) + " - " + str(match.score2)

    mainMessage += mainMessageSuffix

    embed = discord.Embed(title=title, description=description)
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    message = await matchChannelId.send(mainMessage, embed=embed)
    global listOfMatches
    if match is None:
        match = Match(message.id, message.guild.id, player1, player2, playerChosen, False, False)

        await sendMessageToUser(client, player1)
        forfeitMessage = await sendTieOrForfeitMessage(client, match)
        match.forfeitMessage = forfeitMessage.id

        listOfMatches.append(match)
        
    if match.status == MatchStatus.STRIKING:
        await add_ban_reaction(message, listOfBans)
    elif match.status == MatchStatus.PLAYING:
        await add_victory_reaction(message)
    elif match.status == MatchStatus.RESULTS:
        await add_decision_reaction(message)
    elif match.status == MatchStatus.END:
        listOfMatches.remove(match)

    return message

async def sendTieOrForfeitMessage(client, match):
    matchChannelId = client.get_channel(MatchStat.matchChannelId)
    embed = discord.Embed(title="Tie or Forfeit?", description="Both players need to agree on tie! \n Only one player can forfeit.")
    mainMessage = "Tie or Forfeit? \n **<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">**"
    message = await matchChannelId.send(mainMessage, embed=embed)
    await add_tie_or_forfeit_reaction(message)
    return message

def buildCharacterList(characters):
    charList = ""
    listChars = list(dict.fromkeys(characters))
    for char in listChars:
        charList += char
        if listChars[-1] != char:
            charList += ", "
    return charList

def choosePlayer(player1, player2):
    value = random.randint(1,10) % 2
    if value == 0:
        return player1
    else:
        return player2

async def sendMessageToUser(client, player, char=""):
    user = client.get_user(player)
    embed = discord.Embed(title="Example:", description="!char donkeykong \n !char dk \n !char donkey_kong")
    await user.send("Choose your character by sending the command **!char** *[name_or_alias_of_your_character_here]*", embed=embed)
    if char != "":
        await user.send("Your opponent chose: **" + char + "**")

async def validateChar(client, message):
    if not contains(lambda x: x.player1 == message.author.id or x.player2 == message.author.id):
        return

    match = get(lambda x: x.player1 == message.author.id or x.player2 == message.author.id)

    if match.player1 == message.author.id:
        listToCheck = match.player1chars
        userId = match.player1
    else:
        listToCheck = match.player2chars
        userId = match.player2

    user = client.get_user(userId)

    if (match.round == 1 and listToCheck) or (match.round == 2 and len(listToCheck) != 1) or (match.round == 3 and len(listToCheck) != 2) or (match.isBo5 and match.round == 4 and len(listToCheck) != 3) or (match.isBo5 and match.round == 5 and len(listToCheck) != 4):
        await user.send("No need to select a character, you've already selected: + " + match.player1chars[-1] + "!")
    
    text = message.content.lower()
    parts = text.split(" ", 1)
    if len(parts) != 2:
        await user.send("Wrong input, please try again!")
        await sendMessageToUser(client, userId)
    else:
        char = getCharacterName(parts[1])
        if char == "INVALID":
            await user.send("Wrong input, please try again!")
            await sendMessageToUser(client, userId)
        else:
            listToCheck.append(char)
            if match.player1 == message.author.id:
                match.player1chars = listToCheck 
            else:
                match.player2chars = listToCheck 
            
            if len(match.player1chars) != len(match.player2chars):
                if match.round == 1:
                    await sendMessageToUser(client, match.player2)
                else:
                    if len(match.player1chars) < len(match.player2chars):
                        await sendMessageToUser(client, match.player1, char)
                    else:
                        await sendMessageToUser(client, match.player2, char)
            else:
                if match.round == 1:
                    match.status = MatchStatus.STRIKING
                else:
                    match.status = MatchStatus.PLAYING

            await user.send("You've selected: **" + char + "**")

            channel = client.get_channel(MatchStat.matchChannelId)
            message = await channel.fetch_message(match.message)
            oldmessage = message.id
            messages = [message]
            await channel.delete_messages(messages)
            message = await sendMessage(client, match)
            match.message = message.id

            replace(match, lambda x: x.message == oldmessage)
            

def getCharacterName(charAlias):
    for key, value in Ruleset.characters.items():
        for alias in value:
            if charAlias == alias:
                return key

    return "INVALID"

def checkExistingMatch(message):
    if contains(lambda x: x.player1 == message.author.id or x.player2 == message.author.id):       
        return True

    return False

def checkUserInQueue(message):
    global waitingQueue
    if waitingQueue:
        for user in waitingQueue:
            if user.userId == message.author.id:
                return True

    return False

async def getValidMatch(payload):
    if payload.channel_id != MatchStat.matchChannelId:       
        return None
    if not contains(lambda x: x.player1 == payload.user_id or x.player2 == payload.user_id):       
        return None
    match = get(lambda x: x.player1 == payload.user_id or x.player2 == payload.user_id)
    if match is None:
        return None
    if payload.message_id != match.message and payload.message_id != match.forfeitMessage:       
        return None
    
    return match

async def tieOrForfeit(client, payload, match):
    flag = False
    if payload.emoji.name == "🏳️":
        flag = True
        if payload.user_id == match.player1:
            match.forfeit(match.player1)
        elif payload.user_id == match.player2:
            match.forfeit(match.player2)
    elif payload.emoji.name == "🤝":
        channel = client.get_channel(MatchStat.matchChannelId)
        message = await channel.fetch_message(match.forfeitMessage)
        if message.reactions:
            for reaction in message.reactions:
                if reaction.emoji == "🤝" and reaction.count >= 2:
                    matchUsers = [match.player1, match.player2]
                    users = await reaction.users().flatten()
                    if all(x in list(map(lambda x: x.id, users)) for x in matchUsers):
                        match.tieScore()
                        flag = True
                    pass

    if flag:
        channel = client.get_channel(MatchStat.matchChannelId)
        message = await channel.fetch_message(match.message)
        forfeitMessage = await channel.fetch_message(match.forfeitMessage)
        oldmessage = message.id
        messages = [message, forfeitMessage]
        await channel.delete_messages(messages)
        message = await sendMessage(client, match)
        match.message = message.id

        replace(match, lambda x: x.message == oldmessage)

async def stageStriking(client, payload, match):
    text = getText(payload.emoji.name)
    if text != "Big Battlefield":
        count = len(match.bans)
        if match.round == 1:
            match.bans.append(text)
            if count == 0 or count == 2: # first or second-to-last ban
                if match.player1 == match.chooser:
                    match.chooser = match.player2
                elif match.player2 == match.chooser:
                    match.chooser = match.player1

            if count == 3: # last ban
                match.status = MatchStatus.PLAYING
        else:
            if count < 2:
                match.bans.append(text)
                if count == 1:
                    if match.player1 == match.chooser:
                        match.chooser = match.player2
                    elif match.player2 == match.chooser:
                        match.chooser = match.player1
            else:
                if match.player1 == match.chooser:
                    match.chooser = match.player2
                elif match.player2 == match.chooser:
                    match.chooser = match.player1

                match.bans = [text]
                match.status = MatchStatus.CHARACTER
                await sendMessageToUser(client, match.chooser)

        channel = client.get_channel(MatchStat.matchChannelId)
        message = await channel.fetch_message(match.message)
        oldmessage = message.id
        messages = [message]
        await channel.delete_messages(messages)
        message = await sendMessage(client, match)
        match.message = message.id

        replace(match, lambda x: x.message == oldmessage)

async def victoryDecision(client, payload, match):
    flag = False
    if payload.emoji.name == "1️⃣":
        match.winner.append(match.player1)
        flag = True
    elif payload.emoji.name == "2️⃣":
        match.winner.append(match.player2)
        flag = True

    if flag:
        match.status = MatchStatus.RESULTS

        channel = client.get_channel(MatchStat.matchChannelId)
        message = await channel.fetch_message(match.message)
        oldmessage = message.id
        messages = [message]
        await channel.delete_messages(messages)
        message = await sendMessage(client, match)
        match.message = message.id

        replace(match, lambda x: x.message == oldmessage)

async def victoryConfirm(client, payload, match):
    flag = False
    decision = False
    if payload.emoji.name == "🇾":
        flag = True
        decision = True
    elif payload.emoji.name == "🇳":
        flag = True
        decision = False

    if flag:
        if decision:
            match.incrementScore()
        else:
            match.winner.pop()
            match.status = MatchStatus.PLAYING

        channel = client.get_channel(MatchStat.matchChannelId)
        message = await channel.fetch_message(match.message)
        oldmessage = message.id
        if match.Status == MatchStatus.END:
            forfeitMessage = await channel.fetch_message(match.forfeitMessage)
            messages = [message, forfeitMessage]
        else:
            messages = [message]
        await channel.delete_messages(messages)
        message = await sendMessage(client, match)
        match.message = message.id

        replace(match, lambda x: x.message == oldmessage)

def arrangeBans(match):
    if match.round == 1:
        completeList = Ruleset.starters
    else:
        completeList = Ruleset.starters + Ruleset.counterPicks

    if Ruleset.isDSR:
        completeList = [x for x in completeList if x not in match.dsrBans]
    elif Ruleset.isMDSR:
        if match.winner[-1] == match.player1 and match.lastWon2 != "":
            completeList.remove(match.lastWon2)
        elif match.winner[-1] == match.player2 and match.lastWon1 != "":
            completeList.remove(match.lastWon1)
    elif Ruleset.isTSR:
        if match.winner[-1] == match.player1 and match.lastWon2 != "":
            for counter in Ruleset.counterPicks:
                if counter == match.lastWon2:
                    completeList.remove(match.lastWon2)
                    pass
        elif match.winner[-1] == match.player2 and match.lastWon1 != "":
            for counter in Ruleset.counterPicks:
                if counter == match.lastWon1:
                    completeList.remove(match.lastWon1)
                    pass

    return [x for x in completeList if x not in match.bans]

def arrangeBanFields(listOfBans):   
    fields = []
    for item in listOfBans:
        emote = getEmote(item)
        fields.append((item, emote, True))
    return fields

def arrangePlayFields(client, match):   
    fields = []
    player1 = client.get_user(match.player1)
    player2 = client.get_user(match.player2)

    fields.append((str(player1.name), "1️⃣", True))
    fields.append((str(player2.name), "2️⃣", True))

    return fields

async def add_ban_reaction(message, listOfBans):
    for item in listOfBans:
        emote = getEmote(item)
        await message.add_reaction(emote)

async def add_victory_reaction(message):
    await message.add_reaction("1️⃣") # player 1 wins
    await message.add_reaction("2️⃣") # player 2 wins

async def add_decision_reaction(message):
    await message.add_reaction("🇾") # confirm
    await message.add_reaction("🇳") # reject

async def add_tie_or_forfeit_reaction(message):
    await message.add_reaction("🤝") # tie
    await message.add_reaction("🏳️") # forfeit

def contains(filter):
    global listOfMatches
    if listOfMatches:
        for match in listOfMatches:
            if filter(match):
                return True
    return False

def replace(newMatch, filter):
    global listOfMatches
    if listOfMatches:
        for index, match in enumerate(listOfMatches):
            if filter(match):
                listOfMatches[index] = newMatch
                pass

def get(filter):
    global listOfMatches
    if listOfMatches:
        return next((x for x in listOfMatches if filter), None)
    return None

def getEmote(text):
    emote = "0️⃣"
    if text == "Battlefield":
        emote = "1️⃣"
    elif text == "Final Destination":
        emote = "2️⃣"
    elif text == "Smashville":
        emote = "3️⃣"
    elif text == "Pokémon Stadium 2":
        emote = "4️⃣"
    elif text == "Town & City":
        emote = "5️⃣"
    elif text == "Small Battlefield":
        emote = "6️⃣"
    elif text == "Yoshi's Story":
        emote = "7️⃣"
    elif text == "Lylat Cruise":
        emote = "8️⃣"
    elif text == "Kalos Pokémon League":
        emote = "9️⃣"
    return emote

def getText(emote):
    text = "Big Battlefield"
    if emote == "1️⃣":
        text = "Battlefield"
    elif emote == "2️⃣":
        text = "Final Destination"
    elif emote == "3️⃣":
        text = "Smashville"
    elif emote == "4️⃣":
        text = "Pokémon Stadium 2"
    elif emote == "5️⃣":
        text = "Town & City"
    elif emote == "6️⃣":
        text = "Small Battlefield"
    elif emote == "7️⃣":
        text = "Yoshi's Story"
    elif emote == "8️⃣":
        text = "Lylat Cruise"
    elif emote == "9️⃣":
        text = "Kalos Pokémon League"
    return text