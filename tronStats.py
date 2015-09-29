"""
Tron Simulator
Initial Discussion:
https://www.reddit.com/r/TronMTG/comments/3mmnug/rg_tron_i_wrote_some_code_to_figure_out_how_often/

Relevant Cards
4 Mine
4 PP
4 Tower

4 Sphere (labeled star)
4 Star
4 Map
4 Scrying
4 Stirring

4 Karn

24 Other cards
"""

import random

## Initialize some variables that count useful things
count_turn_3_karn = 0
turn_3_tron = 0
map_opening = 0
star_opening = 0
other_opening = 0
hard_opening = 0
hard_success = 0

## Change this to False if you want to always be on the play
on_the_draw = False

## Number of simulations
## N = 100000 should take a couple of seconds, N = million ~30 seconds.
N = 100000

class gameMechanics(object):
	class turnMechanics:
		def __init__(self):		
			# Populate counters for the turn
			self.lands_to_play = 1
			self.colorless_mana = 0
			self.green_mana = 0

	def drawCard(self):
		new_card = random.choice(self.deck)
		self.hand.append(new_card)
		self.deck.remove(new_card)
		
	def playLand(self, land):
		if self.turn.lands_to_play:
			self.hand.remove(land)
			self.battlefield.append(land)
			self.turn.lands_to_play = self.turn.lands_to_play - 1

	def playUrzaLand(self):
		for land in ["Mine", "PP", "Tower"]:
			if self.turn.lands_to_play and land in self.hand and land not in self.battlefield:
				self.playLand(land)
			
	def playCard(self, card):
		self.hand.remove(card)
		self.battlefield.append(card)

	def newTurn(self):
		if ( (self.turn != 0) or (self.on_the_draw) ):
			self.drawCard()
		self.turn_count = self.turn_count + 1 
		self.turn.lands_to_play = 1
		
	def useCard(self, card):
		if card in self.battlefield:
			self.battlefield.remove(card)
			if card == "star":
				self.drawCard()
			elif card == "map":
				for tutored_land in ["Mine", "PP", "Tower"]:
					if tutored_land not in self.battlefield and tutored_land in self.deck:
						self.deck.remove(tutored_land)
						self.hand.append(tutored_land)
			elif card == "scry":
				self.hand.remove("scry")
				for tutored_land in ["Mine", "PP", "Tower"]:
					if tutored_land not in self.battlefield and tutored_land in self.deck:
						self.deck.remove(tutored_land)
						self.hand.append(tutored_land)
			elif card == "stir":
				temp_cards = random.sample(self.deck, 5)
				card_chosen = 0
				for card in temp_cards:
					self.deck.remove(card)
					if card_chosen == 0 and card in ["Mine", "PP", "Tower"] and card not in self.battlefield and card not in self.hand:
						card_chosen = 1
						self.hand.append(card)
				# Take Karn if you already have Tron
				if card_chosen == 0 and "Karn" in temp_cards:
					card_chosen = 1
					self.hand.append("Karn")
				elif card_chosen == 0 and "star" in temp_cards:
					card_chosen = 1
					self.hand.append("star")

	def __init__(self, onTheDraw):
		# Populate the deck
		self.turn_count = 0
		self.hand = []
		self.deck = ["Mine", "Mine", "Mine", "Mine", "PP", "PP", "PP", "PP", "Tower", "Tower", "Tower", "Tower", "star", "star", "star", "star", "star", "star", "star", "star", "map", "map", "map", "map", "scry", "scry", "scry", "scry", "stir", "stir", "stir", "stir", "Karn", "Karn", "Karn", "Karn"]
		for x in range(60 - len(self.deck)):
			self.deck.append("dead")
		# Populate the battlefield
		self.battlefield = []
		self.turn = self.turnMechanics()
		self.on_the_draw = onTheDraw

