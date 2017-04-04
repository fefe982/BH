# -*- coding: utf-8 -*-
import json
import io
import math
from BHinfo import *

f = open("input.raw", "r");
YY = json.load(f)
f.close()

f = io.open("output.out", "w", encoding="utf8");
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