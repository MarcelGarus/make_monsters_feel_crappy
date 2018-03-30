# Monster game

from sys import exit, stdout, argv
from random import random
import math

DIFFICULTY = 0.2
HIGHSCORES_FILE = 'monsters_highscores.txt'
NUM_HIGHSCORES = 10


# THE CORE GAME LOGIC
yard = [0, 0, 0, 4]
score = 0
level = 1


# creates a new monster
def new_monster():
	return math.floor(random() * (score + DIFFICULTY * score**2 + 1))


# generator of all living monsters' indexes
def get_monsters():
	# filter monsters with positive hp, then yield their indexes
	for (index, _) in filter(lambda e: e[1] > 0, enumerate(yard)):
		yield index


# returns a list of how much harm will be done to every position
def get_weapon_effect(weapon):
	effect = [ 0 for _ in range(len(yard)) ]
	if weapon == 'c': # Constant Cannon
		for i in get_monsters():
			effect[i] = -level
	elif weapon == 'l': # Linear Laser
		for counter, i in enumerate(get_monsters()):
			effect[i] = -level * (counter + 1)
	elif weapon == 's': # Sinus Shooter
		for counter, i in enumerate(get_monsters()):
			effect[i] = level if counter % 2 == 1 else -level
	elif weapon == 'g': # Gaussian Gun
		pos_of_strongest = yard.index(max(yard))
		for i in get_monsters():
			effect[i] = round(-level * math.e ** (-0.5 * (i - pos_of_strongest)**2))
	else:
		return None
	return effect


# handles a player action. Returns -1: bad input 0: game continues 1: game over
def handle_action(action):
	global level
	global score

	if action == 'r': # range increased
		yard.append(new_monster())
	elif action == 'u': # weapon level upgrade
		level += 1
	else: # weapon is used
		effect = get_weapon_effect(action)
		if effect == None:
			return -1
		for i in range(len(yard)):
			new_hp = max(0, yard[i] + effect[i])
			score += 0 if yard[i] == 0 or new_hp > 0 else 1 # newly killed
			yard[i] = new_hp

	# move ghosts
	yard.append(new_monster())
	return 0 if yard.pop(0) == 0 else 1




# THE "GRAPHICAL" STUFF
USE_COLORS = not '--no-colors' in argv
TOWN_WIDTH = 17

def clear():
	print('\033[H\033[J') # clear screen

def bold(s):
	return '\x1b[1;37;40m%s\x1b[0m' % (s) if USE_COLORS else s


# pretty-prints the yard. Returns an array with the positions of all monsters
def print_game(message):
	clear()
	print(message + '\n') # print message

	# print line of monsters
	s = '%%-%ds' % (TOWN_WIDTH) % ('helpless village')
	length = TOWN_WIDTH
	positions = [] # positions of all the monsters will be saved here

	for monster in yard:
		positions.append(length)
		# color is cyan, green, yellow, red or violet based on hp
		s += '' if not USE_COLORS or monster == 0 else '\x1b[1;%d;40m' % (\
				36 if monster < 5 else\
				32 if monster < 10 else\
				33 if monster < 50 else\
				31 if monster < 100 else\
				35)
		s += (str(monster) if monster > 0 else '_') + ' '
		s += '\x1b[0m' if USE_COLORS else ''
		length += len(str(monster)) + 1
	print(s)

	# print weapons
	for id, name, bg in [('c','Constant Cannon',41), ('l','Linear Laser',46), ('g','Gaussian Granade',43)]:
		effect = get_weapon_effect(id)
		s = ('\x1b[1;37;%dm' % bg if USE_COLORS else '') + '%%-%ds' % TOWN_WIDTH % name
		length = TOWN_WIDTH

		for (i, pos), eff in zip(enumerate(positions), effect):
			text =  '' if yard[i] == 0 or eff == 0 else\
					'X' if yard[i] + eff <= 0 else\
					str(yard[i] + eff)
			s += (pos - length) * ' ' + text
			length = pos + len(text)

		s += ' \x1b[0m' if USE_COLORS else ''
		print(s)
	print('%s: increase range, %s: upgrade weapon level' % (bold('r'), bold('u')))


# prints the highscores
def print_highscores(highscores):
	if len(highscores) == 0:
		print('There were no highscores saved yet. Time to fill the list!')
		return

	max_len_rank = math.log(len(highscores) + 1, 10)
	max_len_score = max(math.log(max(1, highscores[0][0]), 10), len('Score'))
	max_len_name = max(map(lambda entry: len(entry[1]), highscores))

	# header
	print(bold(\
		('%%%ds %%%ds %%-%ds' % (max_len_rank, max_len_score, max_len_name))\
							% ('#', 'Score', 'Name')\
	))

	# the entries
	for i, entry in enumerate(highscores):
		print(('%%%ds %%%ds %s'\
			% (max_len_rank, max_len_score, entry[1]))\
			% (str(i + 1), str(entry[0])))


