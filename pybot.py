#!/usr/bin/env python

import socket

network = "irc.rizon.net"
port = 6660
username = "sadpy"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((network, port)) #server name and port

s.send('NICK sadpy\r\n')
s.send('USER sadpy sadpy sadpy :sadpy sadpy\r\n')
s.send('JOIN #sadbot-dev \r\n')

while 1:
  global data
  data = s.recv(1024)
  print data
  msg = data.split(':')[2]
  if not msg[0]:
    command = "nulll"
  else:
    command = msg[0]
  print command


def parse():
  nick = data.split('!')[0]
  nick = nick.replace(":", "")

  msg = data.split(':')[2]
  command = msg[0]

  chan = data.split()[2]
