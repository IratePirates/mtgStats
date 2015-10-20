import random
from collections import namedtuple
#required for card library

card = namedtuple('card', 'Name, manaCost, cardType, cardText, power, toughness' )

class gameMechanics(object):
	class turnMechanics:
		def __init__(self):
			# Populate counters for the turn
			self.lands_to_play = 1
			self.mana = [0,0,0,0,0,0]
				#White, Blue, Black, Red, Green, Colourless

	def drawCard(self):
		new_card = random.choice(self.deck)
		self.hand.append(new_card)
		self.deck.remove(new_card)

	def tapAllLands(self):
		for idx,land in enumerate(['plains', 'island', 'swamp', 'mountain', 'forest']): #TODO - alias the colours rather than use index?
			self.turn.mana[idx] = self.landpile.count(land)

	def playLand(self, land):
		if land in self.hand:
			if self.turn.lands_to_play:
				self.hand.remove(land)
				self.landpile.append(land)
				self.turn.lands_to_play = self.turn.lands_to_play - 1

	def playUrzaLand(self):
		for land in ["Mine", "PP", "Tower"]:
			if self.turn.lands_to_play and land in self.hand and land not in self.landpile:
				self.playLand(land)

	def checkForUrzaTron(self):
		tronplayed = 0;
		for land in ["Mine", "PP", "Tower"]:
			if land in self.landpile:
				tronplayed += 1
		return tronplayed

	def playCard(self, cardName):
		if cardName in self.hand:
			for card in self.cardDb:
				if (card.Name == cardName):
					if self.checkCardCanBeCast(card.manaCost):
						#pay costs
						for colour in range(0, len(self.turn.mana)):
							self.turn.mana[colour] -= card.manaCost[colour]
						self.hand.remove(cardName)
						#get effect
						if (card.cardType == 'instant') or (card.cardType ==  'sorcery'):
							card.cardText()
						else:
							self.battlefield.append(cardName)

	def playCardSimple(self, card):
		if card in self.hand:
			self.hand.remove(card)
			self.battlefield.append(card)

	def newTurn(self):
		if ( (self.turn_count != 0) or (self.on_the_draw) ):
			self.drawCard()
		self.turn_count = self.turn_count + 1
		self.turn.lands_to_play = 1
		self.turn.mana = [0,0,0,0,0,0]
		#print ("Turn {} -- Size of hand {},\n hand {} \n battlefield {} {} ".format(self.turn_count, len(self.hand), self.hand, self.battlefield, self.landpile))

	def useCard(self, card):
		if card in self.battlefield:
			self.battlefield.remove(card)
			if card == "star":
				self.drawCard()
			elif card == "map":
				for tutored_land in ["Mine", "PP", "Tower"]:
					if tutored_land not in self.landpile and tutored_land in self.deck:
						self.deck.remove(tutored_land)
						self.hand.append(tutored_land)
		elif card in self.hand:
			self.hand.remove(card)
			if card == "scry":
				for tutored_land in ["Mine", "PP", "Tower"]:
					if tutored_land not in self.landpile and tutored_land in self.deck:
						self.deck.remove(tutored_land)
						self.hand.append(tutored_land)
			elif card == "bolt":
				self.opponents_life_total -= 3
			elif card == "stir":
				temp_cards = random.sample(self.deck, 5)
				card_chosen = 0
				for card in temp_cards:
					self.deck.remove(card)
					if card_chosen == 0 and card in ["Mine", "PP", "Tower"] and card not in self.landpile and card not in self.hand:
						card_chosen = 1
						self.hand.append(card)
				# Take Karn if you already have Tron
				if card_chosen == 0 and "Karn" in temp_cards:
					card_chosen = 1
					self.hand.append("Karn")
				elif card_chosen == 0 and "star" in temp_cards:
					card_chosen = 1
					self.hand.append("star")

	def numberCardsAbleToPlay(self):
		count = 0
		for cardName in self.hand:
			for card in self.cardDb:
				if (card.Name == cardName):
					if ((self.checkCardCanBeCast(card.manaCost)) and ( card.cardType != 'land')):
						count += 1
		return count

	def checkCardCanBeCast(self, manaCost):
		canCast = True
		for colour in range(0, len(self.turn.mana)):
			if manaCost[colour] > self.turn.mana[colour]:
				canCast = False
		return canCast

	def __init__(self, onTheDraw, Deck):
		#Generate the Card Database
		self.cardDb = []
		self.populateCardDb()
		# Populate the deck
		self.turn_count = 0
		self.hand = []
		self.deck = Deck[:]
		# Populate the battlefield
		self.battlefield = []
		self.landpile = []
		self.turn = self.turnMechanics()
		self.on_the_draw = onTheDraw
		self.opponents_life_total = 20

	def populateCardDb(self):
	#card = namedTuple ('card', 'Name, manaCost, cardType, cardText, power, toughness' )
		self.cardDb.append(card('bolt', [0,0,0,1,0,0], 'instant', self.boltCardtext, 0 , 0))
		self.cardDb.append(card('mountain',[0,0,0,0,0,0], 'land', self.mountainCardText, 0 , 0))
		
	def boltCardtext(self):
		#print("Bolt You")
		self.opponents_life_total -= 3

	def mountainCardText(self):
		pass