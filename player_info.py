# -*- coding: utf-8 -*-
import json
import io
import math
from BHinfo import *

f = open("player.raw", "r");
YY = json.load(f)
f.close()

f = io.open("player.out", "w", encoding="utf8");
print_player_info(YY, f)

f.close();          
