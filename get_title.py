#!/usr/bin/env python3
'''
Get title for usage in my RSS scripts for newsboat
'''

from sys import argv
import send2playlist

title: str = send2playlist.get_title(argv[1])
if title.endswith('- YouTube'):
    title = title[:title.find('- YouTube')]
print(title)
