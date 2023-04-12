import re, json, math, random, requests, pandas as pd
from colorama import Fore, Back, Style, init
from replit import db
from tabulate import tabulate

init(autoreset=True)

pokedex = json.loads(open('pokedex.txt').read())

movesdata = json.loads(open('moves.txt').read())
moves = movesdata.keys()
moves_formatted = open('allmoves.txt').read().splitlines()
#print(pokedex["cofagrigus"]["abilities"]["0"])

#chrstc_list = list(pokedex["bulbasaur"].keys())

#------------- test for data | UNUSED; FOR TESTING -------------#

def init_data():
  pokemon_test = input("Select your Pokemon. ").lower()
  
  for count, chrstc in enumerate(chrstc_list):
    print(count, "-", chrstc)
  
  chrstc = int(input("Select a characteristic to view. Indices only. "))
  print(pokedex[pokemon_test][chrstc_list[chrstc]])

#------------ select pokemon -------------#
  
def ask_selectPKMN():
  global p1_pokemon, p1_level, p1_nature
  global p2_pokemon, p2_level, p2_nature
  
  print(Fore.RED + "Player 1, select your Pokemon:", end=' ')
  p1_pokemon = input().lower()
  if p1_pokemon == 'test':
    return 'test'

  print(Fore.RED + "(Type 'help' for Nature information)\nNature:", end=' ')
  p1_nature = input().title()
  if p1_nature == 'Help':
    list_natures(); print(Fore.RED + "\nNature:", end=' '); p1_nature = input().title()
  
  print(Fore.RED + "Level:", end=' ')
  p1_level = int(input())
  
  print(Fore.BLUE + "Player 2, select your Pokemon:", end=' ')
  p2_pokemon = input().lower()

  print(Fore.BLUE + "Nature:", end=' ')
  p2_nature = input().title()
  if p2_nature == 'Help':
    list_natures(); print(Fore.BLUE + "\nNature:", end=' '); p2_nature = input().title()

  print(Fore.BLUE + "Level:", end=' ')
  p2_level = int(input())


#------------- list natures in selection -------------#

def list_natures():
  print('\n'+'\n'.join(open('natures.txt').read().splitlines()))

  
#------------- declare stats of players' pokemon -------------#

#Forgive me, for I have sinned.
def init_statDictionaries(player):
  exec(f'''global {player}_stats;{player}_values = [pokedex[{player}_pokemon]["baseStats"][key] for key in dict.keys(pokedex[{player}_pokemon]["baseStats"])]
{player}_keys = ["{player}_hp", "{player}_atk", "{player}_def", "{player}_spa", "{player}_spd", "{player}_spe"]
{player}_stats = dict(zip({player}_keys, {player}_values))
{player}_stats["{player}_level"], {player}_stats["{player}_nature"], {player}_stats["{player}_pkmn"] = {player}_level, {player}_nature, {player}_pokemon''')  

#------------- initialize all stats -------------#
def init_stats():
  global p1_stats, p2_stats

  #makes list of natures and their buffs (buffs contained as corresponding key indeces to the stat dictionaries)
  naturebuffs = open('naturesbuffs.txt').read().splitlines()
  naturebuffs = [str(i) for i in naturebuffs] ; naturebuffs = [i.split(' ') for i in naturebuffs] 
  
  #creates stat dictionaries for players' pokemon
  #creates values (stat values) and keys (stat names); zips them. Also adds in the level and nature.
  init_statDictionaries('p1'); init_statDictionaries('p2')

    
#calc stats

  #calc HP
  p1_stats['p1_hp'] = math.floor(((2 * p1_stats['p1_hp']) * p1_stats['p1_level']) / 100 + p1_stats['p1_level'] + 10)
  p2_stats['p2_hp'] = math.floor(((2 * p2_stats['p2_hp']) * p2_stats['p2_level']) / 100 + p2_stats['p2_level'] + 10)

  #calc all other stats
  for i in p1_stats.keys():
    if list(p1_stats.keys()).index(i) < 6 and list(p1_stats.keys()).index(i) > 0:
      p1_stats[i] = math.floor((2 * p1_stats[i] * p1_stats['p1_level']) / 100 + 5)
      
  print()
  
  for i in p2_stats.keys():
    if list(p2_stats.keys()).index(i) < 6 and list(p2_stats.keys()).index(i) > 0:
      p2_stats[i] = math.floor((2 * p2_stats[i] * p2_stats['p2_level']) / 100 + 5)

  #calc nature
  do_natures(naturebuffs, 'p1')
  do_natures(naturebuffs, 'p2')

#------- do the natures -------#
def do_natures(naturebuffs, player):

  for i in naturebuffs:
    if eval(f"{player}_stats['{player}_nature'] in i and {player}_stats['{player}_nature'] not in ['Hardy','Docile','Bashful','Quirky','Serious']"):
      #now, we take i[1] and i[2] (the indices of what stats are changed). We find the associated stat. 
      do_natureBuffs(*find_changedStat(i, player, naturebuffs))

      
#------------- do the stat changes from nature -------------#

def do_natureBuffs(upperstat, lowerstat, player):
  if player == 'p1':
    p1_stats[upperstat] *= 1.1
    p1_stats[lowerstat] *= 0.9
    p1_stats[upperstat] = math.floor(p1_stats[upperstat]); p1_stats[lowerstat] = math.floor(p1_stats[lowerstat])
  else:
    p2_stats[upperstat] *= 1.1
    p2_stats[lowerstat] *= 0.9
    p2_stats[upperstat] = math.floor(p2_stats[upperstat]); p2_stats[lowerstat] = math.floor(p2_stats[lowerstat])
    

