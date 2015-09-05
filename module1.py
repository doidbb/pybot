def imgget():
    import requests
    from PIL import Image
    from io import StringIO
    #r = requests.get("https://i.imgur.com/psyps8h.jpg")
    #im = Image.open(StringIO(r.content))
    #im.size
    foo = Image.open(requests.get("https://i.imgur.com/psyps8h.jpg",stream=True).raw)
    print(foo.size)
    print(foo.format)


import os, io, random

shoutdb = "shouts.txt"
if os.path.isfile(shoutdb):
    with open(shoutdb, 'r') as dbShout:
        shouts = dbShout.read().split("\n")
        print(shouts)