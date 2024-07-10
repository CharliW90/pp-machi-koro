import inquirer
from reference import MyTheme

def buildAction(game, player, settings):
  affordableCards = game.listAffordableCards(player)
  showHand = settings.get("offerToShowHand")
  showDeck = settings.get("offerToShowDeck")
  affordableCards.insert(0,(f"[X] {player.colorize}Build Nothing{player.reset}", "Nothing"))
  if showDeck:
    affordableCards.insert(0,(f"[?] {player.colorize}Look at available cards{player.reset}", "Display"))
  if showHand:
    affordableCards.insert(0,(f"[?] {player.colorize}Look at your cards{player.reset}", "Look"))
  if showDeck and showHand:
    game.notify(f"Time to build an establishment, {player.name}!  You have {player.getBalance()} coins")
  else:
    game.notify(f"Time to make a decision, {player.name}!  You have {player.getBalance()} coins")
  options = [
    inquirer.List('build',
                  message=f"{player.colorize}Build an establishment?{player.reset}",
                  choices=affordableCards)
  ]

  action = inquirer.prompt(options, theme=MyTheme(player))
  choice = action['build'] # type: ignore
  built = handleBuilding(game, player, choice, settings)
  return built

def handleBuilding(game, player, cardTitle, settings):
  if cardTitle == 'Nothing':
    cash = player.getBalance()
    statement = f" - holding onto their {cash} coins!" if cash > 1 else "."
    player.declareAction(f"{player.name} built nothing this round{statement}")
    return
  elif cardTitle == 'Look':
    settings["offerToShowHand"] = False
    player.viewHand()
    buildAction(game, player, settings)
    return
  elif cardTitle == 'Display':
    settings["offerToShowDeck"] = False
    game.displayCardsToPlayer(player)
    buildAction(game, player, settings)
    return
  else:
    card = game.takeCardFromStack(cardTitle)
    built = player.build(card, game.bank)
    if not built:
      raise ChildProcessError("Something went wrong when trying to build - sorry!")
    return
