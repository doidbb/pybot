broken = [
":irc.rizon.sexy NOTICE * :*** Couldn't look up your hostname (cached)",
':irc.rizon.sexy NOTICE * :*** Checking Ident',
':irc.rizon.sexy NOTICE * :*** No Ident response',
'PING :2402350712:irc.rizon.sexy 451 sadbot :You have not registered:irc.rizon.sexy 451 sadbot :You have not registered:irc.rizon.sexy 451 sadbot :You have not registered',
':irc.rizon.sexy 513 sadbot :To connect type /QUOTE PONG 2402350712' ]

for i in broken:
    if "To connect type /QUOTE" in i.split(":")[2]:
        print(i.split("/")[1].split()[1] + " " + i.split("/")[1].split()[2])