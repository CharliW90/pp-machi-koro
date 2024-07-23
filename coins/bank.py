from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from coins import Coin
  from game import Game

import time
from reference import reference
from .coinage import CoinPiles, Coin
from .transactions import giving, receiving


class Bank:
  def __init__(self) -> None:
    self.name = "The Bank"
    self.colour = 'cyan'
    self.colorize = reference['ansiColours'][self.colour]
    self.reset = reference["ansiColours"]["reset"]
    self.coins = CoinPiles(42, 24, 12)
    self.total = self.coins.total()
    
  def __str__(self) -> str:
    return (
      f"{self.name} contains {self.total} in coinage:\n"
      f"{len(self.coins.coppers)} Copper 'Ones', valuing {sum([coin.value for coin in self.coins.coppers])}\n"
      f"{len(self.coins.silvers)} Silver 'Fives', valuing {sum([coin.value for coin in self.coins.silvers])}\n"
      f"{len(self.coins.golds)} Gold 'Tens', valuing {sum([coin.value for coin in self.coins.golds])}"
    )
  
  def declareAction(self, action: str) -> None:
    print(f"{self.colorize}{action}{self.reset}")

  def givePlayer(self, total: int) -> list[Coin]:
    return giving(self, total)

  def takePayment(self, coins: list[Coin], totalToPay: int) -> list[Coin]:
    payment = receiving(self, coins) # put payment into bank's coin pile
    return giving(self, payment-totalToPay) # give change, if any

  def check(self, game: Game) -> None:
    ones = len(self.coins.coppers)
    fives = len(self.coins.silvers)
    if ones < 5 or fives < 2:
      if ones < 5:
        plural = "" if ones == 1 else "s"
        self.declareAction(f"{self.name} has {ones} copper One coin{plural} remaining - exchanging up with players...")
      elif fives < 2:
        plural = "" if fives == 1 else "s"
        self.declareAction(f"{self.name} has {fives} silver Five coin{plural} remaining - exchanging up with players...")
      for player in game.players:
        time.sleep(0.2)
        coins = player.giveAll()
        time.sleep(0.5)
        player.receive(self.exchange(coins))
        time.sleep(0.3)

  def exchange(self, coins: list[Coin]) -> list[Coin]:
    intake = receiving(self, coins) # put all coins into the bank's coin pile
    return self.givePlayer(intake) # give back the same value in coins, starting with highest denomination

