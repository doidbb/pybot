﻿#!/usr/bin/env python
import socket, re, requests, json, random, os, os.path, random,datetime
from bs4 import BeautifulSoup
from PIL import Image
from io import StringIO
from isodate import parse_duration
chans    = ('#sadbot-dev', "")#, '#wormhole')
images   = ('image/jpeg', 'image/png', 'image/gif','image/jpg')
prefixes = (':','!','.',';')
commands = ('weather', 'np', 'raw')
moduleDir = "./modules/"

class incMsg():
    def __init__(self, raw, chan, cmd, nick, msg, prefix=""):
        self.channel = chan
        self.command = cmd
        self.sender  = nick
        self.message = msg
        self.rawData = raw
        self.prefix  = prefix
    def toString(self):
        print("channel:\t ", self.channel)
        print("command:\t ", self.command)
        print("nick:\t\t ", self.sender)
        print("message:\t ", self.message)
        print("raw:\t ", self.rawData, end="\n\n")

class outMsg():
    def __init__(self, data, channel=""):
        self.content = data
        self.channel = channel
        self.msg     = ""
    def join(self):
        return "JOIN " + self.channel
    def rawMsg(self):
        return self.content
    def msgChan(self):
        return "PRIVMSG " + self.channel + " :" + self.content


class pybot():
    global sender
    sender = True
    def __init__(self, nick, server, port, verbose=False):
        self.nick    = nick
        self.server  = server
        self.port    = port
        self.conn    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.verbose = verbose
    def send(self, msg):
        msg = msg + "\r\n"
        message = bytes(msg, "utf-8")
        self.conn.send(message)
    """
    subroutine init_conn()
    initialises a socket connection
    sets the bot's ident
    """
    def init_conn(self):
        #initialise the socket
        self.conn.connect((self.server, self.port)) #connecting to address and port with socket
        nicksend = outMsg(('NICK ' + self.nick))
        usersend = outMsg(('USER ' + self.nick + ' 8 * :  ' + self.nick))
        #print(nicksend.rawMsg())
        self.send(nicksend.rawMsg())
        self.send(usersend.rawMsg())
    """
    subroutine chan_join
    iterates through a given list of channels
    signals irc to join said channels
    """
    def chan_join(self, listchans):
        for chan in listchans:
            joinCommand = outMsg("", chan)
            self.send(joinCommand.join())
            #self.sendmsg(chan, "", "join")
        global join
        join = True
    """
    subroutine showdata
    infinite loop, recieves data then prints it to terminal
    todo:
        pretty formatting
    """
    def run(self):
        while 1: #loops so program doesn't quit after one msg
            incomingData = self.conn.recv(1024) #recieves data in buffer size 1024
            #if self.verbose: print(repr(incomingData).encode('UTF-8')) #will have to respond upon ping with pong ping
            self.newParsingEngine(incomingData)
    """
    function parse
    like sadbot, modules/functions will be called with args
    args are data but data needs to be parsed
    regex is magic
    todo:
        error testing
    """

    def newParsingEngine(self, incomingData):
        decodedIncomingData = incomingData.decode("utf-8")
        splitData = decodedIncomingData.split(" ")
        try:
            possibleChannel = splitData[2]
        except IndexError:
            possibleChannel = ""
        if splitData[1] == "PRIVMSG" and possibleChannel in chans:
            rawData  = decodedIncomingData
            channel  = possibleChannel
            userNick = re.split("\:|\!", splitData[0])
            userNick = userNick[1]
            userHost = userNick[2]
            incomingMessage = ""
            userCommand = splitData[3][1:]
            for word in splitData[3:]:
                incomingMessage += word
            incomingMessage = incomingMessage[1:]
            commandPrefix = ""
            if incomingMessage[1:] in prefixes:
                commandPrefix = incomingMessage[1:]
            parsedMessage = incMsg(rawData, channel, userCommand, userNick, incomingMessage, commandPrefix)
            self.newHandler(parsedMessage)

            def newHandler(self, incomingMessage):
                pass

    def parse(self, parseData):
        global listt
        nickV = ""
        cmd   = ""
        mydta = parseData.decode("utf-8")
        mydta = mydta.split(" ")
        print("decoded data: ", mydta)
        nickV = re.split("\:|\!",mydta[0])
        if (len(nickV) > 1):  #let's ensure we can write to the terminal before we actually do
            nickV = nickV[1] #removes the ! between name and host, : at the begin to leave us with nick, along with regex magic
        msg = ""
        if (len(mydta) > 3): #ensures that when mydta is split, it is more than one word.
            for i in mydta[3:]:
                msg += i + " "
            chan = mydta[2]
            cmd  = mydta[3:]
        else:
            msg  = "nnull" #informs user in terminal that the message is null - nn is due to concat at front (1:)
            chan = "null"
        if cmd:
            cmdd = cmd[0][1:] #i am so hack i am so hack
            cmdd = cmdd.strip("\r\n")
        else:
            cmdd = "null"
        if "PING" in mydta:
            pong = outMsg("PONG PING")
            self.send(pong.rawMsg)
            #self.sendmsg("PONG PING", chan, "msg")
        listt = [nickV,msg[1:].strip("\r\n"),parseData,chan,cmdd] #indexes 0,1,2,3 are nick, msg, raw, chan, command
        #print("You want this: ", listt[4])
        curMessage = incMsg(parseData, chan, cmdd, nickV, msg[1:].strip("\r\n"))
        if (join and (chan in chans) and (len(parseData) < 150)):
            if self.verbose: print(curMessage.toString())
            #self.handle(curMessage)
    """
   this is a fucking mess
    """
    def handle(self, incoming): #horrible way of working out - todo: dynamic handling of output
        global sender
        sender = True
        global loc
        loc = ""
        cmd = incoming.command
        ran1 = random.randint(1,10)
        ran2 = random.randint(1,5)
        youtubeRegex = re.compile("(https?://)?(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)")
        for word in incoming.command:
            if youtubeRegex.search(word):
                self.parseYouTube(word, incoming.channel)#listu[3])
        for command in commands:
            if command == incoming.command:
                loc = incoming.message.split(" ")#listu[1].split(" ")
                if len(loc) <= 2:
                    errorMsg = outMsg("Invalid arguments", incoming.channel)
                    self.conn.send(errorMsg.msgChan())
                    sender = False
        if sender:
            loc = ''.join(incoming.message.split(" ")[1]).strip("\r\n")
        for pre in prefixes:
            #cmd = incoming.command#listu[4]
            if (cmd == pre+"weather") and (sender == True):
                self.sendmsg(self.weather(loc), listu[3], "pmsg")
            if (cmd == pre+"np") and (sender == True):
            #try routine here ensures that the bot does not crash if/when last.fm is down
                try:
                    self.sendmsg(self.np(loc), listu[3], "pmsg")
                except requests.exceptions.ConnectionError:
                    self.sendmsg("Error, last.fm is down!", listu[3], "pmsg")
        if (cmd == "raw") and (sender == True):
            self.sendmsg(self.raw(listu), listu[3], "pmsg")
        elif ((cmd == ran1) or (cmd == ran2)): #this decreases the entropy

            self.sendmsg("That's numberwang!", listu[3], "pmsg")
            noshout = True
        #elif ((incoming.message == incoming.message.upper()) and (len(incoming.message) > 8)):
        #    self.sendmsg(self.shout(listu[1],listu[3]),listu[3], "pmsg")#, "pmsg"
        #if listu[1] == "No Text to send":
        #    self.shout(listu[1],listu[3])
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
            if len(split) != 1:
                newsplit = split[1]
        elif len(split) > 1:
            newsplit = split[1]
        if newsplit != "none":
            self.sendmsg(self.youtube(newsplit), chan, "pmsg")
        else:
            self.chanGrab(url, chan)
        #return self.youtube(newsplit)
    def youtube(self, vidID):
        vidUrl = "https://www.googleapis.com/youtube/v3/videos?id=" + vidID +"&part=snippet,contentDetails,statistics,status&key=AIzaSyASyfv2jOYgXdDkttlr5kvOuQMBxSuTpSw" #have my api key its a gift
        vidJSON = self.jsonify(vidUrl)
        if "error" in vidJSON:
            output = "\x034Error with video URL"
        elif vidJSON == "Error":
            output = "\x034Error with video URL"
        else:
            title = vidJSON['items'][0]['snippet']['localized']['title']
            views = vidJSON['items'][0]['statistics']['viewCount']
            dur = vidJSON['items'][0]['contentDetails']['duration']
            dur = parse_duration(dur)
            timesecs = dur.total_seconds()
            dur = str(datetime.timedelta(seconds=timesecs))
            output  = "\x035Title:\x0f " + title + " :::\x037 Views:\x0f " + views + " ::: " + "\x033Duration:\x0f " + dur
        return output
    def checkvid(self,vid):
        if vid[-1] == "#":
            pass

    """
    function chanGrab
    gets information regarding a post on 4chan
    probably requires some validation when someone in irc makes it do something it's not meant to do
    """
    def chanGrab(self,url,chan):
        newsplit = url.split("boards.4chan.org")
        #print(newsplit)
        if len(newsplit) > 1:
            maybesplit = url.split("#")
            if len(maybesplit) > 1:
                url    = maybesplit[0]
            newsplit   = url.split("/")
            #print(newsplit[5])
            chanURL    = "https://a.4cdn.org/"+newsplit[3]+"/thread/"+newsplit[5]+".json"
            chanJSON   = self.jsonify(chanURL)
            if chanJSON != "Error":
                threadInfo = chanJSON['posts'][0]
                threadno   = str(threadInfo['no'])
                name       = threadInfo['name']
                replies    = str(threadInfo['replies'])
                output     = "\x035Board:\x0f "+newsplit[3]+" ::: \x037Thread Number:\x0f "+threadno+" ::: \x033Posted by:\x0f "+name+" ::: \x034Reply Count:\x0f "+replies
                self.sendmsg(output,chan,"pmsg")
        else:
            self.parseURL(url,chan)
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
           ensure better parsing of location
        split up chat so that can respond with 'i wonder what weather is like in n'
    """
    def weather(self, location): #i dont' like json. i like parsing using arrays
        url         = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + "&appid=bbc67f01cffb0e40951dbab4a4e69a87"#+ '&mode=xml' #I don't like json - actually i love it
        userWeather = self.jsonify(url)
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
        url      = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + user  + "&api_key=381fb912a58423616770ce82239bc41b&format=json"
        userInfo = self.jsonify(url)
        if userInfo != "Error":
            try:
                artist = userInfo["recenttracks"]['track'][0]['artist']['#text']
                album  = userInfo["recenttracks"]['track'][0]['album']['#text']
                track  = userInfo["recenttracks"]['track'][0]['name']
                outt   = user + " is now listening to \x035" + track + "\x0f by \x036" + artist + "\x0f on \x032" + album
                outt   = outt[:80]
            except KeyError:
                outt   = "no user found"
            except IndexError:
                outt   = "no user found"
            if len(outt) > 75:
                outt   = user + " is now listening to \x033" + track + "\x0f by \x036" + artist
                if len(outt) > 75:
                    outt = user + " is now listening to \x033" + track
            if user == "help":
                outt   = " "
                self.sendmsg("Usage: np $USERNAME", listt[3], "pmsg")
                self.sendmsg("If the now playing is greater than 75 chars, it returns the \x033title\x0f only", listt[3], "pmsg")
        else:
            outt = "Error with request"
        return outt
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
            elif header in images:
                imgStream = Image.open(requests.get(url,stream=True).raw)
                imgDimensions = imgStream.size
                imgX = str(imgDimensions[0])
                imgY = str(imgDimensions[1])
                imgType = imgStream.format
                sender = "Image type: \x035" + imgType + "\x0f ::: Dimensions:\x036 " + imgX + "\x0f x\x032 " + imgY
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
        edit:
            delegating the fixing to future me
            this code is a fucking mess
            -HJF 20/06/2015
        """

    """
    function shout
    If the message in a channel is in uppercase, this function will be triggered
    The function loads the database from the file 'shouts.txt'
    it splits the lines in the file in to an array
    the output is selected at random from the array
    if the input isn't already present it is then written to the array
    newlines are added at random, this is noise from the server that should be ignored - it's easier this way, not intuitive
    therefore, if the random selection is whitespace the function is invoked again - with a null string
    """
    def shout(self, msg, chan):
        shoutdb = "shouts.txt"
        shoutDatabase = open(shoutdb, 'r+')
        shoutDB = shoutDatabase.readlines()
        output = ""
        while ((output == "") or (output == " ")):
            output = random.choice(shoutDB)
        if msg not in shoutDB[:-1] or msg not in [" ", ""]:
            dbMessage = str(msg)
            dbMessageClean = dbMessage.strip("\r\n")
            dbMessageClean = dbMessageClean[:-1]
            print(dbMessageClean, end=' ', file=shoutDatabase)
        shoutDatabase.close()

        return output
    """
    subroutine jsonify
    paramater is the url
    this subroutine is used to request the contents of a webpage and stick it in to json form
    the website is gotten with requests.get and then put in to a dict with json.loads
    """
    def jsonify(self,url):
        try:
            r           = requests.get(url)
            jsonContent = r.content
            jsonContent = jsonContent.decode('utf-8')
            jsonContent = json.loads(jsonContent)
        except ValueError:
            jsonContent = "Error"
        except TypeError:
            jsonContent = "Error"
        return jsonContent
"""
non class-related items
initialises bot with own varialbes (perhaps a config file in future)
should chain init to join to showing data
"""
newbot = pybot("sadbot", "irc.rizon.net", 6667, True)
newbot.init_conn()
newbot.chan_join(chans)
newbot.run()
