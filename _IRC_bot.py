from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
from twisted.internet import defer


class IRCLogger(irc.IRCClient):
  #logfile = file('/tmp/hanirc.txt', 'a+')

    nickname = 'dice_bot'
    CHANNEL = '#bottest'

    def signedOn(self):
      self.join('#bottest')

    def joined(self, channel):
      """This will get called when the bot joins the channel."""
      print channel

    def got_names(self,nicklist):
      print nicklist

    def callAll(self, nicklist, message, user):
      #self.sendline(' '.join(nicklist))
      self.msg(self.CHANNEL, user.split('!')[0]+":"+message +" "+ ' '.join(nicklist))

    def privmsg(self, user, channel, message):
      print "[got msg]%s" % message
      print "2", self.CHANNEL
      #self.msg(message, self.CHANNEL)

      if message.startswith("callAll"):             
        print "accepted"
        splited = message.split(" ",1)[1:]
        if len(splited) > 0 :
          msg = splited[0]
        else :
          msg = ""
        self.names("#bottest").addCallback(self.callAll, msg, user)

      #self.logfile.write(" %s said %s \n" % ( user.split('!')[0], message ))
      #self.logfile.flush()

    def __init__(self, *args, **kwargs):
      self._namescallback = {}

    def names(self, channel):
      channel = channel.lower()
      d = defer.Deferred()
      if channel not in self._namescallback:
        self._namescallback[channel] = ([], [])

      self._namescallback[channel][0].append(d)
      self.sendLine("names %s" % channel)
      return d

    def irc_RPL_NAMREPLY(self, prefix, params):
      channel = params[2].lower()
      nicklist = params[3].split(' ')

      if channel not in self._namescallback:
        return

      n = self._namescallback[channel][1]
      n += nicklist

    def irc_RPL_ENDOFNAMES(self, prefix, params):
      channel = params[1].lower()
      if channel not in self._namescallback:
        return

      callbacks, namelist = self._namescallback[channel]

      for cb in callbacks:
        cb.callback(namelist)

      del self._namescallback[channel]

def main():
  f = protocol.ReconnectingClientFactory()
  f.protocol = IRCLogger
  reactor.connectTCP('apink.hanirc.org', 6667, f)
  reactor.run()

if __name__ == '__main__':
  main()
