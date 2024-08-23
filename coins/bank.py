from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from coins import Coin
  from game import Game
  from player import Player

import time
from reference import reference
from .coinage import CoinPiles
from .transactions import giving, receiving

class Bank:
  def __init__(self) -> None:
    self.name = "The Bank"
    self.colour = 'cyan'
    self.colorize = reference['ansi_colours'][self.colour]
    self.reset = reference["ansi_colours"]["reset"]
    self.coins = CoinPiles(42, 24, 12)
    self.total = self.coins.total()

  def __str__(self) -> str:
    return f"This is {self.name}, containing {self.total} in cash."
    
  def __repr__(self) -> str:
    return (
      f"Bank({self.name} contains {self.total} in coinage:[\n"
      f"\t{len(self.coins.coppers)} Copper 'Ones', valuing {sum([coin.value for coin in self.coins.coppers])},\n"
      f"\t{len(self.coins.silvers)} Silver 'Fives', valuing {sum([coin.value for coin in self.coins.silvers])},\n"
      f"\t{len(self.coins.golds)} Gold 'Tens', valuing {sum([coin.value for coin in self.coins.golds])}])"
    )
  
  def declare_action(self, action: str) -> None:
    print(f"{self.colorize}{action}{self.reset}")

  def give_player(self, total: int, silent=False) -> list[Coin]:
    return giving(self, total, silent)

  def take_payment(self, coins: list[Coin], total_to_pay: int, silent=False) -> list[Coin]:
    """Takes in a payment in the form of a list of one or more Coin objects, and a total amount to be paid.
    Returns any change due, in the form of a list of one or more Coin objects."""
    payment = receiving(self, coins, silent) # put payment into bank's coin pile
    change = payment - total_to_pay
    return giving(self, change, silent) # give change

  def check(self, game: Game) -> None:
    ones = len(self.coins.coppers)
    fives = len(self.coins.silvers)
    if ones < 5 or fives < 2:
      if ones < 5:
        plural = "" if ones == 1 else "s"
        self.declare_action(f"{self.name} has {ones} copper One coin{plural} remaining - exchanging up with players...")
      elif fives < 2:
        plural = "" if fives == 1 else "s"
        self.declare_action(f"{self.name} has {fives} silver Five coin{plural} remaining - exchanging up with players...")
      for player in game.players:
        time.sleep(0.2)
        coins = player.give_all()
        time.sleep(0.5)
        player.receive(self.exchange(coins))
        time.sleep(0.3)

  def exchange(self, coins: list[Coin], silent=False) -> list[Coin]:
    intake = receiving(self, coins, silent) # put all coins into the bank's coin pile
    return giving(self, intake, silent)     # give back the same value in coins, starting with highest denomination
  
  def handle_transfer(self, payor: Player, amount: int, payee: Player) -> None:
    bank_balance: int = self.total
    payor_balance: int = payor.get_balance()                                  # get the payor's initial balance
    payee_balance: int = payee.get_balance()                                  # get the payee's initial balance
    receiving(self, payor.give_all(True), True)                               # empty the payor's cash into the bank
    receiving(self, payee.give_all(True), True)                               # empty the payee's cash into the bank
    payment: int = amount if payor_balance >= amount else payor_balance       # make sure we only pay what the payor can afford
    payor.receive(giving(self, payor_balance - payment, True), True)          # return the payor's cash, less the amount paid
    payee.receive(giving(self, payee_balance + payment, True), True)          # return the payee's cash, plus the amount paid
    if (payor_balance + payee_balance) == (payor.get_balance() + payee.get_balance()) and (bank_balance == self.total):
      # the bank's balance should not have been affected, and the two players should have the same amount of money between them
      payor.declare_action(f"{payor.name} is giving {payment if payment == amount else f'all {payment} of their'} coins ==>")
      payee.declare_action(f"==> {payee.name} received {payment} coins")
    else:
      new_payor_balance: int = payor.get_balance()
      new_payee_balance: int = payee.get_balance()
      new_bank_balance: int = self.total
      raise ArithmeticError(f"Payment calculation incorrect:\n{payor_balance=}, {payee_balance=}: {(payor_balance + payee_balance)}\n{new_payor_balance=}, {new_payee_balance=}: {(new_payor_balance + new_payee_balance)}\n{bank_balance=}, {new_bank_balance=}")
    