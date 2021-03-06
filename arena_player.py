# -*- coding: utf-8 -*-
import json
import io
import math
from BHinfo import *

f = open("input.raw", "r");
YY = json.load(f)
f.close()

f = io.open("output.out", "w", encoding="utf8");
for p1 in YY:
  for x, p2 in p1.iteritems():
    for uid, player in p2.iteritems():
      print_player_info(player, f)

f.close();          
