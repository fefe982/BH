# -*- coding: utf-8 -*-
import json
import io
import math
import csv

f = open("arena_player.raw", "r");
YY = json.load(f)
f.close()

my_guild_id = "1538a7f9-e1e6-4a13-a54f-2a02fa121822"

card_db = {};

rarity_map = {"Common":"C", "Uncommon":"UC", "Rare":"R", "Super Rare":"SR", "Legendary":"L"};

rarity_coef = {
  "C":{
    "lvl":10,
    "coef":[
      [[1.0,0.0], [1/1.8, 1/1.8]],
      [[0.8/1.8, 0.8/1.8], [0.0,1.0]]
      ]
    },
  "UC":{
    "lvl":20,
    "coef":[
      [[1.0, 0.0], [1.85/2.53, 1/2.53]],
      [[0.8*1.85/2.53, 0.8/2.53], [0.8/2.53, 1.8/2.53]],
      [[0.85*0.8/2.53, 0.85*1.8/2.53], [0.0, 1.0]]
      ]
    },
  "R":{
    "lvl":35,
    "coef":[
      [[1.0,0.0], [2.628/3.2264, 1/3.2264]],
      [[0.8*2.628/3.2264, 0.8/3.2264], [1.504/3.2264, 1.8/3.2264]],
      [[0.85*1.504/3.2264, 1.53/3.2264], [0.68/3.2264, 2.53/3.2264]],
      [[0.88*0.68/3.2264, 0.88*2.53/3.2264],[0.0,1.0]]
      ]
    },
  "SR":{
    "lvl":50,
    "coef":[
      [[3.90376/3.90376, 0/3.90376], [3.3652/3.90376, 1/3.90376]],
      [[2.69216/3.90376, 0.8/3.90376], [2.1536/3.90376, 1.8/3.90376]], 
      [[1.83056/3.90376, 1.53/3.90376], [1.292/3.90376, 2.53/3.90376]], 
      [[1.13696/3.90376, 2.2264/3.90376], [0.5984/3.90376, 3.2264/3.90376]], 
      [[0.53856/3.90376, 2.90376/3.90376], [0/3.90376, 3.90376/3.90376]]
      ]
    },    
  "L":{
    "lvl":60,
    "coef":[
      [[4.5914592/4.5914592, 0/4.5914592], [4.095984/4.5914592, 1/4.5914592]],
      [[3.2767872/4.5914592, 0.8/4.5914592], [2.781312/4.5914592, 1.8/4.5914592]],
      [[2.3641152/4.5914592, 1.53/4.5914592], [1.86864/4.5914592, 2.53/4.5914592]],
      [[1.6444032/4.5914592, 2.2264/4.5914592], [1.148928/4.5914592, 3.2264/4.5914592]],
      [[1.0340352/4.5914592, 2.90376/4.5914592], [0.53856/4.5914592, 3.90376/4.5914592]],
      [[0.4954752/4.5914592, 3.5914592/4.5914592], [0.0, 1.0]]
      ]
    }
  };

with open("card_db.csv", "rb") as csvfile:
  csvreader = csv.reader(csvfile);
  for row in csvreader:
    if row[0] != "":
      card_db[row[0]] = {
        "name": row[2],
        "type": row[6],
        "rarity":rarity_map[row[8]],
        "delay":int(row[9]),
        "target": row[10],
        "min": row[14],
        "max": row[15]
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

f = io.open("arena_player.out", "w", encoding="utf8");
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
            #print(card_name);
            #print(card_info["max"]);
            min_v = float(card_info["min"]);
            max_v = float(card_info["max"]);
            val = 0;
            if card_info["rarity"] in rarity_coef:
              lvl = rarity_coef[card_info["rarity"]]["lvl"];
              coef = rarity_coef[card_info["rarity"]]["coef"][card["evolutionLevel"]];
              lmin = min_v * coef[0][0] + max_v * coef[0][1];
              lmax = min_v * coef[1][0] + max_v * coef[1][1];
              #print(card_info["name"]);
              #print(lmin, lmax);
              #print(min_v, max_v);
              #print(coef);
              val = (lmax - lmin) / (lvl - 1) * card["level"] + lmin;
            f.write(u"    ({rarity:>2s},{0},{1:2d},{delay:d}, {2:7.1f}): {type} {target} : {name}\n".format(card["evolutionLevel"], card["level"]+1, val, **card_info));
          else:
            f.write(u"    ( _,{1},{2:2d}, ,      .0): : {0}\n".format(card_name, card["evolutionLevel"], card["level"]+1));

f.close();          
