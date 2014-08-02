#!/usr/bin/env python

import socket

network = "irc.rizon.net"
port = 6660
username = "sadpy"
ident = username
nick = username
ident1 = "USER " + ident + " 0 1 :" + username
ident2 = "NICK " + nick

def init(servname, servport):
    global s
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    s.connect((servname, servport)) #server name and port
    s.send('NICK %s\n' %nick)
    s.send('USER %s 0 1 : %s\n' %(nick, nick))
    mainloop()
def mainloop():
    while 1:
        global data
        data = s.recv(1024)
        print data

#def parse():


if __name__ == '__main__':
    init(network,port)
