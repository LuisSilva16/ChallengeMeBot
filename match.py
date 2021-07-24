import discord
import random
from enum import Enum
from datetime import datetime
from datetime import timedelta

waitingQueue = []
listOfMatches = []

lockedQueue = False

class QueuedPlayer:
    def __init__(self, userId, guildId):
        self.userId = userId
        self.guildId = guildId
        self.expiration = datetime.utcnow() + timedelta(minutes=30)

class GuildSettings:
    isMultiChannelMode = {}

    queueChannelId = {}
    matchChannelId = {}
    
    adminChannelId = {}

    flairChannelId = {}
    flairMessageId = {}

    rankingRoles = {}
    rankingAdminRoles = {}

    rulesets = {}

    def getIsMultiChannelMode(guildId):
        if not str(guildId) in GuildSettings.isMultiChannelMode:
            GuildSettings.isMultiChannelMode[str(guildId)] = False

        return GuildSettings.isMultiChannelMode[str(guildId)]

    def setIsMultiChannelMode(guildId, flag):
        GuildSettings.isMultiChannelMode[str(guildId)] = flag

    def getQueueChannelId(guildId):
        if not str(guildId) in GuildSettings.queueChannelId:
            GuildSettings.queueChannelId[str(guildId)] = 0

        return GuildSettings.queueChannelId[str(guildId)]

    def setQueueChannelId(guildId, channelId):
        GuildSettings.queueChannelId[str(guildId)] = channelId

    def getMatchChannelId(guildId):
        if not str(guildId) in GuildSettings.matchChannelId:
            GuildSettings.matchChannelId[str(guildId)] = 0

        return GuildSettings.matchChannelId[str(guildId)]

    def setMatchChannelId(guildId, channelId):
        GuildSettings.matchChannelId[str(guildId)] = channelId

    def getAdminChannelId(guildId):
        if not str(guildId) in GuildSettings.adminChannelId:
            GuildSettings.adminChannelId[str(guildId)] = 0

        return GuildSettings.adminChannelId[str(guildId)]

    def setAdminChannelId(guildId, channelId):
        GuildSettings.adminChannelId[str(guildId)] = channelId

    def getFlairChannelId(guildId):
        if not str(guildId) in GuildSettings.flairChannelId:
            GuildSettings.flairChannelId[str(guildId)] = 0

        return GuildSettings.flairChannelId[str(guildId)]

    def setFlairChannelId(guildId, channelId):
        GuildSettings.flairChannelId[str(guildId)] = channelId

    def getFlairMessageId(guildId):
        if not str(guildId) in GuildSettings.flairMessageId:
            GuildSettings.flairMessageId[str(guildId)] = 0

        return GuildSettings.flairMessageId[str(guildId)]

    def setFlairMessageId(guildId, messageId):
        GuildSettings.flairMessageId[str(guildId)] = messageId

    def getRankingRole(guildId):
        if not str(guildId) in GuildSettings.rankingRoles:
            GuildSettings.rankingRoles[str(guildId)] = "Ranking1v1"

        return GuildSettings.rankingRoles[str(guildId)]

    def setRankingRole(guildId, rankingRole):
        GuildSettings.rankingRoles[str(guildId)] = rankingRole

    def getAdminRoles(guildId):
        if not str(guildId) in GuildSettings.rankingAdminRoles:
            GuildSettings.rankingAdminRoles[str(guildId)] = ["RankingStaff"]

        return GuildSettings.rankingAdminRoles[str(guildId)]

    def setAdminRoles(guildId, adminRoles):
        GuildSettings.rankingAdminRoles[str(guildId)] = adminRoles
    
    def getRuleset(guildId):
        if not str(guildId) in GuildSettings.rulesets:
            GuildSettings.rulesets[str(guildId)] = Ruleset()

        return GuildSettings.rulesets[str(guildId)]

    def setRuleset(guildId, ruleset):
        GuildSettings.rulesets[str(guildId)] = ruleset

    def initRuleset(guildId):
        GuildSettings.rulesets[str(guildId)] = Ruleset()

class MatchStatus(Enum):
    CHARACTER = 0
    STRIKING = 1
    PLAYING = 2
    RESULTS = 3
    END = 4

