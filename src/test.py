from blackjackk import blackjack

class Test:
    def __init__(self, strategy_name, cards):
        self.strategy_name = strategy_name

        print("Player strategy:", self.strategy_name)

        this_table = blackjack.Table(4, 0.75)
        this_table.shoe.cards=[("2d",[2],"2")]
        for card in cards:
            this_table.shoe.cards.append(card)

        new_deck = blackjack.Deck()

        this_table.shoe.cards = this_table.shoe.cards + new_deck.cards

        return this_table.play_one_round(self.strategy_name)    # Play a game.