"""
Goldfish simulator for 1 Drop burn deck optimisation
"""

import random
import copy
import gameMechanics

class simulation():
	def __init__(self, sizeOfTestpop = 2):
		self.on_the_draw = False
		self.turn_of_kill = []
		self.deck_to_test = []
		self.cardlistAvailable = ["bolt"]
		self.cardlistAvailableLand = ["mountain"]
		self.gameIterations = 10000
		self.maxTurns = 15
		self.earliest_victory = []

		#Deck optimisation Strategy
		self.test_population_size = sizeOfTestpop
		self.mutateEnable = True
		self.numberDecksToMutate = 1
		self.cardsToMutate = 3
		self.convergenceThreshold = 0.05

		self.cardlistAllAvailable = self.cardlistAvailable + self.cardlistAvailableLand
		for i in range(sizeOfTestpop):
			self.earliest_victory.append(self.maxTurns)

	def randomiseStartingDecks(self, FourCardRule = False):
	#TODO - expand logic for multiple cards and include more rules.
		try:
			for x in range(0, self.test_population_size) :
				deck = []
				numNonLand = random.randint(0, 50)
				cardsInserted = 0
				while (cardsInserted < numNonLand):
					card = self.cardlistAvailable[random.randint(0, len(self.cardlistAvailable) - 1)]
					if (deck.count(card) < 4) or (FourCardRule is False):
						deck.append(card)
						cardsInserted += 1
				while (cardsInserted < 60):
					card = self.cardlistAvailableLand[random.randint(0, len(self.cardlistAvailableLand) - 1)]
					if (deck.count(card) < 4) or (FourCardRule is False) or card is "island" or card is "swamp" or card is "mountain" or card is "forest" or card is "plains":
						deck.append(card)
						cardsInserted += 1
				self.deck_to_test.append(deck)
		except Exception as e:
			print ("Something went horribly wrong - {}".format(e))

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

			while (game.turn_count < self.maxTurns and game.opponents_life_total > 0 ):
				#print('turn {} - opp life {} - hand = {}'.format(game.turn_count + 1, game.opponents_life_total, game.hand))
				game.newTurn()
				game.playLand('mountain')
				#TODO - move casting spell mechanics into the game mechancis file.
				game.tapAllLands()
				while (game.turn.mana[3] and game.numberCardsAbleToPlay()):
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
				DeckResults = [None]*self.test_population_size
				for idx,deck in enumerate(self.deck_to_test):
					DeckResults[idx] = (self.playDeck(deck))
				convergence = False
				mutateDeck = True if ((self.test_population_size > 1) and (self.mutateEnable)) else False

				difference = [None]*self.test_population_size
				#Check for convergence of turn to kill (in final two values)
				for idx, deck in enumerate(self.deck_to_test):
					#TODO - Get this better difference working...
					#if (len(self.turn_of_kill) > 2):
					#	oldDifference = sum(self.turn_of_kill[][idx])/len(self.turn_of_kill[][idx])
					self.turn_of_kill.append(DeckResults)
					#	newDifference = sum(self.turn_of_kill[][idx])/len(self.turn_of_kill[][idx])
					#	difference = oldDifference - newDifference
					#elif(len(self.turn_of_kill) == 2):
					if(len(self.turn_of_kill) > 2):
						difference[idx] = self.turn_of_kill[len(self.turn_of_kill)-1][idx] - self.turn_of_kill[len(self.turn_of_kill)- 2][idx]

				if(len(self.turn_of_kill) > 2):
					print("diffs - {}".format(difference))
					for idx,value in enumerate(difference):
						if ((self.turn_of_kill[len(self.turn_of_kill)-1][idx] is not None) and (value is not None)):
							if (abs(value) < self.convergenceThreshold):
								print('deck {} - difference = {}'.format(idx, value))
								convergence = True

				if (convergence):
					return

				if (mutateDeck):
					print ("***Mutating Decks***")
					mutant_population = random.sample(self.deck_to_test, self.numberDecksToMutate)
					for mutant in mutant_population:
						#self.deck_to_test.remove(mutant)
						cards_to_change = random.sample(range(60), self.cardsToMutate)

						for card in cards_to_change:
							new_card = self.cardlistAllAvailable[random.randint(0, len(self.cardlistAllAvailable) - 1)]
							mutant[card]= new_card
							print("card - {} to change to {}".format(mutant[card] , new_card) )
					self.print_decks()
					#TODO - Fix score on deck being mutated.
		except KeyboardInterrupt:
			print ("Caught Escape character")
		#except Exception as e:
		#	print ("Caught Exception - {}".format(e))

sim = simulation()
sim.randomiseStartingDecks()
sim.runSimulation()
sim.displayResults()
