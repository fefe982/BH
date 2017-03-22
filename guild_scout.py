# -*- coding: utf-8 -*-
import json
import io
import math

f = open("guild_raw_info.txt", "r");
YY = json.load(f)
f.close()

my_guild_id = "1538a7f9-e1e6-4a13-a54f-2a02fa121822"

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

f = io.open("guild_scout", "w", encoding="utf8");
for k, g in YY["members"].iteritems():
    if k == my_guild_id :
        continue
    for m in g:
        t = {"Monty": 0, "Fergus": 0, "Red": 0, "Bree":0, "Thrudd":0, "Trix":0, "Brom": 0, "Hawkeye": 0, "Jinx": 0, "Krell":0, "Gilda":0, "Logan":0, "Peg":0}
        t["name"] = m["name"];
        t["lvl"] = m["fameLevel"] + 1;
        for h, lvl in m["archetypeLevels"].iteritems():
            if h in hero_hash:
                lvln = lvl + 1;
                t[hero_hash[h]] = int(math.floor(hero_hp_coef[hero_hash[h]][0]*lvln*lvln + hero_hp_coef[hero_hash[h]][1]*lvln + hero_hp_coef[hero_hash[h]][2]));
        #print t
        f.write(u"{name}\t{lvl}\t{Monty}\t{Fergus}\t{Red}\t{Bree}\t{Thrudd}\t{Trix}\t{Brom}\t{Hawkeye}\t{Jinx}\t{Krell}\t{Gilda}\t{Logan}\t{Peg}\n".format(**t))
 
f.close();