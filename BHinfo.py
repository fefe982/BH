import csv
import math

my_guild_id = "1538a7f9-e1e6-4a13-a54f-2a02fa121822"

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

traits_hash = {
#Monty
"ebedb4eb-8879-451a-b023-53381bf4c106": {
    "name": "Meteor",
    "desp": "Attack All {}", #89, 17567
    "coef": [2.15, 5.2, 74.65]
  },
"14d7b42f-d97d-4091-98e9-b3b986b7051e": {
    "name": "Rally Party",
    "desp": "Party AtkUp {}", #76, 1742
    "coef": [0.2, 7.1, 47.7]
  },
"8e5d42fa-c6af-44d3-b61d-ebe6b94f161e": {
    "name": "Protection",
    "desp": "Defense Cards Up {}", #61, 2030
    "coef": [0.25, 14.5, 215.25]
  },
#Fergus
"18c1da01-f364-4d5b-8d54-b517c4d8f9e7": {
    "name": "Magnet",
    "desp": "DefUp {}, Return Dmg {}", #89 82% 10227
    "coef": [0, 0.25, 59.75, 1.25, 3.2, 41.55]
  },
"5eb58b62-5a3b-4cdf-98e8-ee2747bd1697": {
    "name": "Fire Breath",
    "desp": "Ramdon Atk {}", #76 3372
    "coef": [0.4, 12.7, 96.9]
  },
"727e60a1-4851-49bd-867d-8092da1e02b9": {
    "name": "Thumbs Up",
    "desp": "AtkUp {}", #61 1620
    "coef": [0.2, 11.6, 168.2]
  },
#Red
"23552184-88f9-427e-9e37-a0180198f767": {
    "name": "Death Trap",
    "desp": "Atk All {}, 35% Bleed", #89 14712
    "coef": [1.8, 4.5, 62.7]
  },
"022f7397-eba7-4e2b-8e27-e862f02170d4": {
    "name": "Flash Bang",
    "desp": "Atk All {:.1f}, Acc Dn", #76 1806;; 55 60
    "coef": [0.2421,4.7072,50.0507]
  },
"6614e24f-ca08-443a-8d82-a6c350a51971": {
    "name": "Blood Rush",
    "desp": "Bleed DmgUp {}" #61 2365
  },
#Bree
"3421fa4e-2672-468d-b1e1-de51adcccbfa": {
    "name": "Remedy Rush",
    "desp": "Heal Party {}" #89 12115
  },
"aa6745ad-af30-43ad-9f4e-30a75b6a35c9": {
    "name": "Healing Kiss",
    "desp": "Heal Party {}", #67 3372
    "coef": [0.4, 12.7, 96.9]
  },
"f7c25be7-e88c-4d34-b4ed-7bbf83bab6d6": {
    "name": "Full Hearts",
    "desp": "MaxHP Up {}", #61 2030
    "coef": [0.25, 14.5, 215.25]
  },
#Thrudd
"554b4bdb-7296-4748-99a6-2f8c7d6d2dce": {
    "name": "Hippy Shake",
    "desp": "Atk All {}", #89 13223
    "coef": [1.62, 3.76, 56.62]
  },
"e7a9389b-ea2b-4669-829c-251cd3fcf9f5": {
    "name": "Vegan Guff",
    "desp": "Poison Dmg {}", #67 2136
    "coef": [0.25, 8.3, 61.45]
  },
"39b74e66-db90-4e07-b2be-b0d4c9646886": {
    "name": "Vengeance ",
    "desp": "AtkUp {}%, DefUp {}%", #61 85% 45%
    "coef": [0, 1, 24, 0, 0.5, 14.5]
  },
#Trix
"95f4115f-0ca2-46b9-8184-dd312f9d2bbd": {
    "name": "Soul Drain",
    "desp": "Drain Trait {}, Leech Health {}", #89 28647, 6954
    "coef": [3.5, 9, 122.5, 0.85, 2.15, 30]
  },
"98eb0342-eca2-4c35-a535-07c50467aff6": {
    "name": "Spellbound",
    "desp": "Weaken to Magic {}", #67 2517
    "coef": [0.3, 9.4, 70.3]
  },
"db847be0-5661-47d8-8bb6-81864049fd3d": {
    "name": "Wizardry",
    "desp": "Magic AtkUp {}", #61 1185
    "coef": [0.16,7.68, 122.16]
  },
#Brom
"2be69fcf-9844-4ab9-b1d5-511935cf5f35": {
    "name": "Holy Sword", # 89, 20891
    "desp": "Attack All {}" 
  },
"5e6e28d4-ffea-4c25-bd8f-76b82604bdd8": {
    "name": "Stronghold",
    "desp": "Party Shield {}" # 76, 3372
  },
"816fd66b-e94b-457d-bbc2-a09ce3fa8a26": {
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
    "desp": "1T Atk Up {:.1f}%", # %85 61
    "coef": [0, 1.25, 8.75]
  },
#Jinx
"2586e4ac-e0dd-4a9c-bd9a-cf2cbcba8c5d": {
    "name": "The Dropper",
    "desp": "Atk All {}", #89 19473
  },
"834b9969-d6a7-4058-a788-51e5e4df38aa": {
    "name": "Steal Life",
    "desp": "Leech {}" #61 2424
  },
"bccd8f3b-1fbc-4840-970f-891b0bc2aaf5": {
    "name": "Increase Loot",
    "desp": "Gold Up {}%", #76 40.5
    "coef": [0, 0.5, 2.5]
  },
#Krell
"e69927a2-6950-4602-8ba1-9ba34eb8dc1e": {
    "name": "Haunt",
    "desp": "DefDn {}%, AtkAll {}" #89 42% 12252
  },
"9565f8a1-f16d-4ea3-bb88-7b54286d905f": {
    "name": "Curse",
    "desp": "Rnd DefDn {}" #76 2512
  },
"14aea8dc-6733-4784-91df-beb14dcb36a0": {
    "name": "Wrath",
    "desp": "MaxHP Dn {}", #61 2030
    "coef": [0.25, 14.5, 215.25]
  },
#Gilda
"f378d47c-1021-4c3a-a791-2421d153caaa": {
    "name": "Shield Maiden",
    "desp": "AtkAll {}, 40% CHILL"
  },
"bb56f5dc-5fa4-4d99-b8ca-0457f2475d3b": {
    "name": "Battle Horn",
    "desp": "Charge Traits {}"
  },
"8a08836d-b97b-4a72-ad37-5cec214e84a6": {
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
"ba88d770-c073-49a7-b69d-6d695b4ee9ca": {
    "name": "Ghost Ship",
    "desp": "Atk All {}, Shld {}"
  },
"e6f381ba-1589-4af4-868a-1421dba8b556": {
    "name": "Wind to the Sails",
    "desp": "Air C Atk Bonus {}, Slf Air Dmg Bonus {}"
  },
"71a9852e-9c9e-4dc4-84c7-e1307ba9a425": {
    "name": "See Legs",
    "desp": "... AtkUp {}"
  },
}


card_db = {};

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

def print_player_info(player, f):
  f.write(u"{0}({1}):\n".format(player["name"], player["fameLevel"]+1));
  cards = player["playerCards"]["cards"];
  for hero in player["archetypes"]:
    h_name = hero_hash[hero["id"]];
    h_lvl = hero["level"]+1;
    h_hp = int(math.floor(hero_hp_coef[h_name][0]*h_lvl*h_lvl + hero_hp_coef[h_name][1]*h_lvl + hero_hp_coef[h_name][2]))
    f.write(u"  {0}({1}:{2}), ".format(h_name, h_lvl, h_hp));
    for ability, lvl in hero["abilityLevels"].iteritems():
      abl_desp = ""
      abl = ability
      lvl = lvl + 1
      if ability in traits_hash:
        abl = traits_hash[ability]["name"];
        abl_desp = traits_hash[ability]["desp"];
        if "coef" in traits_hash[ability]:
          coef = traits_hash[ability]["coef"];
          i = len (coef)/3
          arr = []
          #print (coef);
          #print i;
          for j in xrange(0, i):
            #print j;
            arr.append(coef[j*3]*lvl*lvl + coef[j*3+1]*lvl + coef[j*3+2]);
            #print(arr)
          #print (arr)
          abl_desp = abl_desp.format(*arr);
      f.write(u" {0}({2}):{1} ".format(abl, lvl, abl_desp));
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