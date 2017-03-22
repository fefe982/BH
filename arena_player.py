# -*- coding: utf-8 -*-
import json
import io
import math
import csv

f = open("arena_player_raw.txt", "r");
YY = json.load(f)
f.close()

my_guild_id = "1538a7f9-e1e6-4a13-a54f-2a02fa121822"

card_db = {};

rarity_map = {"Common":"C", "Uncommon":"UC", "Rare":"R", "Super Rare":"SR", "Legendary":"L"};

rarity_coef = {"C":{"lvl":10,"coef":[]}};

with open("card_db.txt", "rb") as csvfile:
  csvreader = csv.reader(csvfile, delimiter="\t");
  for row in csvreader:
    if row[0] != "":
      card_db[row[0]] = {
        "name": row[2],
        "type": row[6],
        "rarity":rarity_map[row[8]],
        "target": row[10]
        };

#print YY.keys()
#print YY["members"].keys()
hero_hash = {
"b3747d9a-8820-4d04-8d06-76dec01a4862" : "Monty",
"994bc8da-1a23-4e44-a65f-b62a45bd248b" : "Fergus",
"a79dc9c1-2819-4412-873e-3ac594eb3161" : "Red",
"292751d2-d264-4b36-9fbf-84b98ddeca58" : "Bree",
"a927d4db-b4a1-46fd-9227-ba9f232dc69c" : "Thrudd",
"8db9e95c-3850-4337-8027-d4847239d857" : "Trix",
"eb4424eb-7ec0-4840-b5da-0c1d53f2c80b" : "Brom",
"2aabfd22-f6b3-4719-a668-c9dd07036d95" : "Hawkeye",
"ef412dd7-80a5-444f-aba5-be1cd8024360" : "Jinx",
"442cb574-92c2-42a8-a55b-62316b3fcf10" : "Krell",
"95e77f74-eef6-4dc4-8c21-ac3ada7301cd" : "Gilda",
"a5697501-0db3-4e4a-817e-6e866e8870e5" : "Logan",
"8d15c5d0-e621-425f-8321-781a89b73a9d" : "Peg"}

hero_hp_coef = {
"Monty"   : [4.286, 2.142, 143.572],
"Fergus"  : [6, 3, 201],
"Red"     : [4, 2, 134],
"Bree"    : [5, 2.5, 167.5],
"Thrudd"  : [38.0/7, 19.0/7, 190-38.0/7-19.0/7],
"Trix"    : [4.286, 2.142, 143.572],
"Brom"    : [5.714, 2.858, 191.438],
"Hawkeye" : [5, 2.5, 167.5],
"Jinx"    : [4, 2, 134],
"Krell"   : [5, 2.5, 167.5],
"Gilda"   : [5.714, 2.858, 191.438],
"Logan"   : [4, 2, 134],
"Peg"     : [4.5, 2, 153.5]}

f = io.open("arena_player", "w", encoding="utf8");
for p1 in YY:
  for x, p2 in p1.iteritems():
    for uid, player in p2.iteritems():
      f.write(u"{0}({1}):\n".format(player["name"], player["fameLevel"]+1));
      cards = player["playerCards"]["cards"];
      for hero in player["archetypes"]:
        f.write(u"  {0}({1}), ".format(hero_hash[hero["id"]], hero["level"]+1));
        for ability, lvl in hero["abilityLevels"].iteritems():
          abl = ability;
          f.write(u" {0}:{1} ".format(abl, lvl+1));
        f.write(u"\n");
        for card_hash in hero["deck"]:
          card = cards[card_hash];
          card_name = card["configId"];
          if card_name in card_db:
            card_info = card_db[card_name];
            f.write(u"    ({rarity:>2s},{0},{1:2d}): {type} {target} : {name}\n".format(card["evolutionLevel"], card["level"]+1, **card_info));
            card_name = "(" + card_info["rarity"] + ")" + card_info["name"] + ":" + card_info["type"] + " " + card_info["target"];
          else:
            f.write(u"    ( _,{1},{2:2d}): : {0}\n".format(card_name, card["evolutionLevel"], card["level"]+1));

f.close();          