#------------- find the changed stats from nature -------------#

def find_changedStat(i, player, naturebuffs):
  
  upperstat_IDX = int(naturebuffs[naturebuffs.index(i)][1])
  lowerstat_IDX = int(naturebuffs[naturebuffs.index(i)][2])
  
  upperstat = list(p1_stats.keys())[upperstat_IDX] if player == 'p1' else list(p2_stats.keys())[upperstat_IDX]
  lowerstat = list(p1_stats.keys())[lowerstat_IDX] if player == 'p1' else list(p2_stats.keys())[lowerstat_IDX]

  return upperstat, lowerstat, player

  
#------------- ask about move settings -------------#
def ask_moveSettings():
  print(Fore.LIGHTGREEN_EX + "How do you want to create your movesets?\n", end='') 
  print(Fore.LIGHTGREEN_EX + """
  1 | Pre-set | All moves are the default for the level
  2 | Choose  | Create movesets based on valid moves for the Pokemon*
  3 | Sandbox | All moves are allowed on all Pokemon.
  4 | Random  | All moves are completely random. 

  *(TMs and Egg Moves included)

  Enter index of mode to play with:
  """, end='')

  moveSetting = input()
  return moveSetting

#------------- make move-sets -------------#
def init_movesets(moveSetting, player):

  print()
  
  if moveSetting == '1': #Pre-set
    print(1)
  elif moveSetting == '2': #Choose
    print(2)
    
    
  elif moveSetting == '3': #Sandbox
    exec(f"""for i in range(1,5):
      while len({player}_moves) != 4:
        try:
          move_to_add =(moves_formatted[moves_formatted.index(input('Player {player[1]}, select move: '))]); {player}_moves.append(move_to_add); print('P{player[1]} moveset:',{player}_moves)
        except ValueError: continue""")

    print(f'{player}_moves')

    
  else: #Random
    exec(f"""while len({player}_moves) != 4: 
      move_to_add = moves_formatted[random.randrange(0, 900)]
      if move_to_add not in {player}_moves:
        {player}_moves.append(move_to_add)""")


    exec(f'print({player}_moves)')

  exec(f'{player}_stats["{player}_moves"] = {player}_moves')
  exec(f'global {player}_moves_data; {player}_moves_data = []')
  exec(f'''for enum, i in enumerate({player}_moves):     
    {player}_moves_data.append(movesdata[(re.sub(" |-","",({player}_moves[enum].lower())))])''')

  

  # ************** BATTLE ************** #

def init_TurnStart(player):
  exec(f'''
global {player}_turn_start
{player}_turn_start = []
{player}_turn_start.append("Player 1" if player == 'p1' else "Player 2")
{player}_turn_start.append({player}_stats["{player}_pkmn"].capitalize()); {player}_turn_start.append({player}_stats["{player}_hp"])

{player}_stats_2 = {player}_stats
#{player}_stats is the one that will change (0.75 x the value, etc.) and be compared to {player}_stats_2 (the duplicate) for the multiplier

#{player}_stats_2 DOES NOT CHANGE.

for i in {player}_stats_2:
    if list({player}_stats_2.keys()).index(i) < 6 and list({player}_stats_2.keys()).index(i) > 0:
        {player}_turn_start.append({player}_stats[i] / {player}_stats_2[i])
''')
  if player == "p1":
    return p1_turn_start
  else: return p2_turn_start


#------------------------------------------------#
  
def tell_TurnStart():

  print(init_TurnStart("p1"), init_TurnStart("p2"))
  table_keys = ["Player","Pokemon", "Current HP", "Atk Buff", "SpA Buff", "Def Buff", "SpD Buff", "Spe Buff", "Status"]
  
  print(tabulate(list(zip(table_keys, init_TurnStart("p1"),init_TurnStart("p2")))))

#------------------------------------------------#

def find_TurnOrder():
  if p1_stats['p1_spe'] > p2_stats['p2_spe']:
    return ['p1', 'p2']
  else: return ['p2','p1']

#------------------------------------------------#

def move(i):
  exec(f"player_moves = {i}_moves")
  move = input(f"Player {i[-1]}, your moves are {player_moves}. Select your move (type it): ")
  
#------------------------------------------------#
def do_battle():
  in_battle = True

 #while in_battle == True:
  tell_TurnStart()
  for i in find_TurnOrder():
    move(i)
  
  

#------------- main -------------#

if __name__ == "__main__":
  if ask_selectPKMN() == 'test':
    p1_pokemon = 'abomasnow'; p1_level = 50; p1_nature = 'Adamant'; p2_pokemon = 'abra'; p2_level = 25; p2_nature = 'Serious'
    
  init_stats()
  print(f"\nP1 Stats: {p1_stats}")
  print(f"\nP2 Stats: {p2_stats}")
  
#prints "X vs Y" (cosmetic)
  print('\n',p1_pokemon.capitalize(), " vs ", p2_pokemon.capitalize(), "\n", sep='')

  moveSetting = ask_moveSettings()

  p1_moves = []
  p2_moves = []
  init_movesets(moveSetting, 'p1');init_movesets(moveSetting,'p2')
  do_battle()
