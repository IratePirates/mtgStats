"""
Goldfish simulator for 1 Drop burn deck optimisation
"""

import random
import copy
import gameMechanics

class simulation():
	def __init__(self, sizeOfTestpop):
		self.on_the_draw = True
		self.turn_of_kill = []
		self.deck_to_test = []
		self.test_population_size = sizeOfTestpop
		self.cardlistAvailable = ['bolt']
		self.cardlistAvailableLand = ['mountain']
		self.gameIterations = 10000
		self.maxTurns = 15
		self.earliest_victory = []

		for i in range(sizeOfTestpop):
			self.earliest_victory.append(10)

	def randomiseStartingDecks(self):
	#TODO - expand logic for multiple cards and include more rules.
		for x in range(0, self.test_population_size) :
			deck = []
			#for i in range(0,random.randint(0, 50)):
			for i in range(0,44):
				deck.append('bolt')
			for x in range(60 - len(deck)):
				deck.append("mountain")
			self.deck_to_test.append(deck)

	def starting_hand(self, deck):
	#TODO  - improve logic in here.
		#populate starting hand
		starting_size = 7
		decided_on_hand = False
		hand = random.sample(deck,7)

		#decide if hand is keepable
		while not decided_on_hand and starting_size > 0:
			landCount = hand.count('mountain')
			if (landCount < 1 ) or (landCount > (starting_size - 2)):
				starting_size -= 1
				hand = random.sample(deck, starting_size)
			else:
				decided_on_hand = True

		#Take the cards out of the deck
		for card in hand:
			deck.remove(card)
		return hand

	def playDeck(self, deck):
		fatalTurn = []
		for iteration in range(0, self.gameIterations):
			gameDeck = copy.deepcopy(deck)
			game = gameMechanics.gameMechanics(self.on_the_draw, gameDeck)
			game.hand = self.starting_hand(gameDeck)

			while (game.turn_count < 10 and game.opponents_life_total > 0 ):
				print('turn {} - opp life {} - hand = {}'.format(game.turn_count + 1, game.opponents_life_total, game.hand))
				game.newTurn()
				game.playLand('mountain')
				#TODO - move casting spell mechanics into the game mechancis file.
				game.tapAllLands()
				while (game.turn.mana[3] and len(game.hand) > 0): #work out stall conditions...
					game.playCard('bolt')
				#TODO - add creatures
			fatalTurn.append(game.turn_count)
		return sum(fatalTurn)/(len(fatalTurn))

	def print_decks(self, printKillTurn = False):
		for idx, deck in enumerate(self.deck_to_test):
			print('Deck {}: '.format(idx))
			for card in self.cardlistAvailable:
				print('{} x {}'.format(card, deck.count(card)))
			for card in self.cardlistAvailableLand:
				print('{} x {}'.format(card, deck.count(card)))
			#print('Fatal Turn  -  {}'.format(self.turn_of_kill[len(self.turn_of_kill)][idx]))
			if printKillTurn:
				print(self.turn_of_kill)

	def displayResults(self):
		print('*********Experiment Over*********')
		print('earliest victory - {}'.format(self.earliest_victory))
		self.print_decks(True)

	def runSimulation(self):
		do_simulation = True

		self.print_decks()
		try:
			while (do_simulation):
			#for each deck simulate the games
				DeckResults = []
				for deck in self.deck_to_test:
					DeckResults.append(self.playDeck(deck))

				self.turn_of_kill.append(DeckResults)

				#Check for convergence of turn to kill (in final two values)
				for idx, deck in enumerate(self.deck_to_test):
					if (len(self.turn_of_kill) > 1):
						difference = self.turn_of_kill[len(self.turn_of_kill)-1][idx] - self.turn_of_kill[len(self.turn_of_kill)- 2][idx]
						if (abs(difference) < 0.05) and self.turn_of_kill[len(self.turn_of_kill)-1][idx] != self.maxTurns:
							print('difference = {}'.format(difference))
							return
						#else mutate the deck.
		except KeyboardInterrupt:
			print ("Caught Escape character")

sim = simulation(1)
sim.randomiseStartingDecks()
sim.runSimulation()
sim.displayResults()
