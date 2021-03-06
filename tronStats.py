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
import gameMechanics

class simulation():
	def __init__(self):
		## Initialize some variables that count useful things
		self.count_turn_3_karn = 0
		self.turn_3_tron = 0
		self.map_opening = 0
		self.star_opening = 0
		self.other_opening = 0
		self.hard_opening = 0
		self.hard_success = 0
		## Change this to False if you want to always be on the play
		self.on_the_draw = False
		## Number of simulations
		## N = 100000 should take a couple of seconds, N = million ~30 seconds.
		self.N = 1000000
		
		self.deckToTest = ["Mine", "Mine", "Mine", "Mine", "PP", "PP", "PP", "PP", "Tower", "Tower", "Tower", "Tower", "star", "star", "star", "star", "star", "star", "star", "star", "map", "map", "map", "map", "scry", "scry", "scry", "scry", "stir", "stir", "stir", "stir", "Karn", "Karn", "Karn", "Karn"]
		for x in range(60 - len(self.deckToTest)):
			self.deckToTest.append("dead")

	def starting_hand(self, deck):
		# Populate the starting hand
		starting_size = 7
		decided_on_hand = False
		hand = random.sample(deck,7)
		
		# Decide on mulligans
		# Keeps iff at least one Tron piece
		while not decided_on_hand and starting_size >0:
			if "Mine" not in hand and "PP" not in hand and "Tower" not in hand:
				starting_size -= 1
				hand = random.sample(deck, starting_size)
			else:
				decided_on_hand = True
		#Take the cards out of the deck
		for card in hand:
			deck.remove(card)
		return hand

	def turn(self):
		pass

	def determine_simulation_end (self, Game):
		if (Game.turn_count == 3):
			if "Karn" in Game.battlefield:
				self.count_turn_3_karn += 1
				self.turn_3_tron += 1 			#implied
				if self.hardOpening:
					self.hard_success += 1
				return True
			elif (Game.checkForUrzaTron() == 3 ):
				self.turn_3_tron += 1
				return True
			else:
				return True
		elif (Game.turn_count == 2):
			if (Game.checkForUrzaTron() < 2 ):
				return True
		return False
	
	def new_game(self, draw, deck):
		self.hardOpening = False;
		game = gameMechanics.gameMechanics(draw, deck)
		
		game.hand = self.starting_hand(deck)

		# Turn 1
		########
		game.newTurn()
		#print ("hand {}, size {}".format(game.hand, len(game.hand)))

		#Playing a land - assumed to hvae at least 1 in hand from mulliganing
		game.playUrzaLand()
		
		# Decide on map or star
		if "map" in game.hand and "star" in game.hand:
			# How many new tron pieces in hand?
			new_tron_in_hand = 0
			for urza_land in ["Mine", "PP", "Tower"]:
				if urza_land not in game.landpile and urza_land in game.hand:
					new_tron_in_hand += 1
			
			# 2 new pieces? Do star to look for Karn
			if new_tron_in_hand == 2:
				game.playCardSimple("star")
				self.star_opening += 1
			elif new_tron_in_hand == 1:
				game.playCardSimple("map")
				self.map_opening += 1
			elif new_tron_in_hand == 0: ###Hard openingg
				game.playCardSimple("star")
				self.hardOpening = True;
				self.hard_opening += 1
		elif "map" in game.hand:
			game.playCardSimple("map")
			self.map_opening += 1
		elif "star" in game.hand:
			game.playCardSimple("star")
			self.star_opening += 1
		else:
			self.other_opening += 1
		
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
				if "scry" in game.hand:
					game.useCard("scry")
				else:
					if "star" in game.hand:
						game.playCardSimple("star")
						game.useCard("star")
						stop_playing_stars = True
					if "stir" in game.hand:
						game.useCard("stir")
					if "star" in game.hand and not stop_playing_stars:
						game.playCardSimple("star")
			elif "map" in game.battlefield:
				game.useCard("map")
		else:
			# No land played yet
			if "star" in game.battlefield:
				game.useCard("star")
				
				# if draw land play it
				game.playUrzaLand()

				if (game.turn.lands_to_play):
					if "stir" in game.hand:
						game.useCard("stir")
						game.playUrzaLand()
						if "star" in game.hand:
							game.playCardSimple("star")
						# End turn
				else:
					# You played a land.
					# Do you have Scrying?
					if "scry" in game.hand:
						game.useCard("scry")
					else:
						if "star" in game.hand:
							game.playCardSimple("star")
							game.useCard("star")	
							stop_playing_stars = True
						if "stir" in game.hand:
							game.useCard("stir")
						if "star" in game.hand and not stop_playing_stars:
							game.playCardSimple("star")
		if self.determine_simulation_end(game):
			return
		
		# Turn 3
		#########
		game.newTurn()
		
		#Playing a land
		game.playUrzaLand()
		
		if "star" in game.battlefield:
			game.useCard("star")

		#Playing a land
		game.playUrzaLand()
		
		#Play Karn
		if (game.checkForUrzaTron() == 3):
			game.playCardSimple("Karn")
		self.determine_simulation_end(game)
		return
	def runSimulation(self):
		for i in range(self.N):
			self.new_game(self.on_the_draw, self.deckToTest[:])
	def displayResults(self):
		print( "Turn 3 Tron {}".format( 100 * float(self.turn_3_tron) / self.N ))
		print( "Turn 3 Karn {}".format( 100 * float(self.count_turn_3_karn) / self.N ))
		print( "Map Openings: {}".format( 100 * float(self.map_opening) / self.N ))
		print( "Star Openings: {}".format( 100 * float(self.star_opening) / self.N ))
		print( "Other Openings: {}".format( 100 * float(self.other_opening) / self.N ))
		print( "Hard Openings: {}".format( 100 * float(self.hard_opening) / self.N ))
		print( "Hard successes: {}".format( 100 * float(self.hard_success) / (self.hard_opening + 1) ))

sim = simulation()
sim.runSimulation()
sim.displayResults()