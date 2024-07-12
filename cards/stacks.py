from collections import Counter
from reference import shortcuts
from cards.blue import *
from cards.green import *
from cards.red import *
from cards.purple import *
from cards.landmark import *

class Deck:
  def __init__(self, players):
    self.wheatFields = [WheatField() for _ in range(6)]
    self.ranches = [Ranch() for _ in range(6)]
    self.bakeries = [Bakery() for _ in range(6)]
    self.cafes = [Cafe() for _ in range(6)]
    self.convenienceStores = [ConvenienceStore() for _ in range(6)]
    self.forests = [Forest() for _ in range(6)]
    self.majorEstablishments = [card for card in [Stadium(), TVStation(), BusinessCentre()] for _ in range(players)]
    self.cheeseFactories = [CheeseFactory() for _ in range(6)]
    self.furnitureFactories = [FurnitureFactory() for _ in range(6)]
    self.mines = [Mine() for _ in range(6)]
    self.familyRestaurants = [FamilyRestaurant() for _ in range(6)]
    self.appleOrchards = [AppleOrchard() for _ in range(6)]
    self.farmersMarkets = [FarmersMarket() for _ in range(6)]
  
  def contents(self, cash = 100):
    cardStacks = [stack for stack in [getattr(self, attribute) for attribute in dir(self)] if isinstance(stack, list)]
    cardCounts = [[title, count] for stack in cardStacks for title, count in Counter(card.title for card in stack).items()]
    
    allCards = ()       # here we will store a multiline f-string per card - tuple because immutable and indexable
    allCardIndexes = [] # here we will store the zIndex per card
    mapOfCards = {}     # here we will map the zIndex of a card to its position in allCards tuple

    for [title, qty] in cardCounts:
      cards = getattr(self, str(lookup(title)))
      card = cards[0]
      mapOfCards[str(card.zIndex)] = len(allCards)
      allCardIndexes.append(card.zIndex)

      style = shortcuts['affordable'] if card.cost <= cash else shortcuts['unaffordable']
      styleReset = shortcuts['reset']

      allCards += ([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{'s' if card.cost > 1 else ''}{styleReset}",
        f"Qty: {qty}",
        ],)   # <= that comma makes this a tuple, and you can add a tuple to a tuple
      
    allCardIndexes.sort()
    sortedCards = [allCards[mapOfCards[str(index)]] for index in allCardIndexes]
    return sortedCards

  def add(self, card):
    pile = lookup(card.title)
    stack = getattr(self, str(pile))
    stack.append(card)
    print(f"Added {card.title} to the {pile or 'major establishments'} pile - there are now {len(stack)} cards in this pile")
    return len(stack)
  
  def remove(self, name):
    pile = lookup(name)
    stack = getattr(self, str(pile))
    card = stack.pop()
    return card, pile, len(stack)

class Hand():
  def __init__(self):
    self.blue = [WheatField()]
    self.green = [Bakery()]
    self.red = []
    self.purple = []
    self.landmarks = [TrainStation(), ShoppingMall(), AmusementPark(), RadioTower()]
  
  def add(self, card):
    stack = getattr(self, card.colour)
    stack.append(card)
  
  def remove(self, colour, name):
    stack = getattr(self, colour)
    for i, card in enumerate(stack):
      if card.title == name:
        stack.pop(i)
        return card
    return ValueError(f"No {name} card")

  def contents(self):
    allCards = []
    cardStacks = []
    for attribute in dir(self):
      actual = getattr(self, attribute)
      if isinstance(actual, list):
        cardStacks.append(actual)
    cardCounts = []
    allCardIndexes = []
    mapOfCards = {}
    for stack in cardStacks:
      counts = Counter(card.title for card in stack)
      cardCounts.extend([title, count] for title, count in counts.items())
      
      for title, count in counts.items():
        card = [card for card in stack if card.title == title][0]
        mapOfCards[str(card.zIndex)] = len(allCards)
        allCardIndexes.append(card.zIndex)
        if card.cardType == "Landmark":
          if card.built:
            allCards.append([
              f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> Landmark Card <{card.reset}",
              f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
              f"{card.colorize}Built!{card.reset}",
              ])
          else:
            allCards.append([
              f"\x1b[9;2m{card.colorize}{card.title}{card.reset}\x1b[0m\n{card.colorize}> Unbuilt Landmark <{card.reset}",
              f"\x1b[9;2m{card.colorize}{card.description.splitlines()[0]}{card.reset}\x1b[0m\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
              f"{card.colorize}Not yet built...{card.reset}",
              ])
        else:
          allCards.append([
            f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
            f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
            f"{card.colorize}Qty: {count}{card.reset}",
            ])
    sortedCards = []
    allCardIndexes.sort()
    for index in allCardIndexes:
      cardsIndex = mapOfCards[str(index)]
      card = allCards[cardsIndex]
      sortedCards.append(card)
    return sortedCards

def lookup(name):
  match name:
    case "Wheat Field":
      return "wheatFields"
    case "Ranch":
      return "ranches"
    case "Bakery":
      return "bakeries"
    case "Cafe":
      return "cafes"
    case "Convenience Store":
      return "convenienceStores"
    case "Forest":
      return "forests"
    case "Stadium" | "TV Station" | "Business Centre": 
      return "majorEstablishments"
    case "Cheese Factory":
      return "cheeseFactories"
    case "Furniture Factory":
      return "furnitureFactories"
    case "Mine":
      return "mines"
    case "Family Restaurant":
      return "familyRestaurants"
    case "Apple Orchard":
      return "appleOrchards"
    case "Farmers Market":
      return "farmersMarkets"
    case _:
      print(f"Error: {name} is not one of the expected names")
      return
