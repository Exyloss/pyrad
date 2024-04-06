#!/usr/bin/env python3

from mpd import MPDClient

client = MPDClient()
client.connect("localhost", 6600)

def play(url):
    client.clear()
    client.add(url)
    client.play(0)

def stop():
    client.delete(0)