class Ruleset:
    def __init__(self):
        self.stages = {
            "Battlefield": ["bf", "battle", "battle1", "battlefield"],
            "Final Destination": [ "fd", "final", "finaldestination", "final_destination" ],
            "Smashville": [ "sv", "ville", "smashville" ],
            "Pokémon Stadium 2": [ "ps2", "ps", "playstation2", "pokemonstadium2", "pokemon_stadium_2", "pokémonstadium2", "pokémon_stadium_2" ],
            "Town & City": [ "tc", "tnc", "t&c", "townandcity", "town_and_city", "town&city" ],
            "Small Battlefield": [ "sbf", "battle2", "smallbattlefield", "small_battlefield" ],
            "Yoshi's Story": [ "yoshi", "yoshis", "yoshisstory", "yoshistory", "yoshis_story", "yoshi_story" ],
            "Lylat Cruise": [ "lylat", "cruise", "lylatcruise", "lylat_cruise" ],
            "Kalos Pokémon League": [ "kalos", "kalospokemonleague", "kalos_pokemon_league", "kalospokémonleague", "kalos_pokémon_league" ],
            "Northern Cave": [ "nc", "northerncave", "northern_cave", "jenova" ]
        }
        self.starters = ["Battlefield", "Final Destination", "Smashville", "Pokémon Stadium 2", "Town & City"]
        self.counterPicks = ["Small Battlefield", "Yoshi's Story", "Lylat Cruise", "Kalos Pokémon League"]
        self.characters = {
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
        self.isDSR = False
        self.isMDSR = True
        self.isTSR = False
        self.counterPickBans = 2

    def getCharacterName(self, charAlias):
        for key, value in self.characters.items():
            for alias in value:
                if charAlias == alias:
                    return key

        return "INVALID"

    def getStageName(self, charAlias):
        for key, value in self.stages.items():
            for alias in value:
                if charAlias == alias:
                    return key

        return "INVALID"

    def arrangeBans(self, match):
        if match.round == 1:
            completeList = self.starters
        else:
            completeList = self.starters + self.counterPicks
            if self.isDSR:
                completeList = [x for x in completeList if x not in match.dsrBans]
            elif self.isMDSR:
                if match.winner[-1] == match.player1 and match.lastWon2:
                    completeList.remove(match.lastWon2[-1])
                elif match.winner[-1] == match.player2 and match.lastWon1:
                    completeList.remove(match.lastWon1[-1])
            elif self.isTSR:
                if match.winner[-1] == match.player1 and match.lastWon2:
                    for counter in self.counterPicks:
                        if counter == match.lastWon2[-1]:
                            completeList.remove(match.lastWon2[-1])
                            pass
                elif match.winner[-1] == match.player2 and match.lastWon1:
                    for counter in self.counterPicks:
                        if counter == match.lastWon1[-1]:
                            completeList.remove(match.lastWon1[-1])
                            pass

        return [x for x in completeList if x not in match.bans]

class ScrapMatch:
    def __init__(self, player1, player2):
        self.player1 = player1.userId
        self.player2 = player2.userId
        self.guildId = player1.guildId

class Match:
    def __init__(self, message, channel, guild, player1, player2, chooser, isBo5, promotion):
        self.message = message
        self.channel = channel
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
        self.lastWon1 = []
        self.lastWon2 = []
        self.promotion = promotion

    def incrementScore(self):
        ruleset = GuildSettings.getRuleset(self.guild)
        if ruleset.isDSR:
            self.dsrBans.append(self.bans[0])

        if self.winner[-1] == self.player1:
            self.score1 += 1
            if (ruleset.isMDSR or ruleset.isTSR) and self.bans:
                self.lastWon1.append(self.bans[0])
        elif self.winner[-1] == self.player2:
            self.score2 += 1
            if (ruleset.isMDSR or ruleset.isTSR) and self.bans:
                self.lastWon2.append(self.bans[0])
        
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

    def reset(self):
        self.round -= 1
        if self.winner[-1] == self.player1:
            self.score1 -= 1
            self.lastWon1.pop()
        elif self.winner[-1] == self.player2:
            self.score2 -= 1
            self.lastWon2.pop()
        self.winner.pop()
        self.chooser = self.winner[-1]
        self.status = MatchStatus.STRIKING

def ready(guildId, messageId):
    initServer(guildId, queueChannelId=865882258636406804, matchChannelId=865882224553623552, adminChannelId=867024058175979550, flairChannelId=865593981164847115, flairMessageId=messageId, isMultiChannel=True)

def initServer(guildId, rankingRole="Ranking1v1", adminRankingRoles=["RankingStaff"], queueChannelId=0, matchChannelId=0, adminChannelId=0, flairChannelId=0, flairMessageId=0, isMultiChannel=False):
    GuildSettings.setRankingRole(guildId, rankingRole)
    GuildSettings.setAdminRoles(guildId, adminRankingRoles)
    
    GuildSettings.setQueueChannelId(guildId, queueChannelId)
    GuildSettings.setMatchChannelId(guildId, matchChannelId)

    GuildSettings.setAdminChannelId(guildId, adminChannelId)

    GuildSettings.setFlairChannelId(guildId, flairChannelId)
    GuildSettings.setFlairMessageId(guildId, flairMessageId)

    GuildSettings.initRuleset(guildId)

    GuildSettings.setIsMultiChannelMode(guildId, isMultiChannel)

def getBotRole(client, guildId):
    guild = client.get_guild(guildId)
    myRole = discord.utils.get(guild.roles, name="ChallengeMe")    
    return myRole

def getRankingRole(client, guildId):
    guild = client.get_guild(guildId)
    myRoleName = GuildSettings.getRankingRole(guild.id)
    myRole = discord.utils.get(guild.roles, name=myRoleName)    
    return myRole

def getAdminRankingRoles(client, guildId):
    guild = client.get_guild(guildId)
    myRoles = GuildSettings.getAdminRoles(guild.id)
    returnRoles = []
    if myRoles:
        for myRoleName in myRoles:
            myRole = discord.utils.get(guild.roles, name=myRoleName)
            if myRole is not None:
                returnRoles.append(myRole)
    
    return returnRoles

async def queue(client, strMsg):
    queueChannelId = client.get_channel(GuildSettings.getQueueChannelId(strMsg.guild.id))
    flag = checkUserInQueue(strMsg.author.id)
    if flag:
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you are already in waiting queue, please wait for your opponent!")
        return

    flag = checkExistingMatch(strMsg.author.id)
    if flag:
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you are already in a match, please finish your match!")
    else:
        await queueChannelId.send("<@" + str(strMsg.author.id) + ">, you have been added to the queue, waiting for opponent...")
        global waitingQueue
        queuedPlayer = QueuedPlayer(strMsg.author.id, strMsg.guild.id)
        waitingQueue.append(queuedPlayer)

async def requeue(client, payload):
    queueChannelId = client.get_channel(GuildSettings.getQueueChannelId(payload.guild_id))
    flag = checkUserInQueue(payload.user_id)
    if flag:
        await queueChannelId.send("<@" + str(payload.user_id) + ">, you are already in waiting queue, please wait for your opponent!")
        return

    flag = checkExistingMatch(payload.user_id)
    if flag:
        await queueChannelId.send("<@" + str(payload.user_id) + ">, you are already in a match, please finish your match!")
    else:
        await queueChannelId.send("<@" + str(payload.user_id) + ">, you have been added to the queue, waiting for opponent...")
        global waitingQueue
        queuedPlayer = QueuedPlayer(payload.user_id, payload.guild_id)
        waitingQueue.append(queuedPlayer)

async def unqueue(client, strMsg):
    queueChannelId = client.get_channel(GuildSettings.getQueueChannelId(strMsg.guild.id))
    flag = checkExistingMatch(strMsg.author.id)
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
                    await sendMessage(client, guildId=scrapMatch.guildId, player1=scrapMatch.player1, player2=scrapMatch.player2)
                
            lockedQueue = False
        elif count == 1:
            if datetime.utcnow() >= waitingQueue[0].expiration:
                await removeFromQueue(client, waitingQueue[0])

async def try_match(client):
    global waitingQueue
    scrapMatches = []
    for queuedPlayer in waitingQueue:
        if datetime.utcnow() >= queuedPlayer.expiration:
            await removeFromQueue(client, queuedPlayer)

    # db connection and handling

    if waitingQueue[0].guildId == waitingQueue[1].guildId:
        waitingPlayer1 = waitingQueue[0]
        waitingPlayer2 = waitingQueue[1]

        scrapMatch = ScrapMatch(waitingPlayer1, waitingPlayer2)
        scrapMatches.append(scrapMatch)
        waitingQueue.remove(waitingPlayer1)
        waitingQueue.remove(waitingPlayer2)

    return scrapMatches

async def removeFromQueue(client, queuedPlayer):
    global waitingQueue
    queueChannelId = client.get_channel(GuildSettings.getQueueChannelId(queuedPlayer.guildId))
    await queueChannelId.send("<@" + str(queuedPlayer.userId) + ">, we couldn't find you an opponent for ranked and you have been removed from the queue, please try again later.")
    waitingQueue.remove(queuedPlayer)


async def sendMessage(client, match=None, guildId=0, player1=0, player2=0):
    if match is not None and guildId == 0:
        guildId = match.guild

    if match is None:
        title = "Round 1!"
        playerChosen = choosePlayer(player1, player2)       
        description = "<@" + str(player1) + "> vs. <@"+ str(player2) +">! Check your DMs to pick your character!"
        fields = []
        mainMessage = "Get ready for the next battle! \n"
    else:
        title = "Round " + str(match.round) + "!"
        ruleset = GuildSettings.getRuleset(match.guild)
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
                if count == ruleset.counterPickBans:
                    description = "<@"+str(match.chooser)+"> pick your stage!"
                else:
                    description = "<@"+str(match.chooser)+"> ban your next stage!"

            listOfBans = ruleset.arrangeBans(match)
            fields = arrangeBanFields(listOfBans)
            mainMessage = "Striking phase! \n"
        elif match.status == MatchStatus.PLAYING:
            mainMessage = "Face-off! \n"
            listOfBans = ruleset.arrangeBans(match)
            description = "Now playing on: **" + listOfBans[0] + "** \nAt the end of your round, <@" + str(match.chooser) + "> please report the result and your opponent will verify it afterwards."
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
                if match.surrendered:
                    description = "Not like this, <@" + str(loser) + ">..."
                else:
                    description = "Better luck next time <@" + str(loser) + ">! Don't be salty and shake your opponent's hand!"
            fields = []

    if match is None:
        mainMessageSuffix = "**<@" + str(player1) + ">** vs. **<@"+ str(player2) +">** \n**Score**: 0 - 0"
    else:
        if match.status == MatchStatus.END:
            if match.tie:
                mainMessageSuffix = "**<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">** \n**Score**: TIE"
            elif match.surrendered:
                if match.score1 == -1:
                    score1 = "DQ"
                    score2 = "W"
                elif match.score2 == -1:
                    score1 = "W"
                    score2 = "DQ"
                mainMessageSuffix = "**<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">** \n**Score**: " + score1 + " - " + score2
            else:
                characters1 = buildCharacterList(match.player1chars)
                characters2 = buildCharacterList(match.player2chars)
                mainMessageSuffix = "**<@" + str(match.player1) + ">** *(" + characters1 + ")* vs. **<@"+ str(match.player2) +">** *(" + characters2 + ")* \n**Score**: " + str(match.score1) + " - " + str(match.score2)

        elif match.player1chars and match.player2chars and len(match.player1chars) == match.round and len(match.player2chars) == match.round:
            mainMessageSuffix = "**<@" + str(match.player1) + ">** *(" + match.player1chars[match.round - 1] + ")* vs. **<@"+ str(match.player2) +">** *(" + match.player2chars[match.round - 1] + ")* \n**Score**: " + str(match.score1) + " - " + str(match.score2)
        else:
            mainMessageSuffix = "**<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">** \n**Score**: " + str(match.score1) + " - " + str(match.score2)

    mainMessage += mainMessageSuffix

    embed = discord.Embed(title=title, description=description)
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
   
    global listOfMatches
    if match is None:
        if GuildSettings.getIsMultiChannelMode(guildId):
            channelId = await createMatchChannel(client, guildId, player1, player2)
        else:
            channelId = GuildSettings.getMatchChannelId(guildId)
            
        matchChannelId = client.get_channel(channelId)
        message = await matchChannelId.send(mainMessage, embed=embed)
        match = Match(message.id, channelId, guildId, player1, player2, playerChosen, False, False)

        await sendMessageToUser(client, player1, False)
        
        forfeitMessage = await sendTieOrForfeitMessage(client, match)
        match.forfeitMessage = forfeitMessage.id

        listOfMatches.append(match)
    else:
        if match.status == MatchStatus.END:
            matchChannelId = client.get_channel(GuildSettings.getMatchChannelId(guildId))
        else:
            matchChannelId = client.get_channel(getMatchChannel(match))
        message = await matchChannelId.send(mainMessage, embed=embed)
        
    if match.status == MatchStatus.STRIKING:
        await add_ban_reaction(message, listOfBans)
    elif match.status == MatchStatus.PLAYING:
        await add_victory_reaction(message)
    elif match.status == MatchStatus.RESULTS:
        await add_decision_reaction(message)
    elif match.status == MatchStatus.END:
        #await stayInQueue(client, match)
        await deleteRankedChannels(client, match)
        listOfMatches.remove(match)

    return message

def getMatchChannel(match):
    if GuildSettings.getIsMultiChannelMode(match.guild):
        return match.channel
    else:
        return GuildSettings.getMatchChannelId(match.guild)

async def createMatchChannel(client, guildId, player1, player2):
    guild = client.get_guild(guildId)
    user1 = guild.get_member(player1)
    user2 = guild.get_member(player2)

    category = await guild.create_category(user1.name.upper() + " vs. " + user2.name.upper())    

    for userRole in user1.roles:
        if userRole.name == "@everyone":
            everyoneRole = userRole
            pass
    
    textMatchChannel = await category.create_text_channel(user1.name.lower() + "-vs-" + user2.name.lower() + "-match")
    textDiscussionChannel = await category.create_text_channel(user1.name.lower() + "-vs-" + user2.name.lower() + "-discussion")
    voiceChannel = await category.create_voice_channel(user1.name.lower() + "-vs-" + user2.name.lower() + "-voice")

    botRole = getBotRole(client, guildId)

    await category.set_permissions(botRole, view_channel=True, send_messages=True)
    adminRoles = getAdminRankingRoles(client, guildId)
    for adminRole in adminRoles:
        await category.set_permissions(adminRole, view_channel=True, send_messages=True)

    await category.set_permissions(user1, view_channel=True, send_messages=False)
    await category.set_permissions(user2, view_channel=True, send_messages=False)

    await textDiscussionChannel.set_permissions(user1, send_messages=True)
    await textDiscussionChannel.set_permissions(user2, send_messages=True)

    await category.set_permissions(everyoneRole, view_channel=False)
    
    return textMatchChannel.id

async def deleteRankedChannels(client, match):
    guild = client.get_guild(match.guild)
    channel = guild.get_channel(match.channel)
    category = channel.category

    for textChannel in category.text_channels:
        await textChannel.delete()

    for voiceChannel in category.voice_channels:
        await voiceChannel.delete()

    await category.delete()

async def stayInQueue(client, match):
    queueChannel = client.get_channel(GuildSettings.getQueueChannelId(match.guild))
    message1 = await queueChannel.send("<@" + str(match.player1) + ">, if you wish to stay in queue, please react to this message.")
    await message1.add_reaction("🔁")
    message2 = await queueChannel.send("<@" + str(match.player2) + ">, if you wish to stay in queue, please react to this message.")
    await message2.add_reaction("🔁")

async def sendTieOrForfeitMessage(client, match):
    matchChannelId = client.get_channel(getMatchChannel(match))
    embed = discord.Embed(title="Tie or Forfeit?", description="Both players need to agree on tie! \nOnly one player can forfeit.")
    mainMessage = "Tie or Forfeit? \n**<@" + str(match.player1) + ">** vs. **<@"+ str(match.player2) +">**"
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

async def sendMessageToUser(client, player, rechoose, char=""):
    user = client.get_user(player)
    embed = discord.Embed(title="Example:", description="!char donkeykong \n!char dk \n!char donkey_kong")
    mainMessagePreffix = "Choose your character by sending the command **!char** *[name_or_alias_of_your_character_here]*"
    if rechoose:
        mainMessage = mainMessagePreffix + "\n Or you can react to keep the same character as before!"
    else:
        mainMessage = mainMessagePreffix

    message = await user.send(mainMessage, embed=embed)
    if rechoose:
        await message.add_reaction("🔁")

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
        await sendMessageToUser(client, userId, match.round != 1)
    else:
        ruleset = GuildSettings.getRuleset(match.guild)
        char = ruleset.getCharacterName(parts[1])
        if char == "INVALID":
            await user.send("Wrong input, please try again!")
            await sendMessageToUser(client, userId, match.round != 1)
        else:
            await user.send("You've selected: **" + char + "**")
            listToCheck.append(char)
            if match.player1 == message.author.id:
                match.player1chars = listToCheck 
            else:
                match.player2chars = listToCheck 
            
            if len(match.player1chars) != len(match.player2chars):
                if match.round == 1:
                    await sendMessageToUser(client, match.player2, match.round != 1)
                else:
                    if len(match.player1chars) < len(match.player2chars):
                        await sendMessageToUser(client, match.player1, match.round != 1, char)
                    else:
                        await sendMessageToUser(client, match.player2, match.round != 1, char)
            else:
                if match.round == 1:
                    match.status = MatchStatus.STRIKING
                else:
                    match.status = MatchStatus.PLAYING

                await resendMessage(client, match)

async def resendCharacter(client, message, reactionUserId):
    if not contains(lambda x: x.player1 == reactionUserId or x.player2 == reactionUserId):
        return

    match = get(lambda x: x.player1 == reactionUserId or x.player2 == reactionUserId)

    if match.player1 == reactionUserId:
        listToCheck = match.player1chars
        userId = match.player1
    else:
        listToCheck = match.player2chars
        userId = match.player2

    user = client.get_user(userId)

    if (match.round == 1 and listToCheck) or (match.round == 2 and len(listToCheck) != 1) or (match.round == 3 and len(listToCheck) != 2) or (match.isBo5 and match.round == 4 and len(listToCheck) != 3) or (match.isBo5 and match.round == 5 and len(listToCheck) != 4):
        await user.send("No need to select a character, you've already selected: + " + match.player1chars[-1] + "!")

    lastCharacter = listToCheck[-1]
    await user.send("You've selected: **" + lastCharacter + "**")
    listToCheck.append(lastCharacter)
    if match.player1 == reactionUserId:
        match.player1chars = listToCheck 
    else:
        match.player2chars = listToCheck 
    
    if len(match.player1chars) != len(match.player2chars):
        if match.round == 1:
            await sendMessageToUser(client, match.player2, match.round != 1)
        else:
            if len(match.player1chars) < len(match.player2chars):
                await sendMessageToUser(client, match.player1, match.round != 1, lastCharacter)
            else:
                await sendMessageToUser(client, match.player2, match.round != 1, lastCharacter)
    else:
        if match.round == 1:
            match.status = MatchStatus.STRIKING
        else:
            match.status = MatchStatus.PLAYING

        await resendMessage(client, match)

async def resendMessage(client, match):
    channel = client.get_channel(getMatchChannel(match))
    message = await channel.fetch_message(match.message)
    oldForfeitMessage = await channel.fetch_message(match.forfeitMessage)
    oldmessage = message.id
    messages = [message, oldForfeitMessage]
    await channel.delete_messages(messages)
    message = await sendMessage(client, match)
    match.message = message.id
    if match.status != MatchStatus.END:
        forfeitMessage = await sendTieOrForfeitMessage(client, match)
        match.forfeitMessage = forfeitMessage.id
    else:
        match.forfeitMessage = 0

    replace(match, lambda x: x.message == oldmessage)

def checkExistingMatch(userId):
    if contains(lambda x: x.player1 == userId or x.player2 == userId):       
        return True

    return False

def checkUserInQueue(userId):
    global waitingQueue
    if waitingQueue:
        for user in waitingQueue:
            if user.userId == userId:
                return True

    return False

async def getValidMatch(payload):
    if not contains(lambda x: (x.player1 == payload.user_id or x.player2 == payload.user_id) and x.guild == payload.guild_id):       
        return None
    match = get(lambda x: (x.player1 == payload.user_id or x.player2 == payload.user_id) and x.guild == payload.guild_id)
    if match is None:
        return None
    if payload.channel_id != getMatchChannel(match):       
        return None
    if payload.message_id != match.message and payload.message_id != match.forfeitMessage:       
        return None
    
    return match

async def getValidMatchAdmin(playerId, guildId):
    if not contains(lambda x: (x.player1 == playerId or x.player2 == playerId) and x.guild == guildId):       
        return None
    match = get(lambda x: (x.player1 == playerId or x.player2 == playerId)  and x.guild == guildId)
    if match is None:
        return None
    
    return match

async def tieOrForfeit(client, payload, match):
    flag = False
    if payload.emoji.name == "🏳️":
        flag = True
        match.forfeit(payload.user_id)
    elif payload.emoji.name == "🤝":
        channel = client.get_channel(getMatchChannel(match))
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
        await resendMessage(client, match)

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
                await sendMessageToUser(client, match.chooser, match.round != 1)

        await resendMessage(client, match)

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

        await resendMessage(client, match)

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

        await resendMessage(client, match)

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

# ADMIN COMMANDS

async def adminCancelSet(client, match):
    match.tieScore()
    await resendMessage(client, match)

async def adminDQPlayerFromSet(client, match, player):
    match.forfeit(player)
    await resendMessage(client, match)

async def adminIncrementScore(client, match, player):
    match.winner.append(player)
    match.incrementScore()
    await resendMessage(client, match)

async def adminResetSet(client, guildId, match):
    player1 = match.player1
    player2 = match.player2
    global listOfMatches
    listOfMatches.remove(match)
    await sendMessage(client, guildId=guildId, player1=player1, player2=player2)

async def adminResetMatch(client, guildId, match):
    if match.round == 1 or match.round - 1 == 1:
        await adminResetSet(client, guildId, match)
    else:
        match.reset()
        await resendMessage(client, match)

async def adminRemoveFromQueue(client, player, guild):
    global waitingQueue
    if waitingQueue:
        for user in waitingQueue:
            if user.userId == player and user.guildId == guild:
                queueChannelId = client.get_channel(GuildSettings.getQueueChannelId(guild))
                await queueChannelId.send("<@" + str(player) + ">, you have been removed from the queue by the admin!")
                waitingQueue.remove(user)
                return True
    return False

async def adminClearQueue(client, guild):
    global waitingQueue
    if waitingQueue:
        for user in waitingQueue:
            if user.guildId == guild:
                queueChannelId = client.get_channel(GuildSettings.getQueueChannelId(guild))
                await queueChannelId.send("<@" + str(user.userId) + ">, you have been removed from the queue by the admin!")
                waitingQueue.remove(user)

def adminInitServer(guildId, adminChannelId):
    initServer(guildId, adminChannelId=adminChannelId)

async def adminAddStarter(guildId, channel, message):
    text = message.content.lower()
    parts = text.split(" ", 1)
    flag = True
    if len(parts) == 2:
        ruleset = GuildSettings.getRuleset(guildId)
        stage = ruleset.getStageName(parts[1])
        if stage != "INVALID":
            for starter in ruleset.starters:
                if stage == starter:
                    flag = False
                    pass

            if flag:
                for counterpick in ruleset.counterPicks:
                    if stage == counterpick:
                        flag = False
                        pass

    if not flag:
        await channel.send("<@" + str(message.author.id) + ">, invalid input or stage already added to the list!")
    else:
        ruleset.starters.append(stage)
        GuildSettings.setRuleset(guildId, ruleset)
        await channel.send("<@" + str(message.author.id) + ">, stage added to starters: " + stage + "!")

async def adminRemoveStarter(guildId, channel, message):
    text = message.content.lower()
    parts = text.split(" ", 1)
    flag = False
    if len(parts) == 2:
        ruleset = GuildSettings.getRuleset(guildId)
        stage = ruleset.getStageName(parts[1])
        if stage != "INVALID":
            for starter in ruleset.starters:
                if stage == starter:
                    flag = True
                    pass

    if not flag:
        await channel.send("<@" + str(message.author.id) + ">, invalid input or stage not in starters!")
    else:
        ruleset.starters.remove(stage)
        GuildSettings.setRuleset(guildId, ruleset)
        await channel.send("<@" + str(message.author.id) + ">, stage removed from starters: " + stage + "!")

async def adminAddCP(guildId, channel, message):
    text = message.content.lower()
    parts = text.split(" ", 1)
    flag = False
    if len(parts) == 2:
        ruleset = GuildSettings.getRuleset(guildId)
        stage = ruleset.getStageName(parts[1])
        if stage != "INVALID":
            for counterpick in ruleset.counterPicks:
                if stage == counterpick:
                    flag = False
                    pass

            if flag:
                for starter in ruleset.starters:
                    if stage == starter:
                        flag = False
                        pass

    if not flag:
        await channel.send("<@" + str(message.author.id) + ">, invalid input or stage already added to the list!")
    else:
        ruleset.counterPicks.append(stage)
        GuildSettings.setRuleset(guildId, ruleset)
        await channel.send("<@" + str(message.author.id) + ">, stage added to counter-picks: " + stage + "!")

async def adminRemoveCP(guildId, channel, message):
    text = message.content.lower()
    parts = text.split(" ", 1)
    flag = False
    if len(parts) == 2:
        ruleset = GuildSettings.getRuleset(guildId)
        stage = ruleset.getStageName(parts[1])
        if stage != "INVALID":
            for counterpick in ruleset.counterPicks:
                if stage == counterpick:
                    flag = True
                    pass

    if not flag:
        await channel.send("<@" + str(message.author.id) + ">, invalid input or stage not in counter-picks!")
    else:
        ruleset.counterPicks.remove(stage)
        GuildSettings.setRuleset(guildId, ruleset)
        await channel.send("<@" + str(message.author.id) + ">, stage removed from counter-picks: " + stage + "!")

def adminSetDSR(guildId):
    ruleset = GuildSettings.getRuleset(guildId)
    ruleset.isDSR = True
    ruleset.isMDSR = False
    ruleset.isTSR = False
    GuildSettings.setRuleset(guildId, ruleset)

def adminSetMDSR(guildId):
    ruleset = GuildSettings.getRuleset(guildId)
    ruleset.isDSR = False
    ruleset.isMDSR = True
    ruleset.isTSR = False
    GuildSettings.setRuleset(guildId, ruleset)

def adminSetTSR(guildId):
    ruleset = GuildSettings.getRuleset(guildId)
    ruleset.isDSR = False
    ruleset.isMDSR = False
    ruleset.isTSR = True
    GuildSettings.setRuleset(guildId, ruleset)

def adminSetNoDSR(guildId):
    ruleset = GuildSettings.getRuleset(guildId)
    ruleset.isDSR = False
    ruleset.isMDSR = False
    ruleset.isTSR = False
    GuildSettings.setRuleset(guildId, ruleset)

def adminSetMultiChannel(guildId):
    GuildSettings.setIsMultiChannelMode(guildId, True)

def adminSetSingleChannel(guildId):
    GuildSettings.setIsMultiChannelMode(guildId, False)

async def adminSetCounterPickBanCount(guildId, channel, message):
    parts = message.content.split(" ", 1)
    if len(parts) != 2:
        await channel.send("<@" + str(message.author.id) + ">, invalid input!")
    else:
        count = 0
        flag = True
        try:
            count = (int)(parts[1])
        except ValueError:
            flag = False

        if flag:
            ruleset = GuildSettings.getRuleset(guildId)
            if count <= 0 or count > 3:
                flag = False
            else:
                ruleset.counterPickBans = count
                GuildSettings.setRuleset(guildId, ruleset)

        if flag:
            await channel.send("<@" + str(message.author.id) + ">, the ruleset has set " + count + " winner bans in Round 2+!")
        else:
            await channel.send("<@" + str(message.author.id) + ">, invalid number of bans!")

def adminAddStaffRole(client, guildId, roleId):
    role = getRole(client, guildId, roleId)
    adminRoles = GuildSettings.getAdminRoles(guildId)
    flag = True
    if adminRoles:
        for adminRole in adminRoles:
            if role.name == adminRole:
                flag == False
                pass
    if flag:
        adminRoles.append(role.name)
        GuildSettings.setAdminRoles(guildId, adminRoles)

    return flag

def adminRemoveStaffRole(client, guildId, roleId):
    role = getRole(client, guildId, roleId)
    adminRoles = GuildSettings.getAdminRoles(guildId)
    flag = False
    if adminRoles:
        for adminRole in adminRoles:
            if role.name == adminRole:
                adminRoles.remove(adminRole)
                flag == True
    if flag:
        GuildSettings.setAdminRoles(guildId, adminRoles)

    return flag

def adminSetRankingRole(client, guildId, roleId):
    role = getRole(client, guildId, roleId)
    GuildSettings.setRankingRole(guildId, role.name)
    
def getRole(client, guildId, roleId):
    guild = client.get_guild(guildId)
    role = guild.get_role(roleId)
    return role

def adminSetQueueChannel(guildId, channelId):
    GuildSettings.setQueueChannelId(guildId, channelId)

def adminSetMatchChannel(guildId, channelId):
    GuildSettings.setMatchChannelId(guildId, channelId)

def adminSetFlairChannel(guildId, channelId):
    GuildSettings.setFlairChannelId(guildId, channelId)

async def adminSendFlairMessage(client, guildId, message):
    channelId = GuildSettings.getFlairChannelId(guildId)
    if channelId != 0:
        channel = client.get_channel(channelId)
        if channel is not None:
            message = await channel.send("React to me! \nUse our commands that you can find by typing \"!help\"")
            await message.add_reaction("🥏")
            GuildSettings.setFlairMessageId(guildId, message.id)
            return True
    
    return False

async def adminSetFlairMessage(guildId, channel, message):
    parts = message.content.split(" ", 1)
    if len(parts) != 2:
        await channel.send("<@" + str(message.author.id) + ">, invalid input!")
    else:
        count = 0
        flag = True
        try:
            count = (int)(parts[1])
        except ValueError:
            flag = False

        if flag:
            GuildSettings.setFlairMessageId(guildId, count)
            await channel.send("<@" + str(message.author.id) + ">, the flair message has been set")
        else:
            await channel.send("<@" + str(message.author.id) + ">, invalid message!")