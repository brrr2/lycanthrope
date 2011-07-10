from oyoyo.client import IRCClient
from oyoyo.parse import parse_nick
import logging
import botconfig
import wolfgame

def on_privmsg(cli, rawnick, chan, msg):         
    if chan != botconfig.NICK:  #not a PM
        for x in wolfgame.COMMANDS.keys():
            if msg.lower().startswith(x):
                h = msg[len(x):]
                if not h or h[0] == " " or not x:
                    wolfgame.COMMANDS[x](cli, rawnick, chan, h.lstrip())
    else:
        for x in wolfgame.PM_COMMANDS.keys():
            if msg.lower().startswith(x):
                h = msg[len(x):]
                if not h or h[0] == " " or not x:
                    wolfgame.PM_COMMANDS[x](cli, rawnick, h.lstrip())
    
def __unhandled__(cli, prefix, cmd, *args):
    if cmd in wolfgame.HOOKS.keys():
        largs = list(args)
        for i,arg in enumerate(largs):
            if isinstance(arg, bytes): largs[i] = arg.decode('ascii')
        wolfgame.HOOKS[cmd](cli, prefix, *largs)
    else:
        logging.debug('Unhandled command {0}({1})'.format(cmd, [arg.decode('utf_8')
                                                              for arg in args
                                                              if isinstance(arg, bytes)]))

def main():
    logging.basicConfig(level=logging.DEBUG)
    cli = IRCClient(
                      {"privmsg":on_privmsg,
                       "":__unhandled__},
                     host=botconfig.HOST, 
                     port=botconfig.PORT,
                     nickname=botconfig.NICK,
                     connect_cb=wolfgame.connect_callback
                    )
    cli.mainLoop()


if __name__ == "__main__":
    main()