# Teenbot for #rteenagers - A community developed bot
import reddit # reddit_api for python
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from string import Template
import random
import time, sys
import urllib2
class MessageLogger:
    """Logging class"""
    def __init__(self, file):
        self.file = file
     
    def log(self, message): # Logging is very limited but added to give room for expansion
        """write to file"""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

class Teenbot(irc.IRCClient):
    """Teenbot IRC bot"""

    nickname = "Teenbot"
    realname = "Teenbot for \#rteenagers"
    username = "Teenbot"
    versionName = "teenBot"
    versionNum = "0.00 (Beta)"
    versionEnv = "IRC"
    source = "http://github.com/neoinr/teenbot"
    operatorlist = ['neoinr', 'keve']
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % time.asctime(time.localtime(time.time())))
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" %
                        time.asctime(time.localtime(time.time())))
        self.logger.close()
    def irc_ERR_BANNEDFROMCHAN(self, prefix, params):
        self.msg("ChanServ", "unban " + params[1] + " " + params[0])
        self.join(params[1])    
    def signedOn(self):
        """When bot has logged in, this comes!"""
        if self.nickname != "Teenbot":
            self.msg("NickServ", "GHOST Teenbot REDACTED ") #password redacted for security
        self.setNick("Teenbot")
        self.msg("NickServ", "IDENTIFY REDACTED")
        joinchan = self.factory.channel
        self.join("#teenBot")
        self.join("#rteenagers")

    def joined(self, channel):
        """When bot joins a chan, this happens"""
        self.logger.log("[I have joined %s]" % channel)
    def privmsg(self, user, channel, msg):
        """When bot gets message"""
        user = user.split('!', 1)[0]
        print msg
        if channel == self.nickname:
            """Private message"""
            pm = 1
        if user.lower() in Teenbot.operatorlist:
            sudo = 1
        else:
            sudo = 0
        if msg.startswith("+"):
            msg = msg.split(' ')
            if msg[0] == "+join":
                if sudo == 1:
                    self.join(msg[1])
            elif msg[0].lower() == "+karma":
                r = reddit.Reddit(user_agent='Teenbot')
                guy = r.get_redditor(msg[1])
                linkkrm = "Link Karma: " + str(guy.link_karma) + ", Comment Karma: " + str(guy.comment_karma) + ", Total Karma: " + str(guy.comment_karma + guy.link_karma)
                self.msg(channel, linkkrm)
            elif msg[0].lower() == "+hot":
                r = reddit.Reddit(user_agent='Teenbot')
                subs = r.get_subreddit('teenagers').get_hot(limit=5)
                substring = [str(x) for x in subs]
                num = 0
                for x in substring:
                    self.msg(channel, substring[num])
                    num = num + 1
            elif msg[0] == "+part":
                if sudo == 1:
                    self.part(channel)
            elif msg[0] == "+die":
                if sudo == 1:
                    self.msg(channel, "Ok :(")
                    self.logger.log("[died at %s]" % time.asctime(time.localtime(time.time())))
                    self.quit(message="What did I do wrong?")
                    reactor.stop()
                else:
                    self.notice(user, "You shall not pass!")
            elif msg[0] == "+restart":
                if sudo == 1:
                    self.msg(channel, "Be right back :P")
                    self.logger.log("[restarted]")
                    self.quit(message="Activate warp drive")
            elif msg[0] == "+nick":
                 if sudo == 1:
                    nich = msg[1]
                    self.setNick(nich)
                    self.nickname = nich
            elif msg[0] == "+group":
                 if sudo == 1:
                    self.msg("NickServ", "GROUP")
            elif msg[0].upper() == "+SLAPASS":
                if len(msg) == 2:
                    self.msg(msg[1], "How to do a SLAPASS:")
                    self.msg(msg[1], "just type: ")
                    self.msg(msg[1], "!add sex / location / age / photo / aspirations / sexuality / starsign")
                    self.msg(msg[1], "into the chat.")
                    self.msg(msg[1], "This sends the SLAPASS to scaledbot, which stores SLAPASSes for retrieval")
                    self.msg(msg[1], "To view someone's SLAPASS, just type \"!info user\" into the channel.")
                else:
                    self.msg(user, "How to do a SLAPASS:")
                    self.msg(user, "just type: ")
                    self.msg(user, "!add sex / location / age / photo / aspirations / sexuality / starsign")
                    self.msg(user, "into the chat.")
                    self.msg(user, "This sends the SLAPASS to scaledbot, which stores SLAPASSes for retrieval")
		    self.msg(user, "To view someone's SLAPASS, just type \"!info user\" into the channel.")
        elif msg.startswith(self.nickname + ":") or msg.startswith(self.nickname + ","):
            if "attack" in msg.lower() and sudo == 1:
                 msg = msg.split(' ')
                 atklist = open('attacks.txt')
                 attack = Template(random.choice(atklist.read().split('\n')))
                 atk = attack.substitute(inp=msg[2])
                 print msg
                 self.kick(channel, msg[2], atk)
                 atklist.close()
            if "terminate" in msg.lower() and sudo == 1:
                 msg = msg.split(' ')
                 protocols = ['ALPHA', 'BETA', 'DELTA', 'OMEGA', 'LLAMA']
                 prot = random.choice(protocols)
                 self.msg(channel, "ATTACK TYPE:  " + prot)
                 reasons = ['For Pony!', 'FOR THE HORDE!', 'NAC MAC FEEGLE!', 'Oh oh, here comes Mr Jelly!', 'Puuuuberty Poooower']
                 reason = random.choice(reasons)
                 self.kick(channel, msg[2], reason)
    def action(self, user, channel, msg):
        """When action is seen"""
        filler = 0
    def userJoined(self, user, channel):
        print user.upper()
        if "mib_" in user.lower():
            self.msg(channel, "Hi, " + user + ", welcome to #rteenagers. We will not be able to hear you unless you change your nick with /nick NEWNAME.") # Change in message suggested by Ruska.
    def userQuit(self, user, quitMessage):
        if "peer" in quitMessage:
            chance = random.randint(1, 20)
            if chance == 17:
                self.describe("#rteenagers", "glares at peer")
    def kickedFrom(self, channel, kicker, message):
        print "Kicked by %s." % kicker
        self.join(channel)
    # callbacks
    def modeChanged(self, user, channel, set, modes, args):
        if modes == "o" and set == False and self.nickname in args:
            self.msg("ChanServ", "op " + channel + " " + self.nickname)
            self.msg(channel, "nou")
            user = user.split('!', 1)[0]
            self.msg("ChanServ", "deop " + channel + " " + user)
    def userKicked(self, kickee, channel, kicker, message):
        kickee = kickee.split('!', 1)[0]

    def irc_NICK(self, prefix, params):
        """When someone changes their nick."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]

    def alterCollidedNick(self, nickname):
        """Deforms nick to let him in"""
        return "Not" + nickname



class TeenbotFactory(protocol.ClientFactory):
    """Make some Teenbots. New bot every connection"""

    def __init__(self, channel, filename):
        self.channel = channel
        print "Teenbot by Robin 'Neoinr' Elden"
        self.filename = filename

    def buildProtocol(self, addr):
        p = Teenbot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """reconnect if disconnected"""
        connector.connect()



    def clientConnectionFailed(self, connector, reason):
        print "Connection failed: ", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)

    # create factory protocol and application
    f = TeenbotFactory("#rteenagers", "log")

    # connect factory to this host and port
    reactor.connectTCP("irc.foonetic.net", 6667, f)

    # run bot
    reactor.run()

