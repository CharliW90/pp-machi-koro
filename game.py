import time
from tabulate import tabulate
from reference import reference, credits
from coins.bank import Bank
from player import Player, reset as reset_player_names
from cards import Deck
from actions.dice import roll_dice
from actions.build import build_action
from setup import determine_player_one, set_turn_orders

class Game:
  name = "Machi Koro"

  def __init__(self, player_names: list[str], rounds: int | None = None):
    self.initialised = False
    self.players = player_names
    self.player_count = len(player_names)
    self.bank: Bank = Bank()
    self.deck: Deck = Deck(self.player_count)
    self.round: int = 0
    self.limit_rounds = rounds
    self.initialised = True
    self.in_progress = False

  @property
  def initialised(self) -> bool:
    return self.__initialised
  @initialised.setter
  def initialised(self, trigger: bool):
    if hasattr(self, "initialised"):
      if self.initialised: raise Exception("Game already initialised - cannot initialise again.")
    self.__initialised = trigger

  @property
  def in_progress(self) -> bool:
    return self.__in_progress
  @in_progress.setter
  def in_progress(self, trigger: bool):
    if hasattr(self, "in_progress"):
      if self.in_progress: raise Exception("Game already in progress - cannot set value again.")
    self.__in_progress = trigger

  @property
  def players(self) -> list[Player]:
    return self.__players
  @players.setter
  def players(self, names: list[str]) -> None:
    if self.__initialised: raise PermissionError("Sorry, but you can't edit games")
    if not isinstance(names, list): raise ValueError(f"Player names must be provided as a List - {names} is a {type(names)}")
    if not 2 <= len(names) <= 4: raise ValueError(f"This is a game for 2 to 4 players only!  You have requested {len(names)} players.")
    generated_players = []
    for i, name in enumerate(names):
      if not isinstance(name, (str)): raise ValueError(f"Provided names must be plain strings - {name} is a {type(name)}.")
      generated_players.append(Player(str(name), i))
    self.__players = generated_players
  
  @property
  def player_count(self) -> int:
    return self.__player_count
  @player_count.setter
  def player_count(self, count: int) -> None:
    if self.__initialised: raise PermissionError("Sorry, but you can't edit games")
    if not 2 <= count<= 4: raise ValueError(f"This is a game for 2 to 4 players only!  You have requested {count} players.")
    self.__player_count = count

  @property
  def limit_rounds(self):
    return self.__rounds
  @limit_rounds.setter
  def limit_rounds(self, value):
    if self.__initialised: raise PermissionError("Sorry, but you can't edit games")
    if value:
      if value > 50: raise ValueError(f"{value} rounds is too high - if you don't want to limit the number of rounds playable, simply omit this parameter.")
      self.__rounds = value
    else:
      self.__rounds = None
  
  def __str__(self):
    players = [f"{player.colorize}{player.name}{player.reset}" for player in self.__players]
    return f"This is a game of {self.name}!\nIt has {self.player_count} players - {', '.join(players)}.\nWe are on round {self.round}"

  def notify(self, message: str) -> None:
    for line in message.splitlines():
      print(f"{reference['shortcuts']['notification_start']}{line}{reference['shortcuts']['notification_end']}")

  def list_affordable_cards(self, player: Player) -> list[tuple[str, str]]:
    available_cards = self.deck.contents()
    affordable_cards = []
    players_landmarks = player.cards.landmarks
    for landmark in players_landmarks:
      style = "\x1b[9;2m" if landmark.cost > player.get_balance() else "\x1b[3;32m"
      reset = "\x1b[0m"
      available_cards.append([
        f"{landmark.colorize}{landmark.title}{landmark.reset}\n{landmark.colorize}- Permanent Ability{landmark.reset}",
        f"{landmark.colorize}{landmark.description.splitlines()[0]}{landmark.reset}\n{landmark.colorize}(your turn only){landmark.reset}",
        f"{landmark.colorize}{landmark.title}{landmark.reset}\n{style}{landmark.cost} coins{reset}",
        f"Qty: {int(not landmark.built)}",
        ])
    for [title, _, cost, qty] in available_cards:
      available = int(qty.split(': ')[1])
      price = int(repr(cost).split("2m")[1].split(' ')[0])
      if price <= player.get_balance() and available > 0:
        card_title = title.splitlines()[0]
        clean_title = repr(card_title).split("74m")[1].split("\\")[0] # strip away the ANSI colour codes
        affordable_cards.append((f"{card_title}: Purchase Price: {cost} - BUY?", clean_title))
    return affordable_cards

  def display_cards_to_player(self, player: Player) -> None:
    available_cards = self.deck.contents(player.get_balance())
    players_landmarks = player.cards.landmarks
    for landmark in players_landmarks:
      style = "\x1b[9;2m" if landmark.cost > player.get_balance() else "\x1b[3;32m"
      reset = "\x1b[0m"
      available_cards.append([
        f"{landmark.colorize}{landmark.title}{landmark.reset}\n{landmark.colorize}- Permanent Ability{landmark.reset}",
        f"{landmark.colorize}{landmark.description.splitlines()[0]}{landmark.reset}\n{landmark.colorize}(your turn only){landmark.reset}",
        f"{style}{landmark.cost} coins{reset}",
        f"Qty: {int(not landmark.built)}",
        ])
    print(tabulate(available_cards, ["Name", "Action", "Cost", "Remaining"]))

  def take_card_from_stack(self, cardTitle: str):
    card, pile, qty = self.deck.remove(cardTitle)
    self.notify(f"Took a {card.title} from the {pile} pile - there are now {qty} cards remaining in this pile")
    return card

  def current_player(self) -> Player:
    if self.in_progress:
      for player in self.players:
        if player.current:
          return player
      raise LookupError(f"Game is in progress, but does not have a current player - something has gone wrong.\n{self.players=}")
    else:
      raise RuntimeError(f"Game has not begun - no current player available.\n{self}")

  def start(self) -> str:
    self.notify(f"{self}")
    time.sleep(0.5)
    player_one = determine_player_one(self.players, self)
    set_turn_orders(self.players, player_one)
    self.players.sort(reverse=True)
    for player in self.players:
      player.receive(self.bank.give_player(3))
      player.initialised = True
      time.sleep(0.2)
    time.sleep(0.5)
    self.in_progress = True
    return self.play()
  
  def resume(self):
    return self.play()
  
  def play(self) -> str:
    self.bank.check(self)
    player_number = self.round % self.player_count
    active_player = self.players[player_number]
    self.round += 1
    active_player.begin_turn()
    time.sleep(1)
    take_turn(self, active_player)

    if active_player.has_won():
      self.notify(f"{active_player} has won!  Congratulations!!\n\nThis game of {self.name} took {self.round} rounds to play.")
      return f"Congratulations {active_player.name}!!"
    else:
      active_player.end_turn()
      if self.limit_rounds:
        if self.round < self.limit_rounds:
          self.notify(f"This is round {self.round + 1} of {self.limit_rounds}")
          return self.play()
        else:
          self.notify(f"You have reached the limit of {self.limit_rounds} rounds.  Game over.")
          raise TimeoutError(f"Completed {self.round}/{self.limit_rounds} rounds without a winner.")
      else:
        return self.play()

  def end_game(self):
    self.notify("Ending game...")
    self.notify(reset_player_names())
    for line in credits:
      time.sleep(0.8)
      print(line)

  def summary(self) -> list[str]:
    return [f"Game Summary:"]

def take_turn(game, player):
  roll_dice(game, player)
  time.sleep(1)
  build_action(game, player, {'offer_to_show_hand': True, 'offer_to_show_deck': True})
  time.sleep(1)
  return