from blackjackk import blackjack

def black(strategy_name, cards):
    strategy_name = strategy_name
    print("Player strategy:", strategy_name)
    this_table = blackjack.Table(4, 0.75)
    this_table.shoe.cards=[("2d",[0],"2")]
    for card in cards:
        this_table.shoe.cards.append(card)
    new_deck = blackjack.Deck()
    this_table.shoe.cards = this_table.shoe.cards + new_deck.cards
    return this_table.play_one_round(strategy_name)    # Play a game.

result = black("Basic Strategy Section 4",[("6d",[6],'6'),("Kd",[10],'K'),("3s",[3],'3')])
print(result)