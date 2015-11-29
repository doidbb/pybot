#!/usr/bin/env python3
import os

msgNotPresent = "OI U KUNT HARI"
msgPresent    = "TOSSER\n"
shoutDB       = "shouts.txt"

shoutDatabase = open(shoutDB, 'r+')
if msgPresent in shoutDatabase.readlines():