# print the gameover screen
def game_over():
	clear()
	print('\n' + ('\x1b[1;31;40m' if USE_COLORS else '')
	+ ' ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗\n'
	+ '██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗\n'
	+ '██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝\n'
	+ '██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗\n'
	+ '╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║\n'
	+ ' ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝\n'
	+ ('\x1b[0m' if USE_COLORS else ''))

# returns the prompt string
def get_promt_string():
	return ('\x1b[1;37;42m' if USE_COLORS else '') \
	+ 'weapon lvl %d ' % level \
	+ ('\x1b[1;37;45m' if USE_COLORS else '/') \
	+ ' %d killed ' % score \
	+ ('\x1b[0m' if USE_COLORS else '/') \
	+ ' action>'




# THE HIGHSCORES
# returns a list of highscores with names
def get_highscores():
	highscores = []
	try:
		with open(HIGHSCORES_FILE, 'r') as f:
			for line in f:
				try:
					i = line.index(' ')
					score = int(line[:i])
				except ValueError:
					continue # not a valid line
				if score < 0:
					continue # not a valid line
				name = line[i+1:].strip()
				highscores.append((score, name))
	except FileNotFoundError:
		pass # just continue and return an empty list. First time played.
	return highscores


# returns what the own position in the high scores list would be. -1 if too bad
def get_rank(highscores, score):
	for i, entry in enumerate(highscores):
		if score > entry[0]:
			return i
	return -1 if len(highscores) >= NUM_HIGHSCORES else len(highscores)


# adds a score to the highscores list
def add_to_highscores(highscores, score, name):
	highscores.insert(get_rank(highscores, score), (score, name))
	if len(highscores) > NUM_HIGHSCORES:
		del highscores[-1]
	return highscores


# saves the highscores back into the file
def save_highscores(highscores):
	with open(HIGHSCORES_FILE, 'w+') as f:
		for entry in highscores:
			f.write(str(entry[0]) + ' ' + entry[1] + '\n')
			f.flush()




# THE MAIN PROGRAM
def main():
	try:
		res = 0
		while True:
			message = 'That is not a valid action. Enter c, l, g, r, or u!' if res < 0 else\
				'First game? Watch the tutorial: https://example.com' if score == 0 else\
				'Villagers start to realize you fight for them.' if score < 20 else\
				'Clouds fly by as the monsters\' blood drains the ground.' if score < 30 else\
				'Scarecrows move and creak in the wind.' if score < 40 else\
				'The sun shifts as the massacre continues for hours.' if score < 50 else\
				'Water swirling dreamily in a nearby river starts to get a red, bloody shade.' if score < 60 else\
				'Hours pass and the sun starts to set, causing a group of old oaks to cast long shadows on the battlefield.' if score < 70 else\
				'A beautiful red fills the sky, matching the red of the dead monsters\' corpuses.' if score < 80 else\
				'The moon shines on the field. The sound of crickets, owl and wind is only interrupted by the creaks of dying monsters.' if score < 90 else\
				'The last villagers who stayed awake out of fear begin to fall asleep dreamily.' if score < 100 else\
				'Hundreds of monsters have been killed by now. But the fight goes on.'
			print_game(message)
			stdout.write(get_promt_string())
			stdout.flush()
			action = input('').lower()

			res = handle_action(action[0])
			if res > 0:
				break
	except (KeyboardInterrupt, EOFError) as _:
		clear()
		stdout.write('\x1b[1;37;41m' if USE_COLORS else '')
		print('It was a short, brutal, bloody fight as the monsters enter the village.')
		print(('They mourn about the %d of them who you killed, but they ' % score if score > 0 else 'They ')
		+ 'thank you for leaving the yummy villagers unprotected.')
		stdout.write('\x1b[0m' if USE_COLORS else '')
		exit(0)

	# game over
	game_over()
	stdout.write('\x1b[1;37;41m' if USE_COLORS else '')
	print('It was a short, brutal, bloody fight as the monsters enter the village.')
	if score > 0:
		print('At least you killed %d of them before they could eat the villagers.\n' % score)
	else:
		print('You couldn\'t kill one of them before they reached the village.')
	stdout.write('\x1b[0m' if USE_COLORS else '')
	highscores = get_highscores()
	rank = get_rank(highscores, score)

	if rank < 0:
		print('Play again if you want to try to get on this highscores list:')
		print_highscores(highscores)
	else:
		if rank == 0:
			print('Wow! That\'s a new highscore!')
		else:
			print('That would be rank #%d in the highscores list!' % (rank + 1))
		try:
			name = input('Enter your name > ').strip()

			highscores = add_to_highscores(highscores, score, name)
			save_highscores(highscore)

			# save and print them
			clear()
			print('Doesn\'t this look beautiful?')
			print_highscores(highscores)

		except (KeyboardInterrupt , EOFError) as _:
			print('\nIf you don\'t want to, that\'s alright.')
			print('See you again soon!')


main()
