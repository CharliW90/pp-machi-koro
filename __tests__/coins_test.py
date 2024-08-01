import pytest
from unittest.mock import patch, Mock, create_autospec, call
import random
from reference import reference
from player import Player
from game import Game

from coins.coinage import One, Five, Ten, CoinPiles, Coin
from coins.bank import Bank

class TestCoinage:
  def test_One(self):
    # Arrange
    coin = One()

    # Act / Assert
    assert coin.colour == "Copper"
    assert coin.value == 1
    assert str(coin) == "A single Copper coin, with a value of 1"

  def test_Five(self):
    # Arrange
    coin = Five()

    # Act / Assert
    assert coin.colour == "Silver"
    assert coin.value == 5
    assert str(coin) == "A single Silver coin, with a value of 5"
  
  def test_Ten(self):
    # Arrange
    coin = Ten()

    # Act / Assert
    assert coin.colour == "Gold"
    assert coin.value == 10
    assert str(coin) == "A single Gold coin, with a value of 10"
  
  def test_coinage_comparisons(self):
    # Arrange
    test_coin_A = One()
    test_coin_B = Five()
    test_coin_C = Ten()
    test_coin_D = One()
    test_coin_E = Five()
    test_coin_F = Ten()

    # Act / Assert
    assert test_coin_A == test_coin_D    # value: 1
    assert test_coin_B == test_coin_E    # value: 5
    assert test_coin_C == test_coin_F   # value: 10

    assert test_coin_A != test_coin_E
    assert test_coin_B != test_coin_F
    assert test_coin_C != test_coin_D
    
    assert test_coin_A < test_coin_B < test_coin_C
    assert test_coin_F > test_coin_E > test_coin_D

    assert test_coin_A <= test_coin_D <= test_coin_B <= test_coin_E <= test_coin_C <= test_coin_F
    assert test_coin_F >= test_coin_C >= test_coin_E >= test_coin_B >= test_coin_D >= test_coin_A

  
  def test_CoinPiles_x100(self):
    for _ in range(100):
      # Arrange
      quantities = random_quantities()
      copper, silver, gold = quantities

      # Act
      piles = CoinPiles(copper, silver, gold)

      # Assert
      assert len(piles) == 3
      assert len(piles.coppers) == copper
      assert len(piles.silvers) == silver
      assert len(piles.golds) == gold

      assert piles.total() == sum([gold*10, silver*5, copper])

      assert str(piles) == f"3 piles of coins (Coppers, Silvers and Golds) with a total value of {sum([gold*10, silver*5, copper])}."

      for i, pile in enumerate(piles):
        assert len(pile) == quantities[i]

def random_quantities() -> list:
  low_number = random.randint(0, 3)
  high_number = random.randint(36, 48)
  any_number = random.randint(3, 36)

  quantities = [low_number, high_number, any_number]
  random.shuffle(quantities)

  return quantities

