#!/usr/bin/env python3.4
import socket, re, requests, json, random, os, os.path, random,datetime
from bs4 import BeautifulSoup
from PIL import Image
from io import StringIO
from isodate import parse_duration
chans    = ('#sadbot-dev', '#/g/summer', '#wormhole')
images   = ('image/jpeg', 'image/png', 'image/gif','image/jpg')
triggers = ('woof', 'kek','lel','coffee','andri','noice')
prefixes = (':','!','.',';')
commands = ('weather', 'np', 'raw')

class pybot():
    global sender 
    sender = True
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
        #print(msg) #msg[1:] == No text to send then shout again
        listt = [nickV,msg[1:].strip("\r\n"),parseData,chan,cmdd] #indexes 0,1,2,3 are nick, msg, raw, chan, command
        if join:
            if chan in chans:
                if len(parseData) < 150:
                    self.handle(listt)
    """
   this is a fucking mess
    """
    def handle(self, listu): #horrible way of working out - todo: dynamic handling of output
        global sender
        global loc
        loc = ""
        ran1 = random.randint(1,10)
        ran2 = random.randint(1,5)
        myregex = re.compile("(https?://)?(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)")
        print(listu[4].encode("utf-8",'ignore'))
        splitt = listu[4].split(" ")
        for i in splitt:
            matcher = myregex.search(i)
            if matcher:
                self.parseYouTube(i, listu[3])
        print(str(listu[1].split()))
        for word in triggers:
            if word in listu[1].split():
                self.sendmsg("\x03"+str(random.randint(1,7))+word+"\x03"+str(random.randint(1,7))+" "+word+"\x03"+str(random.randint(1,7))+" "+word, listu[3], "pmsg") #shit nigga
        for cmd in commands:
            if cmd == listu[4]:
                loc = listu[1].split(" ")
                if len(loc) <= 2:
                    self.sendmsg("invalid args", listu[3], "pmsg")
                    sender = False
                else:
                    sender = True
        if sender:
            loc = ''.join(listu[1].split(" ")[1])
            loc = loc.strip('\r\n') 
        for pre in prefixes:
            cmd = listu[4]
            if (cmd == pre+"weather") and (sender == True):
                self.sendmsg(self.weather(loc), listu[3], "pmsg")
            elif (cmd == pre+"np") and (sender == True):
            #try routine here ensures that the bot does not crash if/when last.fm is down
                try:
                    self.sendmsg(self.np(loc), listu[3], "pmsg")
                except requests.exceptions.ConnectionError:
                    self.sendmsg("Error, last.fm is down!", listu[3], "pmsg")
            cmd = ""
        if (listu[4] == "raw") and (sender == True):
            self.sendmsg(self.raw(listu), listu[3], "pmsg")
        elif ((listu[4] == ran1) or (listu[4] == ran2)): #this decreases the entropy

            self.sendmsg("That's numberwang!", listu[3], "pmsg")
            noshout = True
        elif ((listu[1] == listu[1].upper()) and (len(listu[1]) > 6)):
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
            newsplit   = url.split("/")
            #print(newsplit[5])
            chanURL    = "https://a.4cdn.org/"+newsplit[3]+"/thread/"+newsplit[5]+".json"
            chanJSON   = self.jsonify(chanURL)
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
        url         = 'http://api.openweathermap.org/data/2.5/weather?q=' + location #+ '&mode=xml' #I don't like json - actually i love it
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
        try:
            artist = userInfo["recenttracks"]['track'][0]['artist']['#text']
            album  = userInfo["recenttracks"]['track'][0]['album']['#text']
            track  = userInfo["recenttracks"]['track'][0]['name']
            outt   = user + " is now listening to \x035" + track + "\x0f by \x036" + artist + "\x0f on \x032" + album
            outt   = outt[:80]
        except KeyError:
            outt   = "no user found"
        if len(outt) > 75:
            outt   = user + " is now listening to \x033" + track + "\x0f by \x036" + artist
            if len(outt) > 75:
                outt = user + " is now listening to \x033" + track
        if user == "help":
            outt   = " "
            self.sendmsg("Usage: np $USERNAME", listt[3], "pmsg")
            self.sendmsg("If the now playing is greater than 75 chars, it returns the \x033title\x0f only", listt[3], "pmsg")
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
        if os.path.isfile(shoutdb):
            with open(shoutdb, 'r+') as shoutDatabase:
                shouts = shoutDatabase.read().split("\n")
                output = random.choice(shouts[:-1])
                if msg not in shouts[:-1] or msg not in [ " ", ""] :
                    try:
                        shoutDatabase.write((str(" " + (str(msg.strip("\r\n"))))).encode('UTF-8','ignore') )
                    except UnicodeEncodeError: #nice habit faggot
                        pass
                    except TypeError:
                        pass
        else:
            output = " SHOUT DATABASE NOT PRESENT SPASTIC"
        if output != '':
            self.sendmsg(output[2:], chan, "pmsg") #hacky hacky hacky
            shoutDatabase.close()
        else:
            print("no data") #muh debug
            self.shout("",chan)
    """
    subroutine jsonify
    paramater is the url
    this subroutine is used to request the contents of a webpage and stick it in to json form
    the website is gotten with requests.get and then put in to a dict with json.loads
    """
    def jsonify(self,url):
        r          = requests.get(url)
        jsonContent= r.content
        jsonContent = jsonContent.decode('utf-8')
        jsonContent = json.loads(jsonContent)
        return jsonContent
"""
non class-related items
initialises bot with own varialbes (perhaps a config file in future)
should chain init to join to showing data
"""
newbot = pybot("sadbot", "irc.rizon.net", 6667) 
newbot.init_conn()
newbot.chan_join(chans)
newbot.showdata()
