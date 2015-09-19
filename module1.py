#import requests
#from PIL import Image
#from io import StringIO
##r = requests.get("https://i.imgur.com/psyps8h.jpg")
##im = Image.open(StringIO(r.content))
##im.size
#foo = Image.open(requests.get("https://i.imgur.com/psyps8h.jpg",stream=True).raw)
#print(foo.size[0])
#print(foo.size[1])
#rq = requests.get("https://i.imgur.com/psyps8h.jpg")
#print(rq.headers['content-type'])

def factorial(num):
    if num != 1:
      return factorial(num -1) * num
    else:
        return 1

import requests,json 
#id = "X9mGQU7rGGM"
#id = "U4oB28ksiIo"
id = "6grVJyS-ap4"
r = requests.get("https://www.googleapis.com/youtube/v3/videos?id=" + id +"&part=snippet,contentDetails,statistics,status&key=AIzaSyASyfv2jOYgXdDkttlr5kvOuQMBxSuTpSw")
vidJSON = r.content
vidJSON = vidJSON.decode('utf-8')
vidJSON = json.loads(vidJSON)
title = vidJSON['items'][0]['snippet']['localized']['title']
views = vidJSON['items'][0]['statistics']['viewCount']
likes = vidJSON['items'][0]['contentDetails']['duration']
likes = likes[2:]
hour = ""
min  = ""
sec  = likes[-3:]
if "H" in likes:
    hour = likes.split("H")[0] + ":"
if "H" and "M" in likes:
    min = likes.split("M")[0][2:] + ":"
if ("M" in likes) and ("H" not in likes):
    min = likes.split("M")[0] + ":"
if "M" in sec:
    sec = sec[1:][:1]
else:
    sec = sec[:2]
time = hour+min+sec
output = "Title: " + title + " ::: " + "Views: " + views + " ::: " + "Duration: " + time
print(output)