class TestBank:
  def test_Bank_setup(self):
    # Arrange
    test = Bank()

    # Act / Assert
    assert hasattr(test, "name")
    assert test.name == "The Bank"
    assert hasattr(test, "colour")
    assert test.colour == "cyan"
    assert hasattr(test, "colorize")
    assert test.colorize == reference['ansi_colours']['cyan']
    assert hasattr(test, "reset")
    assert test.reset == reference['ansi_colours']['reset']
    assert hasattr(test, "coins")
    assert isinstance(test.coins, CoinPiles)
    assert test.coins.total() == 282
    assert hasattr(test, "total")
    assert test.total == 282
    assert hasattr(test, "declare_action")
    assert hasattr(test, "give_player")
    assert hasattr(test, "take_payment")
    assert hasattr(test, "check")
    assert hasattr(test, "exchange")

    assert str(test) == "This is The Bank, containing 282 in cash."
    assert repr(test) == "Bank(The Bank contains 282 in coinage:[\n\t42 Copper 'Ones', valuing 42,\n\t24 Silver 'Fives', valuing 120,\n\t12 Gold 'Tens', valuing 120])"
    
  def test_Bank_functions_declare_action(self, capsys):
    # Arrange
    expectedMessage = f"{reference['ansi_colours']['cyan']}Hello World!{reference['ansi_colours']['reset']}"
    test = Bank()

    # Act
    test.declare_action("Hello World!")

    # Assert
    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == expectedMessage

  @patch("coins.bank.giving")
  def test_Bank_functions_give_player(self, mocked_giving):
    # Arrange
    mockCoins = random_coins()
    mocked_giving.return_value = mockCoins
    give = sum(coin.value for coin in mockCoins)
    test = Bank()

    # Act
    output = test.give_player(give)

    # Assert
    assert output == mockCoins
    mocked_giving.assert_called_once_with(test, give)
  
  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  def test_Bank_functions_take_payment(self, mocked_receiving, mocked_giving):
    # Arrange
    mockCoins = random_coins()
    mocked_giving.return_value = mockCoins
    mock_payment = random_coins()
    mock_pay_value = sum(coin.value for coin in mock_payment)
    mocked_receiving.return_value = mock_pay_value
    receive = random.randint(0,99)
    test = Bank()

    # Act
    output = test.take_payment(mock_payment, receive)

    # Assert
    assert output == mockCoins
    mocked_receiving.assert_called_once_with(test, mock_payment)
    mocked_giving.assert_called_once_with(test, mock_pay_value-receive)

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  @patch("coins.bank.time")
  def test_Bank_functions_check_need_nothing(self, mocked_time, mocked_receiving, mocked_giving, capsys):
    # Arrange
    mocked_time.sleep = lambda x: None
    mockCoin = One()
    mocked_receiving.return_value = 1
    mocked_giving.return_value = [mockCoin]
    test = Bank()
    mock_player = create_autospec(Player)
    mock_game = create_autospec(Game)
    mock_game.players = [mock_player]

    # Act
    test.check(mock_game)

    # Assert
    assert len(mock_game.players) == 1
    assert len(test.coins.coppers) > 5
    assert len(test.coins.silvers) > 2
    assert not mock_player.give_all.called
    assert not mock_player.receive.called

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 0

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  @patch("coins.bank.time")
  def test_Bank_functions_check_need_Ones(self, mocked_time, mocked_receiving, mocked_giving, capsys):
    # Arrange
    mocked_time.sleep = lambda x: None
    mockCoin = One()
    mocked_receiving.return_value = 1
    mocked_giving.return_value = [mockCoin]
    test = Bank()
    mock_player = create_autospec(Player)
    mock_player.coins = random_coins()
    mock_game = create_autospec(Game)
    mock_game.players = [mock_player]
    coppers = random.randint(0, 4)
    test.coins.coppers = [One() for _ in range(coppers)]

    # Act
    test.check(mock_game)

    # Assert
    assert len(mock_game.players) == 1
    assert len(test.coins.coppers) < 5
    assert len(test.coins.silvers) > 2
    mock_player.give_all.assert_called_once_with()
    mock_player.receive.assert_called_once_with(test.exchange(mock_player.coins))
    mock_player.receive.assert_called_once_with([mockCoin])

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"{reference['ansi_colours']['cyan']}The Bank has {coppers} copper One coin{'' if coppers == 1 else 's'} remaining - exchanging up with players...{reference['ansi_colours']['reset']}"

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  @patch("coins.bank.time")
  def test_Bank_functions_check_need_Fives(self, mocked_time, mocked_receiving, mocked_giving, capsys):
    # Arrange
    mocked_time.sleep = lambda x: None
    mockCoin = One()
    mocked_receiving.return_value = 1
    mocked_giving.return_value = [mockCoin]
    test = Bank()
    mock_player = create_autospec(Player)
    mock_player.coins = random_coins()
    mock_game = create_autospec(Game)
    mock_game.players = [mock_player]
    silvers = random.randint(0, 1)
    test.coins.silvers = [Five() for _ in range(silvers)]

    # Act
    test.check(mock_game)

    # Assert
    assert len(mock_game.players) == 1
    assert len(test.coins.coppers) > 5
    assert len(test.coins.silvers) < 2
    mock_player.give_all.assert_called_once_with()
    mock_player.receive.assert_called_once_with(test.exchange(mock_player.coins))
    mock_player.receive.assert_called_once_with([mockCoin])

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 1
    assert console_lines[0] == f"{reference['ansi_colours']['cyan']}The Bank has {silvers} silver Five coin{'' if silvers == 1 else 's'} remaining - exchanging up with players...{reference['ansi_colours']['reset']}"

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  def test_Bank_functions_exchange(self, mocked_receiving, mocked_giving):
    # Arrange
    swap_this = random_coins()
    for_that = random_coins()
    mocked_receiving.return_value = sum(coin.value for coin in swap_this)
    mocked_giving.return_value = for_that
    test = Bank()

    # Act
    output = test.exchange(swap_this)

    # Assert
    assert output == for_that
    mocked_receiving.assert_called_once_with(test, swap_this)
    mocked_giving.assert_called_once_with(test, sum(coin.value for coin in swap_this))

def random_coins() -> list[Coin]:
  ones = [One() for _ in range(random.randint(0,12))]
  fives = [Five() for _ in range(random.randint(0,12))]
  tens = [Ten() for _ in range(random.randint(0,12))]
  return ones + fives + tens