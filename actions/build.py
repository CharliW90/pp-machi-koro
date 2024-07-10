import inquirer
from reference import shortcuts, MyTheme

def buildAction(game, player, offerToShowDeck):
  affordableCards = game.listAffordableCards(player)
  affordableCards.insert(0,("Build Nothing", "Nothing"))
  if offerToShowDeck:
    shortcuts['notify'](f"Time to build an establishment, {player.name}!  You have {player.getBalance()} coins")
    affordableCards.insert(0,("Look at available cards", "Display"))
  else:
    shortcuts['notify'](f"Time to make a decision, {player.name}!  You have {player.getBalance()} coins")
  options = [
    inquirer.List('build',
                  message=f"{player.colorize}Build an establishment?{player.reset}",
                  choices=affordableCards)
  ]

  action = inquirer.prompt(options, theme=MyTheme(player))
  return action['build']

def handleBuilding(game, player, cardTitle):
  if cardTitle == 'Nothing':
    player.declareAction(f"{player.name} chose to build nothing this round - holding onto their {player.getBalance()} coins!")
    return
  elif cardTitle == 'Display':
    game.displayCardsToPlayer(player)
    finalDecision = buildAction(game, player, False)
    card = game.getCardFromStack(finalDecision)
    print(card)
    return finalDecision
  else:
    card = game.getCardFromStack(cardTitle)
    print(card)
    return cardTitle