def new_game(draw):
	# Keep track of stats
	# 0 = Map openings, 1 = Star openings, 2 = Other opening, 3 = Hard Opening, 4 = T3 Tron
	opening = [0,0,0,0,0]
	game = gameMechanics(draw)

	# Populate the starting hand
	starting_size = 7
	decided_on_hand = False
	game.hand = random.sample(game.deck,7)
	
	# Decide on mulligans
	# Keeps iff at least one Tron piece
	while not decided_on_hand and starting_size >0:
		if "Mine" not in game.hand and "PP" not in game.hand and "Tower" not in game.hand:
			starting_size -= 1
			game.hand = random.sample(game.deck, starting_size)
		else:
			decided_on_hand = True
	#Take the cards out of the deck
	for card in game.hand:
		game.deck.remove(card)
	
	# Turn 1
	########
	game.newTurn()

	#Playing a land
	game.playUrzaLand()
	
	# Decide on map or star
	
	if "map" in game.hand and "star" in game.hand:
		# How many new tron pieces in hand?
		new_tron_in_hand = 0
		if "Mine" in game.hand and "Mine" not in game.battlefield:
			new_tron_in_hand += 1
		if "PP" in game.hand and "PP" not in game.battlefield:
			new_tron_in_hand += 1
		if "Tower" in game.hand and "Tower" not in game.battlefield:
			new_tron_in_hand += 1			
		
		# 2 new pieces? Do star to look for Karn
		if new_tron_in_hand == 2:
			# Star Opening
			game.playCard("star")
			opening[1] += 1
		elif new_tron_in_hand == 1:
			# Map Opening
			game.playCard("map")
			opening[0] += 1
		elif new_tron_in_hand == 0:
			##### These are the hard choice openings
			game.playCard("star")
			opening[3] += 1
	elif "map" in game.hand:
		# Map Opening
		game.playCard("map")
		opening[0] += 1
	elif "star" in game.hand:
		# Star Opening
		game.playCard("star")
		opening[1] += 1
	else:
		# Other opening
		opening[2] += 1
	
	# Turn 2
	########
	game.newTurn()

	# This will be used once later
	stop_playing_stars = False
	
	#Playing a land
	game.playUrzaLand()
	
	if (game.turn.lands_to_play == 0):
		#Use your star if you have it
		if "star" in game.battlefield:
			game.useCard("star")
			#Do you have Scrying?
			if "scry" in game.hand:
				game.useCard("scry")
			else:
				if "star" in game.hand:
					#Play and use a star
					game.playCard("star")
					game.useCard("star")
					stop_playing_stars = True
				if "stir" in game.hand:
					game.useCard("stir")
				if "star" in game.hand and not stop_playing_stars:
					game.playCard("star")
		elif "map" in game.battlefield:
			game.useCard("map")

	else:
		# No land played yet
		# Use a star if you have it
		if "star" in game.battlefield:
			game.useCard("star")
			
			game.playUrzaLand()

			if (game.turn.lands_to_play):
				if "stir" in game.hand:
					game.useCard("stir")
					game.playUrzaLand()
					# Do you have a star?
					if "star" in game.hand:
						game.playCard("star")
					# End turn
				if game.turn.lands_to_play:
					# You only have one land on Turn 2, so no Turn 3 Karn
					return False, opening
			else:
				# You played a land.
				# Do you have Scrying?
				if "scry" in game.hand:
					game.useCard("scry")
					# END TURN
				else:
					if "star" in game.hand:
						#Play and use a star
						game.playCard("star")
						game.useCard("star")	
						stop_playing_stars = True
					if "stir" in game.hand:
						game.useCard("stir")
					if "star" in game.hand and not stop_playing_stars:
						#Play your last star
						game.playCard("star")
		else:
			# You only have one land on Turn 2, so no Turn 3 Karn
			return False, opening
	
	# Turn 3
	#########
	game.newTurn()
	
	#Playing a land
	game.playUrzaLand()
	
	if "star" in game.battlefield:
		game.useCard("star")
	
	#Play Karn
	if "Mine" in game.battlefield and "PP" in game.battlefield and "Tower" in game.battlefield:
		opening[4] += 1
		if "Karn" in game.hand:
			return True, opening
		else: 
			return False, opening
	else:
		return False, opening

####
## Run simulations
for i in range(N):
	state = new_game(on_the_draw)
	map_opening += state[1][0]
	star_opening += state[1][1]
	other_opening += state[1][2]
	hard_opening += state[1][3]
	turn_3_tron += state[1][4]
	if state[0]:
		count_turn_3_karn += 1
	if state[0] and state[1][3]:
		hard_success += 1

#####
## Display results
print( "Turn 3 Tron {}".format( 100 * float(turn_3_tron) / N ))
print( "Turn 3 Karn {}".format( 100 * float(count_turn_3_karn) / N ))
print( "Map Openings: {}".format( 100 * float(map_opening) / N ))
print( "Star Openings: {}".format( 100 * float(star_opening) / N ))
print( "Other Openings: {}".format( 100 * float(other_opening) / N ))
print( "Hard Openings: {}".format( 100 * float(hard_opening) / N ))
print( "Hard successes: {}".format( 100 * float(hard_success) / hard_opening ))
