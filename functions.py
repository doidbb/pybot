#!/usr/bin/env python
import re, requests
from bs4 import Beautifulsoup
def parseurl(url):
    ourInfo = ""
    imgDL1 = BeautifulSoup(url)
    imgDL = requests.get(url)
    imgInfo = imgDL.headers['content-type']
    urltitle = imgDL1.title.string
    return urltitle + imgInfo
