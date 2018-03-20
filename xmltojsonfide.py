#!/usr/bin/env python
# this script converts the FIDE xml file that contains the chess players to a .json file
# Author Alexis Vargas :)
# Excution Example : python ./xmltojsonfide.py players_list_xml_foa.xml players.json
# Excution Explanation: python_script-py json_output_file.json
# -*- coding: utf-8 -*-
import sys
import json

lines = open(sys.argv[1],'r')
output = sys.argv[2]


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getTextIntoTags(tag):
	return find_between(tag,'>','</')

def getTagName(tag):
	return find_between_r(tag,'</','>')

def getDataPlayer(tags_player):
	data_player={}
	for tag in tags_player:
		index = getTagName(tag)
		value = getTextIntoTags(tag)
		data_player[index] = value

	return data_player

tag_players_is_open = False
tag_player_is_open = False
tags_player = []
players = []
num_players = 0
for index, line in enumerate(lines):
	#if(index==99999):
	#	break

	if line.strip()=="<playerslist>":
		tag_players_is_open = True
		continue
	elif line.strip()=="</playerslist>":
		tag_players_is_open = False
		continue
	elif line.strip()=="<player>":
		tags_player = []
		tag_player_is_open = True
		continue
	elif line.strip()=="</player>":
		num_players+=1
		print "Player #: "+str(num_players)
		tag_players_is_open = False
		players.append(getDataPlayer(tags_player))
		continue
	
	if tag_player_is_open == True:
		tags_player.append(line.strip())
		continue
	

lines.close()

f = open(output,"w+")
f.write(json.dumps(players))
f.close()