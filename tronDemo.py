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
N = 1000000


def game(draw):
	# Populate the deck
	deck = ["Mine", "Mine", "Mine", "Mine", "PP", "PP", "PP", "PP", "Tower", "Tower", "Tower", "Tower", "star", "star", "star", "star", "star", "star", "star", "star", "map", "map", "map", "map", "scry", "scry", "scry", "scry", "stir", "stir", "stir", "stir", "Karn", "Karn", "Karn", "Karn"]
	for x in range(24):
		deck.append("dead")
	
	# Keep track of stats
	# 0 = Map openings, 1 = Star openings, 2 = Other opening, 3 = Hard Opening, 4 = T3 Tron
	opening = [0,0,0,0,0]
	
	# Populate the battlefield
	battlefield = []
	
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
	
	# Turn 1
	########
	
	# Draw a card
	if draw == True: 
		new_card = random.choice(deck)
		hand.append(new_card)
		deck.remove(new_card)
	
	#Playing a land
	lands_played_this_turn = 0
	for land in ["Mine", "PP", "Tower"]:
		if lands_played_this_turn == 0 and land in hand and land not in battlefield:
			hand.remove(land)
			battlefield.append(land)
			lands_played_this_turn = 1
	
	# Decide on map or star
	
	if "map" in hand and "star" in hand:
		# How many new tron pieces in hand?
		new_tron_in_hand = 0
		if "Mine" in hand and "Mine" not in battlefield:
			new_tron_in_hand += 1
		if "PP" in hand and "PP" not in battlefield:
			new_tron_in_hand += 1
		if "Tower" in hand and "Tower" not in battlefield:
			new_tron_in_hand += 1			
		
		# 2 new pieces? Do star to look for Karn
		if new_tron_in_hand == 2:
			# Star Opening
			hand.remove("star")
			battlefield.append("star")
			opening[1] += 1
		elif new_tron_in_hand == 1:
			# Map Opening
			hand.remove("map")
			battlefield.append("map")
			opening[0] += 1
		elif new_tron_in_hand == 0:
			##### These are the hard choice openings
			hand.remove("star")
			battlefield.append("star")
			opening[3] += 1
	elif "map" in hand:
		# Map Opening
		hand.remove("map")
		battlefield.append("map")
		opening[0] += 1
	elif "star" in hand:
		# Star Opening
		hand.remove("star")
		battlefield.append("star")
		opening[1] += 1
	else:
		# Other opening
		opening[2] += 1
	
	# Turn 2
	########
	
	lands_played_this_turn = 0
	# This will be used once later
	stop_playing_stars = False
	
	# Draw a card
	new_card = random.choice(deck)
	hand.append(new_card)
	deck.remove(new_card)
	
	#Playing a land
	for land in ["Mine", "PP", "Tower"]:
		if lands_played_this_turn == 0 and land in hand and land not in battlefield:
			hand.remove(land)
			battlefield.append(land)
			lands_played_this_turn = 1
	
	if lands_played_this_turn == 1:
		#Use your star if you have it
		if "star" in battlefield:
			battlefield.remove("star")
			# Draw a card
			new_card = random.choice(deck)
			hand.append(new_card)
			deck.remove(new_card)
		
			#Do you have Scrying?
			if "scry" in hand:
				# Play Scrying
				hand.remove("scry")
				for tutored_land in ["Mine", "PP", "Tower"]:
					if tutored_land not in battlefield and tutored_land in deck:
						deck.remove(tutored_land)
						hand.append(tutored_land)
			else:
				if "star" in hand:
					#Play and use a star
					hand.remove("star")
					# Draw a card
					new_card = random.choice(deck)
					hand.append(new_card)
					deck.remove(new_card)
					stop_playing_stars = True
				if "stir" in hand:
					#Resolve Stirrings
					temp_cards = random.sample(deck, 5)
					card_chosen = 0
					for card in temp_cards:
						deck.remove(card)
						if card_chosen == 0 and card in ["Mine", "PP", "Tower"] and card not in battlefield and card not in hand:
							card_chosen = 1
							hand.append(card)
					# Take Karn if you already have Tron
					if card_chosen == 0 and "Karn" in temp_cards:
						card_chosen = 1
						hand.append("Karn")
					elif card_chosen == 0 and "star" in temp_cards:
						card_chosen = 1
						hand.append("star")
				if "star" in hand and not stop_playing_stars:
					#Play your last star
					hand.remove("star")
					battlefield.append("star")
		# Use a map if you have it
		elif "map" in battlefield:
			# Use Map
			battlefield.remove("map")
			for tutored_land in ["Mine", "PP", "Tower"]:
				if tutored_land not in battlefield and tutored_land in deck:
					deck.remove(tutored_land)
					hand.append(tutored_land)
	else:
		# No land played yet
		# Use a star if you have it
		if "star" in battlefield:
			# Use star 
			battlefield.remove("star")
			# Draw a card
			new_card = random.choice(deck)
			hand.append(new_card)
			deck.remove(new_card)
			
			# Playing a land
			for land in ["Mine", "PP", "Tower"]:
				if lands_played_this_turn == 0 and land in hand and land not in battlefield:
					hand.remove(land)
					battlefield.append(land)
					lands_played_this_turn = 1
			if lands_played_this_turn == 0:
				if "stir" in hand:
					#Resolve Stirrings
					temp_cards = random.sample(deck, 5)
					card_chosen = 0
					for card in temp_cards:
						deck.remove(card)
						if card_chosen == 0 and card in ["Mine", "PP", "Tower"] and card not in battlefield and card not in hand:
							card_chosen = 1
							hand.append(card)
					if card_chosen == 1:
						# You found a land
						# Playing a land
						for land in ["Mine", "PP", "Tower"]:
							if lands_played_this_turn == 0 and land in hand and land not in battlefield:
								hand.remove(land)
								battlefield.append(land)
								lands_played_this_turn = 1
						# Do you have a star?
						if "star" in hand:
							# Play a star
							hand.remove("star")
							battlefield.append("star")
						# End turn
					else:
						# You only have one land on Turn 2, so no Turn 3 Karn
						return False, opening
			else:
				# You played a land.
				# Do you have Scrying?
				if "scry" in hand:
					# Play Scrying
					hand.remove("scry")
					for tutored_land in ["Mine", "PP", "Tower"]:
						if tutored_land not in battlefield and tutored_land in deck:
							deck.remove(tutored_land)
							hand.append(tutored_land)
					# END TURN
				else:
					if "star" in hand:
						#Play and use a star
						hand.remove("star")
						# Draw a card
						new_card = random.choice(deck)
						hand.append(new_card)
						deck.remove(new_card)
						stop_playing_stars = True
					if "stir" in hand:
						#Resolve Stirrings
						temp_cards = random.sample(deck, 5)
						card_chosen = 0
						for card in temp_cards:
							deck.remove(card)
							if card_chosen == 0 and card in ["Mine", "PP", "Tower"] and card not in battlefield and card not in hand:
								card_chosen = 1
								hand.append(card)
						# Take Karn if you already have Tron
						if card_chosen == 0 and "Karn" in temp_cards:
							card_chosen = 1
							hand.append("Karn")
						elif card_chosen == 0 and "star" in temp_cards:
							card_chosen = 1
							hand.append("star")
					if "star" in hand and not stop_playing_stars:
						#Play your last star
						hand.remove("star")
						battlefield.append("star")
		else:
			# You only have one land on Turn 2, so no Turn 3 Karn
			return False, opening
	
	# Turn 3
	#########
	lands_played_this_turn = 0
	
	# Draw a card
	new_card = random.choice(deck)
	hand.append(new_card)
	deck.remove(new_card)
	
	#Playing a land
	for land in ["Mine", "PP", "Tower"]:
		if lands_played_this_turn == 0 and land in hand and land not in battlefield:
			hand.remove(land)
			battlefield.append(land)
			lands_played_this_turn = 1
	
	if "star" in battlefield:
		battlefield.remove("star")
		# Draw a card
		new_card = random.choice(deck)
		hand.append(new_card)
		deck.remove(new_card)
	
	#Play Karn
	if "Mine" in battlefield and "PP" in battlefield and "Tower" in battlefield:
		opening[4] += 1
		if "Karn" in hand:
			return True, opening
		else: 
			return False, opening
	else:
		return False, opening

####
## Run simulations
for i in range(N):
	state = game(on_the_draw)
	map_opening += state[1][0]
	star_opening += state[1][1]
	other_opening += state[1][2]
	hard_opening += state[1][3]
	turn_3_tron += state[1][4]
	if state[0]:
		count_turn_3_karn += 1
	if state[0] and state[1][3]:
		hard_success += 1

####
## Compute percentages
percentage_turn_3_karn = 100 * float(count_turn_3_karn) / N
percentage_turn_3_tron = 100 * float(turn_3_tron) / N
percentage_map = 100 * float(map_opening) / N
percentage_star = 100 * float(star_opening) / N
percentage_other = 100 * float(other_opening) / N
percentage_hard = 100 * float(hard_opening) / N
percentage_hard_success = 100 * float(hard_success) / hard_opening

#####
## Display results
print( "Turn 3 Tron {}".format( percentage_turn_3_tron ))
print( "Turn 3 Karn {}".format( percentage_turn_3_karn ))
print( "Map Openings: {}".format( percentage_map ))
print( "Star Openings: {}".format( percentage_star ))
print( "Other Openings: {}".format( percentage_other ))
print( "Hard Openings: {}".format( percentage_hard ))
print( "Hard successes: {}".format( percentage_hard_success ))
