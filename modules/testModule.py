#!/usr/bin/env python

class pybotModule():
    def __init__(self):
        self.name = "testModule"
        self.commands = ("test", "testo")
    def main(self):
        return "This is a test"
    def toString(self):
        ret = "I am " + self.name + "my commands are: "
        for command in self.commands:
            ret += command + " "
        return ret
