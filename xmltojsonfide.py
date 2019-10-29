#!/usr/bin/env python
# this script converts the FIDE xml file that contains the chess players to a .json file
# Author Alexis Vargas :)
# Excution Example : python ./xmltojsonfide.py players_list_xml_foa.xml players.json
# Excution Explanation: python_script-py json_output_file.json
# -*- coding: utf-8 -*-
import sys
import json
import requests
from pymongo import MongoClient,UpdateOne

lines = open(sys.argv[1],'r')
output = sys.argv[2]
if len(sys.argv) == 4:
	option = sys.argv[3]

test = False
url = 'http://localhost:8000'
user='admin@admin.com'
password='12345'


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

def getToken(user, password):
	data = {'email' : user,'password':password}
	response = requests.post(url+"/login",data=data)

	response = response.json()

	return response['token']



if(option!='-r' and option!='-s'):
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
			print ("Player #:" + str(num_players))
			tag_players_is_open = False
			players.append(getDataPlayer(tags_player))

			if (test==True and num_players==5):
				break
			else:
				continue

		if tag_player_is_open == True:
			tags_player.append(line.strip())
			continue


lines.close()

if option=='-r':
	auth_token=getToken(user,password)

	hed = {'Authorization': 'Bearer ' + auth_token}

	players = json.load(open(sys.argv[2],'r'))
	num_players = 0
	for player in players:
		num_players+=1
		print("Player #: "+str(num_players)+" "+str(player['fideid']))
		data = {
			'fideid':str(player['fideid']),
			'name':str(player['name']),
			'country':str(player['country']) if 'country' in player is True else '',
			'sex':str(player['sex']) if 'sex' in player is True else '',
			'title':str(player['title']) if 'title' in player is True else '',
			'w_title':str(player['w_title']) if 'w_title' in player is True else '',
			'o_title':str(player['o_title']) if 'o_title' in player is True else '',
			'foa_title':str(player['foa_title']) if 'foa_title' in player is True else '',
			'rating':str(player['rating']) if 'rating' in player is True else '',
			'games':str(player['games']) if 'games' in player is True else '0',
			'k':str(player['k']) if 'k' in player is True else '',
			'rapid_rating':str(player['rapid_rating']) if 'rapid_rating' in player is True else '',
			'rapid_games':str(player['rapid_games']) if 'rapid_games' in player is True else '0',
			'rapid_k':str(player['rapid_k']) if 'rapid_k' in player is True else '',
			'blitz_rating':str(player['blitz_rating']) if 'blitz_rating' in player is True else '',
			'blitz_games':str(player['blitz_games']) if 'blitz_games' in player is True else '0',
			'blitz_k':str(player['blitz_k']) if 'blitz_k' in player is True else '',
			'birthday':str(player['birthday']) if 'birthday' in player is True else '',
			'flag':str(player['flag']) if 'flag' in player is True else ''
		}


		response = requests.post(url+"/players",data=data, headers=hed)

		print(response.json())
elif option=='-s':
	client = MongoClient('mongodb://localhost:27018/')
	db = client.chessfyapi
	players_coll = db.players
	#count = players_coll.count_documents({})
	#print(count)
	#cursor = players_coll.find({})
	#for document in cursor:
	#	print(document)

	#operations = [
	#	UpdateOne({ "field1": 1},{ "$push": { "vals": 1 } },upsert=True),
	#	UpdateOne({ "field1": 1},{ "$push": { "vals": 2 } },upsert=True),
	#	UpdateOne({ "field1": 1},{ "$push": { "vals": 3 } },upsert=True)
	#]

	#result = players_coll.bulk_write(operations)

	players = json.load(open(sys.argv[2],'r'))
	num_players = 0
	operations = []
	for player in players:
		num_players+=1
		
		data = {
			'fideid':str(player['fideid']),
			'name':str(player['name']),
			'country':str(player['country']) if 'country' in player is True else '',
			'sex':str(player['sex']) if 'sex' in player is True else '',
			'title':str(player['title']) if 'title' in player is True else '',
			'w_title':str(player['w_title']) if 'w_title' in player is True else '',
			'o_title':str(player['o_title']) if 'o_title' in player is True else '',
			'foa_title':str(player['foa_title']) if 'foa_title' in player is True else '',
			'rating':str(player['rating']) if 'rating' in player is True else '',
			'games':str(player['games']) if 'games' in player is True else '0',
			'k':str(player['k']) if 'k' in player is True else '',
			'rapid_rating':str(player['rapid_rating']) if 'rapid_rating' in player is True else '',
			'rapid_games':str(player['rapid_games']) if 'rapid_games' in player is True else '0',
			'rapid_k':str(player['rapid_k']) if 'rapid_k' in player is True else '',
			'blitz_rating':str(player['blitz_rating']) if 'blitz_rating' in player is True else '',
			'blitz_games':str(player['blitz_games']) if 'blitz_games' in player is True else '0',
			'blitz_k':str(player['blitz_k']) if 'blitz_k' in player is True else '',
			'birthday':str(player['birthday']) if 'birthday' in player is True else '',
			'flag':str(player['flag']) if 'flag' in player is True else ''
		}
		operations.append(
			UpdateOne({ "fideid": player['fideid'] },{ "$set": data },True)
		)
		# Send once every 1000 in batch
		if ( len(operations) == 1000 ):
			percent = num_players*100/len(players)
			print("Percent inserted: "+str(percent)+" %")
			players_coll.bulk_write(operations,ordered=False)
			operations = []
	if ( len(operations) > 0 ):
		print("Player #: "+str(num_players)+" "+str(player['fideid']))
		players_coll.bulk_write(operations,ordered=False)


else:
	with open(output, 'w') as f:
	    for chunk in json.JSONEncoder().iterencode(players):
	        f.write(chunk)
