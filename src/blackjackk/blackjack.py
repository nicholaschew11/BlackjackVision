# Blackjack simulator.

import random

# See - https://en.wikipedia.org/wiki/Standard_52-card_deck
class Deck:

    # Create a new deck of cards.
    def __init__(self):

        # [(name of the rank, [list of possible values], card_value)]
        # For example, ("2", [2]), ("K", [10]), ("A", [1, 11])
        ranks = []

        # Add the pip ranks, 2 through 10.
        for i in range(2, 11):
            ranks.append((str(i), [i], str(i)))

        # Add the court ranks, Jack, Queen, King.
        court = ["J", "Q", "K"]
        for c in court:
            ranks.append((c, [10], "10"))

        # Add the Ace.
        ranks.append(("A", [1, 11], "A"))

        # Make 1 deck of cards.
        self.cards = []
        suits = ["c", "d", "h", "s"]

        for r in ranks:
            (name, value_list, card_value) = r

            for s in suits:
                card_name = name + s                        # For example "8" + "♥".
                self.cards.append((card_name, value_list, card_value))

    # Shuffle the deck.
    def shuffle(self):
        random.shuffle(self.cards)

class Card_Counting:

    def __init__(self):
        self.running_count = 0
        self.true_count = 0

    def reset(self):
        self.running_count = 0
        self.true_count = 0
        self.bet_size = 0

    def print(self):
        print("Running count=%d, True count=%d, Bet size=%d" % (self.running_count, self.true_count, self.bet_size))

    def adjust_count(self, card, shoe_size, betting_unit):
        (_, _, card_value) = card

        count_map = {"2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 0, "8": 0, "9": 0, "10": -1, "A": -1}

        self.running_count += count_map.get(card_value)     # Adjust the running count based on value of this card.

        decks_in_shoe = shoe_size / 52

        self.true_count = int(self.running_count / decks_in_shoe)

        self.bet_size = (self.true_count - 1) * betting_unit
        if self.bet_size < 0:                               # Can't bet a -ve stake :)
            self.bet_size = 0


# See - https://en.wikipedia.org/wiki/Shoe_(cards)
class Shoe:

    def __init__(self):
        self.cards = []                                     # Cards currently in the shoe.

        # Default values for these two attributes.
        self.decks = 4                                      # Number of decks in the shoe when full.
        self.penetration = 75 / 100                         # Percentage of cards to be dealt before refilling shoe.

        self.card_count = Card_Counting()                   # Create an object to do card counting.

    # Print the first 10 cards in shoe, plus number of cards in shoe.
    def print(self):
        print("Shoe: ", end="")
        for c in self.cards[0:10]:
            (card, value_list, card_value) = c
            print(card, end=" ")
        print("Number of cards", len(self.cards))

    # Shuffle all of the cards in the shoe.
    def shuffle(self):
        random.shuffle(self.cards)

    # If the shoe of cards is getting small, then replenish it.
    def replenish(self):
        if len(self.cards) <= ((1 - self.penetration) * self.decks * 52):
            self.cards = []                                 # Remove the remaining cards from the shoe.
            for d in range(self.decks):
                new_deck = Deck()
                self.cards = self.cards + new_deck.cards

            self.shuffle()                                  # If cards were added, then shuffle the cards in the shoe.
            self.card_count.reset()                         # Reset the card count to zero.

    # Return the number of cards left in the shoe.
    def shoe_size(self):
        return len(self.cards)

    # Remove the card from the front of the shoe. Return it as value.
    def draw_one_card(self):

        # For safety, ensure that there is at least 1 card in the shoe at all times.
        if self.shoe_size() <= 1:
            self.replenish()

        choice = self.cards.pop(0)                          # Take the first card off the front of the shoe.
        return choice                                       # Return the chosen card.


class Hand:
    def __init__(self, name, stake, ancestors):
        self.name = name                        # User friendly name for the hand of cards.
        self.stake = stake
        self.ancestors = ancestors              # How many ancestors does this hand have?
        self.cards = []                         # The hand starts with an empty list of cards.
        self.value = 0                          # Current value of the hand.
        self.busted = False                     # Is the hand busted?
        self.blackjack = False

    # Print a summary of the hand.
    def print(self):
        print(self.name, end=":")
        for c in self.cards:
            (card, _, _) = c
            print("", card, end="")
        print(", Value=%d" % self.value, end="")
        if self.busted:
            print(", Busted", end="")
        else:
            print(", Not-busted", end="")
        if self.blackjack:
            print(", Blackjack", end="")
        else:
            print(", No Blackjack", end="")
        print(", Stake=£%d" % self.stake, end="")
        print()

    # Calculate the points value of a hand. If the hand is busted, it sets the busted attribute to True.
    # For hands containing 1 or more aces, there are multiple possible value. This method returns the highest
    # non-busted value possible. If the hand is busted, it returns the lowest points value possible.
    def calculate_value(self):
        possible_values = [0]             # List of all possible values of this hand.

        for c in self.cards:
            (_, value_list, _) = c

            new_possible_values = []
            for p in possible_values:
                for v in value_list:
                    new_possible_values.append(p + v)
            possible_values = new_possible_values

        self.value = 0
        self.busted = True
        for p in possible_values:
            if p > self.value and p <=21:
                self.value = p         # We found a new higher, non-busted value.
                self.busted = False

        # If we busted, it is still nice to set the value to the lowest possible value the cards in the hand can make.
        if self.busted:
            self.value = min(possible_values)

    # This method should only be called for the 1st hands (player or dealer) of each round. Hands created from
    # splits cannot be blackjacks.
    def check_blackjack(self):
        if self.value == 21 and self.ancestors == 0:    # Check no ancestors. Hands with ancestors are not 1st hands.
            self.blackjack = True

    # Add the parm card to this hand.
    def receive_card(self, card):
        self.cards.append(card)         # Append the parm card to the list of cards in this hand.
        self.calculate_value()          # Recalculate the value of this hand.


class Table:

    def __init__(self, decks, penetration):
        self.shoe = Shoe()                              # Create an empty card shoe.

        # Overwrite the shoe's defaults for decks and penetration with the table's parms.
        self.shoe.decks = decks
        self.shoe.penetration = penetration

        self.shoe.replenish()                           # ... fill the shoe with normal, randomised cards.

        # Normal stake is £4. Chosen as it can be split into 4 hands while remaining an integer.
        self.betting_unit = 4
        self.blackjack_value = 3 / 2                    # Eg. £4 bet wins £6 for a blackjack (and stake returned too).

        self.rounds_played = 0
        self.hands_played_by_player = 0
        self.total_staked = 0
        self.amount_won_or_lost = 0                     # +ve number means the player is in profit, -ve means loss.

        self.dealer = None                              # The dealer's current hand on the table.
        self.player_hands = []                          # List of player hands currently on the table.

    # Update running totals to reflect money staked by player.
    def invest(self, stake):
        self.total_staked += stake
        self.amount_won_or_lost -= stake

    # Double down the stake on this hand.
    def double_down(self, hand):
        self.invest(hand.stake)
        hand.stake += hand.stake

    # Add parm winnings to player running total or money won (or lost).
    def win(self, winnings):
        self.amount_won_or_lost += winnings

    # Deal one card from the front of the shoe to one of the hands.
    def deal_one_card(self, hand):
        card = self.shoe.draw_one_card()                # Draw a card from the shoe,
        hand.receive_card(card)                         # ... and add it to the parm hand.
        return card    
    def insert_one_card(self, hand, assignedCard):
        card = assignedCard                     # Assign the card
        hand.receive_card(card)                         # ... and add it to the parm hand.
        return card                                    # Return the card to caller.

    # When a card is dealt face up, it's value is visible, so the card count can be adjusted.
    def deal_one_card_face_up(self, hand):
        card = self.deal_one_card(hand)
        current_shoe_size = self.shoe.shoe_size()

        # This card has been dealt face up, so adjust the card count.
        self.shoe.card_count.adjust_count(card, current_shoe_size, self.betting_unit)

    def print_table_status(self):
        print("Rounds played=%d, Total staked=£%d, Amount won or lost=£%d"
              % (self.rounds_played, self.total_staked, self.amount_won_or_lost))

    # This strategy is to Stand on 17 to 21, and to Hit on anything less than 17. In most casinos, this is also the
    # strategy that the Dealer is required to follow.
    def dealer_stategy(self, hand, dealer_up_card):
        while hand.value < 17 and not hand.busted:
            self.deal_one_card_face_up(hand)

    # This section of Basic Strategy looks at the dealer's up card to make a more nuanced decision about whether
    # to Hit or Stand.
    def basic_strategy_section_1(self, hand, dealer_up_card):

        (_, _, dealer_card_value) = dealer_up_card
        finished = False
        moves=[]
        while not finished:
            if hand.value == 12 and dealer_card_value in ["2", "3"] \
               or (hand.value in [12, 13, 14, 15, 16] and dealer_card_value in ["7", "8", "9", "10", "A"]) \
               or hand.value <= 11:
                self.deal_one_card_face_up(hand)            # "Hit"
                moves.append("hit")
            else:
                finished = True
                moves.append("stand")                             # "Stand"
        return moves

    # The section of Basic Strategy introduces rules for when to Double Down.
    def basic_strategy_section_2(self, hand, dealer_up_card):
        (_, _, dealer_card_value) = dealer_up_card

        # It is only possible to Double Down with first 2 cards of the hand on table.
        double_down = False
        if hand.value == 11:
            if dealer_card_value != "A":
                double_down = True
        elif hand.value == 10:
            if not dealer_card_value in ["10", "A"]:
                double_down = True
        elif hand.value == 9 and dealer_card_value in ["3", "4", "5", "6"]:
            double_down = True

        if double_down:                                         # "Double Down"
            self.double_down(hand)
            self.deal_one_card_face_up(hand)                    # One more card only, after Double Down.
            return ["double down"]

        # If we are not doubling down, then play Basic Strategy Section 1.
        else:
            return self.basic_strategy_section_1(hand, dealer_up_card)

    # This section of Basic Strategy introduces rules for player hands that include an ace.
    def basic_strategy_section_3(self, hand, dealer_up_card):

        other_card = ""
        decision = ""

        # Work out the values of both of the player's cards.
        (_, _, player_card_1_value) = hand.cards[0]
        (_, _, player_card_2_value) = hand.cards[1]

        if player_card_1_value == "A":
            other_card = player_card_2_value
        elif player_card_2_value == "A":
            other_card = player_card_1_value

        # Are either of the player's cards an ace?
        if other_card != "":
            (_, _, dealer_card_value) = dealer_up_card

            if other_card in ["8", "9", "10"]:
                decision = "Stand"
            elif other_card == "7":
                if dealer_card_value in ["2", "7", "8"]:
                    decision = "Stand"
                elif dealer_card_value in ["9", "10", "A"]:
                    decision = "Hit"
                else:
                    decision = "Double Down"
            elif other_card == "6":
                if dealer_card_value in ["3", "4", "5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"
            elif other_card in ["4", "5"]:
                if dealer_card_value in ["4", "5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"
            elif other_card in ["2", "3"]:
                if dealer_card_value in ["5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"

        if other_card == "":                                        # If neither card is an ace,
            return self.basic_strategy_section_2(hand, dealer_up_card)     # ... continue with Section 2 strategy.

        elif decision == "Double Down":
            self.double_down(hand)                                  # Double stake.
            self.deal_one_card_face_up(hand)                                # One more card only, after Double Down.
            return ["double down"]

        elif decision == "Hit":
            self.deal_one_card_face_up(hand)                        # "Hit",
            val=self.basic_strategy_section_2(hand, dealer_up_card)
            val.insert(0,"hit")     # ... and then continue with Section 2 strategy.
            return val

        elif decision != "Stand":                                   # "Stand" means do nothing, but otherwise,
            return self.basic_strategy_section_2(hand, dealer_up_card)     # ... continue with Section 2 strategy.
        return ['stand']

    # This section of Basic Strategy introduces rules for player hands which with matching card values, which may
    # be Split.
    def basic_strategy_section_4(self, hand, dealer_up_card):

        # Work out the values of both of the player's cards.
        (_, _, player_card_1_value) = hand.cards[0]
        (_, _, player_card_2_value) = hand.cards[1]

        # Rule is that 1st hand can only be split twice. Ie. no more than 4 hands for 1 player in a single game.
        # And a hand can only be split if both cards are equal value.
        if hand.ancestors <= 1 and player_card_1_value == player_card_2_value:

            (_, _, dealer_card_value) = dealer_up_card

            decision_map = \
            {("A", "2"): "SP", ("A", "3"): "SP", ("A", "4"): "SP", ("A", "5"): "SP", ("A", "6"): "SP", ("A", "7"): "SP", ("A", "8"): "SP", ("A", "9"): "SP", ("A", "10"): "SP", ("A", "A"): "SP",
            ("10", "2"): "S", ("10", "3"): "S", ("10", "4"): "S", ("10", "5"): "S", ("10", "6"): "S", ("10", "7"): "S", ("10", "8"): "S", ("10", "9"): "S", ("10", "10"): "S", ("10", "A"): "S",
            ("9", "2"): "SP", ("9", "3"): "SP", ("9", "4"): "SP", ("9", "5"): "SP", ("9", "6"): "SP", ("9", "7"): "S", ("9", "8"): "SP", ("9", "9"): "SP", ("9", "10"): "S", ("9", "A"): "S",
            ("8", "2"): "SP", ("8", "3"): "SP", ("8", "4"): "SP", ("8", "5"): "SP", ("8", "6"): "SP", ("8", "7"): "SP", ("8", "8"): "SP", ("8", "9"): "SP", ("8", "10"): "SP", ("8", "A"): "SP",
            ("7", "2"): "SP", ("7", "3"): "SP", ("7", "4"): "SP", ("7", "5"): "SP", ("7", "6"): "SP", ("7", "7"): "SP", ("7", "8"): "H", ("7", "9"): "H", ("7", "10"): "H", ("7", "A"): "H",
            ("6", "2"): "SP", ("6", "3"): "SP", ("6", "4"): "SP", ("6", "5"): "SP", ("6", "6"): "SP", ("6", "7"): "H", ("6", "8"): "H", ("6", "9"): "H", ("6", "10"): "H", ("6", "A"): "H",
            ("5", "2"): "D", ("5", "3"): "D", ("5", "4"): "D", ("5", "5"): "D", ("5", "6"): "D", ("5", "7"): "D", ("5", "8"): "D", ("5", "9"): "D", ("5", "10"): "H", ("5", "A"): "H",
            ("4", "2"): "H", ("4", "3"): "H", ("4", "4"): "H", ("4", "5"): "SP", ("4", "6"): "SP", ("4", "7"): "H", ("4", "8"): "H", ("4", "9"): "H", ("4", "10"): "H", ("4", "A"): "H",
            ("3", "2"): "SP", ("3", "3"): "SP", ("3", "4"): "SP", ("3", "5"): "SP", ("3", "6"): "SP", ("3", "7"): "SP", ("3", "8"): "H", ("3", "9"): "H", ("3", "10"): "H", ("3", "A"): "H",
            ("2", "2"): "SP", ("2", "3"): "SP", ("2", "4"): "SP", ("2", "5"): "SP", ("2", "6"): "SP", ("2", "7"): "SP", ("2", "8"): "H", ("2", "9"): "H", ("2", "10"): "H", ("2", "A"): "H"}

            decision = decision_map.get((player_card_1_value, dealer_card_value))
            if decision == "SP":                                        # "Split"
                hand.stake = hand.stake / 2                             # Stake is split between parent and child hands.

                # Add the new child hand to the list of player's hands that are on the table.
                self.player_hands.append(Hand("Child of " + hand.name,
                                              hand.stake,               # New hand has same newly halved stake as parent.
                                              hand.ancestors + 1))      # It has 1 more ancestor than its parent.

                new_hand_index = len(self.player_hands) -1
                self.hands_played_by_player += 1

                # Move 2nd card from parent hand to child hand.
                second_card = hand.cards.pop(1)
                self.player_hands[new_hand_index].receive_card(second_card)

                # Deal a card to parent, so that it has 2 cards again.
                self.deal_one_card_face_up(hand)

                # The parent hand is now a child too.
                hand.ancestors += 1

                # Now apply this strategy to the new version of the parent hand.
                self.basic_strategy_section_4(hand, dealer_up_card)

                # Now work on the child hand.
                self.deal_one_card_face_up(self.player_hands[new_hand_index])

                # Now apply this strategy to the child hand.
                self.basic_strategy_section_4(self.player_hands[new_hand_index], dealer_up_card)

            elif decision == "D":                                       # "Double Down"
                self.double_down(hand)                                  # Double stake.
                self.deal_one_card_face_up(hand)                                # One more card only, after Double Down.
                return ["double down"]

            elif decision == "H":                                       # "Hit"
                self.deal_one_card_face_up(hand)                                # Deal one card to the hand.

                val=self.basic_strategy_section_3(hand, dealer_up_card)     # ... and then continue with Section 3 strategy.
                val.insert(0,"hit")
                return val

            elif decision != "S":                                       # "Stand" means do nothing, but otherwise,
                return self.basic_strategy_section_3(hand, dealer_up_card)     # ... continue with Section 3 strategy.
        else:
            return self.basic_strategy_section_3(hand, dealer_up_card)


        

    def play_one_round(self, strategy_name):

        self.rounds_played += 1                             # Increment number of rounds played on this table.

        # Create a hand of cards for the dealer. Dealer has no money staked.
        self.dealer = Hand("Dealer Hand",
                            0,                              # Dealer has no money staked.
                            0)                              # This hand has no ancestors.

        if verbose:
            self.shoe.card_count.print()  # Print the status of the card counting.

        # If we're doing card counting, then bet according to the calculation of the card counting strategy.
        if strategy_name == "Hi-Lo Card Count":
            this_stake = self.shoe.card_count.bet_size
        else:
            this_stake = self.betting_unit
        self.invest(this_stake)

        # Create a first hand of cards for the player.
        self.player_hands.append(Hand("Player Hand",
                                      this_stake,
                                      0))                   # The player's first hand has no ancestors.
        self.hands_played_by_player += 1

        # Deal first 4 cards in classic order (Player, Dealer, Player, Dealer). 
        self.deal_one_card(self.dealer)                     # Not face up.
        self.deal_one_card_face_up(self.dealer)             # Face up.
        self.deal_one_card_face_up(self.player_hands[0])    # Face up.
        self.deal_one_card_face_up(self.player_hands[0])    # Face up.



        # Check both Player and Dealer's hands for Blackjack on original 2 cards only.
        self.dealer.check_blackjack()
        self.player_hands[0].check_blackjack()

        if self.player_hands[0].blackjack:                  # Player has a Blackjack.
            if self.dealer.blackjack:                       # Dealer also has a Blackjack,
                self.win(self.player_hands[0].stake)        # ... so player wins his stake back.
                return ["Both blackjack ... win your stake back"]
            else:                                           # Player has Blackjack, and dealer doesn't have one,
                # ... so he wins his stake back, plus his stake multiplied by Blackjack odds.
                self.win(self.player_hands[0].stake + self.blackjack_value * self.player_hands[0].stake)
                return ["Blackjack!"]

        # No Blackjack for the player, so proceed to a playing strategy.
        else:
            # The Dealer's up card, is the first card in his hand. Some strategies vary their decisions based upon it.
            dealer_up_card = self.dealer.cards[0]

            # Convert the parm strategy string into a strategy function.
            # Note that card counting is based on Basic Strategy.
            strategy_map = {"Dealer": self.dealer_stategy,
                            "Basic Strategy Section 1": self.basic_strategy_section_1,
                            "Basic Strategy Section 2": self.basic_strategy_section_2,
                            "Basic Strategy Section 3": self.basic_strategy_section_3,
                            "Basic Strategy Section 4": self.basic_strategy_section_4,
                            "Hi-Lo Card Count": self.basic_strategy_section_4}
            strategy = strategy_map.get(strategy_name)

            a=strategy(self.player_hands[0], dealer_up_card)
            # Does the player have any non-busted hands?
            all_player_hands_busted = True
            for ph in self.player_hands:
                if ph.busted == False:
                    all_player_hands_busted = False

            # If player has executed his strategy without busting all of his hands,
            # and the dealer doesn't have a Blackjack...
            # ... then it is the dealer's turn to play.
            if not all_player_hands_busted and not self.dealer.blackjack:

                # First turn over the dealer's second card (index=1), and adjust the card count.
                self.shoe.card_count.adjust_count(self.dealer.cards[1], self.shoe.shoe_size(), self.betting_unit)

                self.dealer_stategy(self.dealer, dealer_up_card)

                # Compare each of the player's hands with the dealer's hand.
                for ph in self.player_hands:
                    if not ph.busted:                       # Only interested in non-busted player hands.

                        # If Dealer has busted, or Player has higher score than Dealer, then pleyer wins.
                        if self.dealer.busted or ph.value > self.dealer.value:
                            self.win(2 * ph.stake)          # Win 1*stake as winnings, plus get stake back.

                        # Dealer and Player have matching scores, so no winner... but Player does get his stake back.
                        elif ph.value == self.dealer.value:
                            self.win(ph.stake)
            return a
        
verbose = False