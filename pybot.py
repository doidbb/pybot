#!/usr/bin/env python3.4
import socket, re, requests, json, random, os, os.path, random
from bs4 import BeautifulSoup
chans    = ['#sadbot-dev', '#/g/summer']#, '#childfree']
prefixes = ['.', ',', '>', '-', '!']
commands = ['weather', 'np', 'raw', 'addie']#, 'echo']
#todo: raw, notify and echo
#todo: work on string concat in __init__

class pybot():
    def __init__(self, nick, server, port):
        self.nick   = nick
        self.server = server
        self.port   = port
    """
    subroutine init_conn()
    initialises a socket connection 
    sets the bot's ident
    """
    def init_conn(self):
        global mysock
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialise the socket
        mysock.connect((self.server, self.port)) #connecting to address and port with socket
        nicksend = 'NICK ' + self.nick
        usersend = 'USER ' + self.nick + ' 8 * :  ' + self.nick
        print(nicksend)
        print(usersend)
        self.sendmsg(nicksend, "", "msg") 
        self.sendmsg(usersend, "", "msg") 
    """
    subroutine chan_join
    iterates through a given list of channels 
    signals irc to join said channels
    """
    def chan_join(self, listchans):
        for chan in listchans:
            self.sendmsg(chan, "", "join")
        global join
        join = True
    """
    subroutine sendmsg
    data has to be encoded to bytes before being sent
    shortcut rather than having to encode and send on different lines
    """
    def sendmsg(self, msgtosend, chan, type):
        if type == "pmsg":
            msgsend = "PRIVMSG " + chan + " :" + msgtosend + "\r\n"
        elif type == "join":
            msgsend = "JOIN " + msgtosend + "\r\n"
        elif type == "msg":
            msgsend = msgtosend + "\r\n"
        if msgtosend == " ":
            pass
        else:
            newmsg = bytes(msgsend, "utf-8") #encode data to bytes and sends to open socket
            mysock.send(newmsg)
    """
    subroutine showdata
    infinite loop, recieves data then prints it to terminal
    todo: 
        pretty formatting
        as recieving data, ensure to ping back - possibly in sendmsg()?
    """
    def showdata(self):
        while 1: #loops so program doesn't quit after one msg
            dta = ""
            dta = mysock.recv(1024) #recieves data in buffer size 1024
            print(repr(dta)) #will have to respond upon ping with pong ping
            self.parse(dta)
    """
    function parse
    like sadbot, modules/functions will be called with args
    args are data but data needs to be parsed
    regex is magic
    todo: 
        error testing
    """
    def parse(self, parseData):
        global listt
        nickV = ""
        cmd   = ""
        mydta = parseData.decode("utf-8")
        mydta = mydta.split(" ")
        nickV = re.split("\:|\!",mydta[0])
        if (len(nickV) > 1):  #let's ensure we can write to the terminal before we actually do
            nickV = nickV[1] #removes the ! between name and host, : at the begin to leave us with nick, along with regex magic
        msg = ""
        if (len(mydta) > 3): #ensures that when mydta is split, it is more than one word.
            for i in mydta[3:]:
                msg += i + " "
            chan = mydta[2]
            cmd  = mydta[3:]
            #cmd = 
        else:
            msg  = "nnull" #informs user in terminal that the message is null - nn is due to concat at front (1:)
            chan = "null" 
        #print("msg1 is: " + msg[1:])
        if cmd:
            cmdd = cmd[0][1:] #i am so hack i am so hack
            cmdd = cmdd.strip("\r\n") 
        #    print("\n")
        else:
            cmdd = "null"
        if "PING" in mydta:
            self.sendmsg("PONG PING", chan, "msg")
        print(msg) #msg[1:] == No text to send then shout again
        listt = [nickV,msg[1:].strip("\r\n"),parseData,chan,cmdd] #indexes 0,1,2,3 are nick, msg, raw, chan
        if join:
            if chan in chans:
                self.handle(listt)
    """
    subroutine handle
    passed list from parse
    temporary way to test and ensure written modules work
    todo:
        improve this doc
        improve getting weather location
    """
    def handle(self, listu): #horrible way of working out - todo: dynamic handling of output
        ran1 = random.randint(1,10)
        ran2 = random.randint(1,5)
        myregex = re.compile("(https?://)?(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)")
        print(listu[4].encode("utf-8"))
        splitt = listu[4].split(" ")
        for i in splitt:
            matcher = myregex.search(i)
            if matcher:
                self.parseYouTube(i, listu[3])
        if "kek" in listu[4].split():
            self.sendmsg("https://www.youtube.com/watch?v=8DfjKtUItsM", listu[3], "pmsg")
        for cmd in commands:
            if cmd == listu[4]:
                loc = listu[1].split(" ")
                if len(loc) <= 2:
                    self.sendmsg("invalid args", listu[3], "pmsg")
                    sender = False
                else:
                    sender = True
                    loc    = ''.join(loc[1])
                    loc    = loc.strip('\r\n') #should really remove this upon sending and recieving
        #print(listu[4].encode('utf-8').strip())

        #for pre in prefixes:
        if (listu[4] == "weather") and (sender == True):
                self.sendmsg(self.weather(loc), listu[3], "pmsg")
        elif (listu[4] == "np") and (sender == True):
            #try routine here ensures that the bot does not crash if/when last.fm is down
            try:
                self.sendmsg(self.np(loc), listu[3], "pmsg")
            except requests.exceptions.ConnectionError:
                self.sendmsg("Error, last.fm is down!", listu[3], "pmsg")
        elif (listu[4] == "raw") and (sender == True):
            self.sendmsg(self.raw(listu), listu[3], "pmsg")
        elif (listu[4] == "addie") and (sender == True):
            self.sendmsg(self.addie(listu[1]), listu[3], "pmsg")
        elif ((listu[4] == ran1) or (listu[4] == ran2)):
            self.sendmsg("That's numberwang!", listu[3], "pmsg")
            noshout = True
        elif (listu[1] == listu[1].upper()):
            self.shout(listu[1],listu[3])#, "pmsg"
        if listu[1] == "No Text to send":
            self.shout(listu[1],listu[3])
        noshout = False

    """
    function youtube
    gets data from youtube link and puts it in chat
    """
    def parseYouTube(self, url, chan): 
        newsplit = "none"
        split = url.split("https://www.youtube.com/watch?v=")
        if len(split) == 1:
            split = url.split("http://youtu.be/")
            if len(split) == 1:
                pass
            else:
                newsplit = split[1]
        if len(split) > 1:
            newsplit = split[1]
        else:
            notyoutube = True
        if newsplit != "none":
            self.sendmsg(self.youtube(newsplit), chan, "pmsg")
        else:
            self.parseURL(url, chan)  
        #return self.youtube(newsplit)
    def youtube(self, vidID):
        vidUrl = 'http://gdata.youtube.com/feeds/api/videos/' + vidID + '?v=2&alt=jsonc'
        r = requests.get(vidUrl)
        vidJSON = r.content
        vidJSON = vidJSON.decode('utf-8')
        vidJSON = json.loads(vidJSON)
        if "error" in vidJSON:
            output = "\x034Error with video URL"
        else:
            title   = vidJSON['data']['title']
            views   = str(vidJSON['data']['viewCount'])
            likes   = str(vidJSON['data']['likeCount'])
            output  = "\x035Title:\x0f " + title + ";\x037 Views:\x0f " + views + ";\x033 Likes:\x0f " + likes 
        return output

    """
    function weather
    possibly moved to own file as module
    takes location and uses json api on openweathermap
    weather, temp and location are taken from list and returned
    weather is changed from Kelvin to Celsius
    location is taken so that user can ensure that they are in the right country:
        portsmouth GB rather than portsmouth US
    todo:
        option for weather in Farenheit
        add hacky way to remove &mode=xml to ensure that the bot doesn't crash
        ensure better parsing of location
        split up chat so that can respond with 'i wonder what weather is like in n'
    """
    def weather(self, location): #i dont' like json. i like parsing using arrays
        url         = 'http://api.openweathermap.org/data/2.5/weather?q=' + location #+ '&mode=xml' #I don't like json - actually i love it
        userWeather = requests.get(url)
        userWeather = json.loads(userWeather.text)
        if userWeather['cod'] == "404":
            strweather  = "Error, no such location"
        else:
            country     = userWeather['sys']['country']
            weather     = userWeather['weather'][0]['description']
            temp        = str((round(float(userWeather['main']['temp'])) - 273)) + "C" #appends C so user knows that it's not 0K and freaks out
            strweather  = "Weather for " + location + ", " + country + " is " + weather + ", " + str(temp) #beautiful concatination
        return strweather
    """
    subroutine raw
    prints raw data to channel
    primary use: debugging
    todo:  
        send to listu 2
        send w/o self.send() as format is already raw
            or re-encode as str for it only to be decoded
            one if check for every output when 2/3 aren't bytes is redundant
    """
    def raw(self, rawData):
        return str(rawData[2])
    """
    subroutine echo
    prints a string that user sets to channel
    primary use: debugging
    """
    def echo():
        pass
    """
    function np
    uses last.fm api to find what a user is currently listening to
    uses json dict to find artist, album and track name
    todo:
        add validation for username
    """
    def np(self, user):
        url        = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + user  + "&api_key=381fb912a58423616770ce82239bc41b&format=json"
        userInfo   = requests.get(url)
        userInfo   = userInfo.text
        userInfo   = json.loads(userInfo)
        try:
            artist = userInfo["recenttracks"]['track'][0]['artist']['#text']
            album  = userInfo["recenttracks"]['track'][0]['album']['#text']
            track  = userInfo["recenttracks"]['track'][0]['name']
            outt   = user + " is now listening to \x035" + track + "\x0f by \x036" + artist + "\x0f on \x032" + album
            outt   = outt[:80]
        except KeyError:
            outt   = "no user found"
        if len(outt) > 75:
            #A JOB FOR CAPTAIN RECURSION YOU RETARD
            outt   = user + " is now listening to \x033" + track + "\x0f by \x036" + artist
            if len(outt) > 75:
                outt = user + " is now listening to \x033" + track
        if user == "help":
            outt   = " "
            self.sendmsg("Usage: np $USERNAME", listt[3], "pmsg")
            self.sendmsg("If the now playing is greater than 75 chars, it returns the \x033title\x0f only", listt[3], "pmsg")
        return outt
    """
    function addoe
    uses api of addie.cc to find a user's address for cryptocurrencies
    """
    def addie(self, inn):
        address = "http://addie.cc/api/"
        #use listt[1]
        stuff = inn.split()
        username = stuff[1]
        if len(stuff) == 2:
            userApiAddress = address + username
            outAddress = requests.get(userApiAddress)
            if username.lower() == "help":
                return "addie username cointype"
            if outAddress.text == "Username not found.":
                return "username not found"
            dictAddressesJson = json.loads(outAddress.text)
            counter = 0
            userCoins = []
            for key in dictAddressesJson:
                userCoins.append(key)
                if len(userCoins) == 1:
                    output = key + ": " + dictAddressesJson[userCoins[0]]
                elif len(userCoins) > 1:
                    addCoins = ""
                    for item in userCoins:
                        randColor = random.randint(1,10)
                        randColor = "\x03" + str(randColor)
                        addCoins += (randColor + item + " ")
                    output = username + " has " + addCoins
                else:
                    output = "User has no coins"
        elif len(stuff) >= 2:
            userApiAddress = address + username + "/" + stuff[2].lower()
            outAddress = requests.get(userApiAddress)
            output = outAddress.text
        else: 
            pass
        return output
    """
    parse
    """
    def parseURL(self, url, chan):
        try:
            r          = requests.get(url)
            header     = r.headers['content-type']
            headcheck  = header.split("text/html")
            if (header == "text/html") or (len(headcheck) > 1):
                soup   = BeautifulSoup(r.content)
                title  = soup.title.string
                sender = title + ", " + header
            else:
                sender = header
            self.sendmsg(sender, chan, "pmsg")
        except requests.exceptions.InvalidURL:
            pass
        except requests.exceptions.InvalidSchema:
            pass
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.SSLError:
            self.sendmsg("site contains invalid SSL cert", chan, "pmsg")
        """
        note to me
        you're lazy, stupid
        fix the regex
        """

    """
    function shout
    if the output is all in caps, MAKE IT LOUD
    adds that to a database, print a random one to the channel
    """
    def shout(self, msg, chan):
        shoutdb = "shouts.txt"
        if os.path.isfile(shoutdb):
            with open(shoutdb, 'r+') as shoutDatabase:
                shouts = shoutDatabase.read().split("\n")
                output = random.choice(shouts[:-1])
                if msg not in shouts[:-1]:
                    shoutDatabase.write(str(msg.strip("\r\n")))
        else:
            output = " Shout database not present!"
        self.sendmsg(output[1:], chan, "pmsg") #hacky hacky hacky

    
"""
non class-related items
initialises bot with own varialbes (perhaps a config file in future)
should chain init to join to showing data
"""
newbot = pybot("sadbot", "irc.rizon.net", 6667) 
#otherbot = pybot("nigger", "irc.freenode.net", 6697) #ow do i into multiplexing
newbot.init_conn()
newbot.chan_join(chans)
newbot.showdata()
