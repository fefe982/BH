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
'''
traits_hash = {
#Monty
"ebedb4eb-8879-451a-b023-53381bf4c106": {
    "name": "Meteor",
    "desp": "Attack All {}" #89, 17567
  },
"14d7b42f-d97d-4091-98e9-b3b986b7051e": {
    "name": "Rally Party",
    "desp": "Party AtkUp {}" #76, 1742
  },
"8e5d42fa-c6af-44d3-b61d-ebe6b94f161e": {
    "name": "Protection",
    "desp": "Defense Cards Up {}" #61, 2030
  },
#Fergus
"5ac32330-545f-4cae-9edc-": {
    "name": "Magnet",
    "desp": "DefUp, Return Dmg {}" #89 82% 10227
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Fire Breath",
    "desp": "Ramdon Atk {}" #76 3372
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Thumbs Up",
    "desp": "AtkUp {}" #61 1620
  },
#Red
"5ac32330-545f-4cae-9edc-": {
    "name": "Death Trap",
    "desp": "Atk All {}, 35% Bleed" #89 14712
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Flash Bang"
    "desp": "Atk All {}, Acc Dn" #76 1806;; 55 60
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Blood Rush"
    "desp": "Bleed DmgUp {}" #61 2365
  },
#Bree
"5ac32330-545f-4cae-9edc-": {
    "name": "Remedy Rush",
    "desp": "Heal Party {}" #89 12115
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Healing Kiss",
    "desp": "Heal Party {}" #67 3372
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Full Hearts"
    "desp": "Party MaxHP Up" #61 2030
  },
#Thrudd
"5ac32330-545f-4cae-9edc-": {
    "name": "Hippy Shake",
    "desp": "Atk All {}" #89 13223
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Vegan Guff",
    "desp": "Poison Dmg {}" #67 2136
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Vengeance ",
    "desp": "AtkUp {}, DefUp {}" #61 85% 45%
  },
#Trix
"5ac32330-545f-4cae-9edc-": {
    "name": "Soul Drain"
    "desp": "Drain Trait {}, Leech Health {}", #89 28647, 6954
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Spellbound",
    "desp": "Weaken to Magic {}", #67 2517
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Wizardry",
    "desp": "Magic AtkUp {}" #61 1185
  },
#Brom
"5ac32330-545f-4cae-9edc-": {
    "name": "Holy Sword", # 89, 20891
    "desp": "Attack All {}" 
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Stronghold",
    "desp": "Party Shield {}" # 76, 3372
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Resurrect",
    "desp": "resurrect at {}" # 61, 12200
  },
#Hawkeye
"606a9247-535e-4733-ba83-b98224e2860b": {
    "name": "Whirl Wind",
    "desp": "Attack All {}" #20468, 89; 37 3750; 39 3944
  },
"1e259702-9ae1-4a19-9fb9-933df6f64bd6": {
    "name": "Focus",
    "desp": "Weaken to Ranged {}" #2517, 76; 23 445; 24 468
  },
"5cc06ef9-c400-4537-b554-75238d9efcee": {
    "name": "Sharpen",
    "desp": "1-turn Attack Up {}%", # %85 61
    "coef": [0, 1.25, 8.75]
  },
#Jinx
"2586e4ac-e0dd-4a9c-bd9a-cf2cbcba8c5d": {
    "name": "The Dropper"
    "desp": "Atk All {}", #89 19473
  },
"bccd8f3b-1fbc-4840-970f-891b0bc2aaf5": {
    "name": "Steal Life",
    "desp": "Leech {}" #61 2424
  },
"834b9969-d6a7-4058-a788-51e5e4df38aa	": {
    "name": "Increase Loot",
    "desp": "Gold Up {}%", #76 40.5
    "coef": [0, 0.5, 2.5]
  },
#Krell
"e69927a2-6950-4602-8ba1-9ba34eb8dc1e": {
    "name": "Haunt",
    "desp": "DefDn {}%, AtkAll {}" #89 42% 12252
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Curse",
    "desp": "Rnd DefDn {}" #76 2512
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Wrath",
    "desp": "MaxHP Dn {}" #61 2030
  },
#Gilda
"5ac32330-545f-4cae-9edc-": {
    "name": "Shield Maiden",
    "desp": "AtkAll {}, 40% CHILL"
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Battle Horn",
    "desp": "Charge Traits {}"
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "Defender",
    "desp": "Shield Up {}"
  },
#Logan
"5ac32330-545f-4cae-9edc-095ba5065e67": {
    "name": "WaterWall",
    "desp": "Bonus Water Dmg {}%, Return Dmg {}"
  },
"d6e0e8d8-d955-403a-8290-e966475bab33": {
    "name": "Holy Water",
    "desp": "Heal Self {}/Cure Party"
  },
"8b942c09-dc3e-4da2-a200-53524c02fbb5": {
    "name": "Angels Kiss",
    "desp": "Heal Cards Up {}"
  },
#Peg
"5ac32330-545f-4cae-9edc-": {
    "name": "Ghost Ship",
    "desp": "Atk All {}, Party Shield {}"
  },
"d6e0e8d8-d955-403a-8290-": {
    "name": "Wind to the Sails",
    "desp": "Air Card Atk Bonus {}, Self Air Dmg Bonus {}"
  },
"8b942c09-dc3e-4da2-a200-": {
    "name": "See log",
    "desp": "... AtkUp {}"
  },
}
'''
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
