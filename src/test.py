from treys import Evaluator
from treys import Card
from treys import Deck

cardsArr=[[]]
cardsArr[0].append(Card.new("Ad"))
cardsArr[0].append(Card.new("Kd"))
# cardsArr[0].append(Card.new("Qd"))

board=[
    Card.new("Td"),
    Card.new("Jd"),
    Card.new("Qd")
]
evaluator=Evaluator()
print(evaluator.evaluate(cardsArr[0],board)/6767)
print(evaluator.get_rank_class(evaluator.evaluate(cardsArr[0],board)))
print(evaluator.class_to_string(evaluator.get_rank_class(evaluator.evaluate(cardsArr[0],board))))


# if you have a good chance on river, then you should check or raise
# flop - keep raising
# turn -keep raising