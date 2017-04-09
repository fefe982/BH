# -*- coding: utf-8 -*-
import json
import io
import math
import datetime
from BHinfo import *

f = open("input.raw", "r");
YY = json.load(f)
f.close()

guild_map = {};
for g in YY["guilds"]:
    guild_map[g["id"]] = {};
    guild_map[g["id"]]["name"] = g["name"];
    
player_map = {};

f = io.open("output.out", "w", encoding="utf8");
for k, g in YY["members"].iteritems():
    for m in g:
        player_map[m["playerId"]] = {};
        player_map[m["playerId"]]["guild"] = guild_map[k]["name"];
        player_map[m["playerId"]]["name"] = m["name"];
        if k == my_guild_id :
            continue
        t = {"Monty": 0, "Fergus": 0, "Red": 0, "Bree":0, "Thrudd":0, "Trix":0, "Brom": 0, "Hawkeye": 0, "Jinx": 0, "Krell":0, "Gilda":0, "Logan":0, "Peg":0}
        t["pos"] = membership_map[m["position"]];
        t["name"] = m["name"];
        t["lvl"] = m["fameLevel"] + 1;
        for h, lvl in m["archetypeLevels"].iteritems():
            if h in hero_hash:
                lvln = lvl + 1;
                t[hero_hash[h]] = int(math.floor(hero_hp_coef[hero_hash[h]][0]*lvln*lvln + hero_hp_coef[hero_hash[h]][1]*lvln + hero_hp_coef[hero_hash[h]][2]));
        #print t
        f.write(u"{pos}_{name}\t{name}\t{lvl}\t{Monty}\t{Fergus}\t{Red}\t{Bree}\t{Thrudd}\t{Trix}\t{Brom}\t{Hawkeye}\t{Jinx}\t{Krell}\t{Gilda}\t{Logan}\t{Peg}\n".format(**t))
 
for b in YY["currentWar"]["battles"]:
    t = {};
    t["i_name"] = player_map[b["initiator"]["playerId"]]["name"];
    t["i_guild"] = player_map[b["initiator"]["playerId"]]["guild"];
    t["i_score"] = b["initiator"]["totalScore"];
    t["brag"] = b["completedBragId"] != "";
    t["o_name"] = player_map[b["opponent"]["playerId"]]["name"];
    t["o_guild"] = player_map[b["opponent"]["playerId"]]["guild"];
    t["o_score"] = b["opponent"]["totalScore"];
    t["time"] = datetime.datetime.utcfromtimestamp(b["endOfBattleTimestamp"]/1000).strftime('%Y-%m-%d %H:%M:%S')
    f.write(u"{i_name}\t{i_guild}\t{i_score}\t{brag}\t{o_name}\t{o_guild}\t{o_score}\t{time}\n".format(**t));
f.close();