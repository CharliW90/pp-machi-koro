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
  
  def test_CoinPiles_x100(self):
    for _ in range(100):
      # Arrange
      quantities = randomQuantities()
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

def randomQuantities() -> list:
  lowNumber = random.randint(0, 3)
  highNumber = random.randint(36, 48)
  anyNumber = random.randint(3, 36)

  quantities = [lowNumber, highNumber, anyNumber]
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
    assert test.colorize == reference['ansiColours']['cyan']
    assert hasattr(test, "reset")
    assert test.reset == reference['ansiColours']['reset']
    assert hasattr(test, "coins")
    assert isinstance(test.coins, CoinPiles)
    assert test.coins.total() == 282
    assert hasattr(test, "total")
    assert test.total == 282
    assert hasattr(test, "declareAction")
    assert hasattr(test, "givePlayer")
    assert hasattr(test, "takePayment")
    assert hasattr(test, "check")
    assert hasattr(test, "exchange")

    assert str(test) == "The Bank contains 282 in coinage:\n42 Copper 'Ones', valuing 42\n24 Silver 'Fives', valuing 120\n12 Gold 'Tens', valuing 120"
    
  def test_Bank_functionsDeclare(self, capsys):
    # Arrange
    expectedMessage = f"{reference['ansiColours']['cyan']}Hello World!{reference['ansiColours']['reset']}"
    test = Bank()

    # Act
    test.declareAction("Hello World!")

    # Assert
    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == expectedMessage

  @patch("coins.bank.giving")
  def test_Bank_functionsGivePlayer(self, mocked_giving):
    # Arrange
    mockCoins = randomCoins()
    mocked_giving.return_value = mockCoins
    give = sum(coin.value for coin in mockCoins)
    test = Bank()

    # Act
    output = test.givePlayer(give)

    # Assert
    assert output == mockCoins
    mocked_giving.assert_called_once_with(test, give)
  
  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  def test_Bank_functionsTakePayment(self, mocked_receiving, mocked_giving):
    # Arrange
    mockCoins = randomCoins()
    mocked_giving.return_value = mockCoins
    mockPayment = randomCoins()
    mockPayValue = sum(coin.value for coin in mockPayment)
    mocked_receiving.return_value = mockPayValue
    receive = random.randint(0,99)
    test = Bank()

    # Act
    output = test.takePayment(mockPayment, receive)

    # Assert
    assert output == mockCoins
    mocked_receiving.assert_called_once_with(test, mockPayment)
    mocked_giving.assert_called_once_with(test, mockPayValue-receive)

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  @patch("coins.bank.time")
  def test_Bank_functionsCheck_fullBalance(self, mocked_time, mocked_receiving, mocked_giving, capsys):
    # Arrange
    mocked_time.sleep = lambda x: None
    mockCoin = One()
    mocked_receiving.return_value = 1
    mocked_giving.return_value = [mockCoin]
    test = Bank()
    mockPlayer = create_autospec(Player)
    mockGame = create_autospec(Game)
    mockGame.players = [mockPlayer]

    # Act
    test.check(mockGame)

    # Assert
    assert len(mockGame.players) == 1
    assert len(test.coins.coppers) > 5
    assert len(test.coins.silvers) > 2
    assert not mockPlayer.giveAll.called
    assert not mockPlayer.receive.called

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 0

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  @patch("coins.bank.time")
  def test_Bank_functionsCheck_needOnes(self, mocked_time, mocked_receiving, mocked_giving, capsys):
    # Arrange
    mocked_time.sleep = lambda x: None
    mockCoin = One()
    mocked_receiving.return_value = 1
    mocked_giving.return_value = [mockCoin]
    test = Bank()
    mockPlayer = create_autospec(Player)
    mockPlayer.coins = randomCoins()
    mockGame = create_autospec(Game)
    mockGame.players = [mockPlayer]
    coppers = random.randint(0, 4)
    test.coins.coppers = [One() for _ in range(coppers)]

    # Act
    test.check(mockGame)

    # Assert
    assert len(mockGame.players) == 1
    assert len(test.coins.coppers) < 5
    assert len(test.coins.silvers) > 2
    mockPlayer.giveAll.assert_called_once_with()
    mockPlayer.receive.assert_called_once_with(test.exchange(mockPlayer.coins))
    mockPlayer.receive.assert_called_once_with([mockCoin])

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"{reference['ansiColours']['cyan']}The Bank has {coppers} copper One coin{'' if coppers == 1 else 's'} remaining - exchanging up with players...{reference['ansiColours']['reset']}"

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  @patch("coins.bank.time")
  def test_Bank_functionsCheck_needFives(self, mocked_time, mocked_receiving, mocked_giving, capsys):
    # Arrange
    mocked_time.sleep = lambda x: None
    mockCoin = One()
    mocked_receiving.return_value = 1
    mocked_giving.return_value = [mockCoin]
    test = Bank()
    mockPlayer = create_autospec(Player)
    mockPlayer.coins = randomCoins()
    mockGame = create_autospec(Game)
    mockGame.players = [mockPlayer]
    silvers = random.randint(0, 1)
    test.coins.silvers = [Five() for _ in range(silvers)]

    # Act
    test.check(mockGame)

    # Assert
    assert len(mockGame.players) == 1
    assert len(test.coins.coppers) > 5
    assert len(test.coins.silvers) < 2
    mockPlayer.giveAll.assert_called_once_with()
    mockPlayer.receive.assert_called_once_with(test.exchange(mockPlayer.coins))
    mockPlayer.receive.assert_called_once_with([mockCoin])

    console = capsys.readouterr()
    consoleLines = console.out.splitlines()
    assert len(consoleLines) == 1
    assert consoleLines[0] == f"{reference['ansiColours']['cyan']}The Bank has {silvers} silver Five coin{'' if silvers == 1 else 's'} remaining - exchanging up with players...{reference['ansiColours']['reset']}"

  @patch("coins.bank.giving")
  @patch("coins.bank.receiving")
  def test_Bank_functionsExchange(self, mocked_receiving, mocked_giving, capsys):
    # Arrange
    swapThis = randomCoins()
    forThat = randomCoins()
    mocked_receiving.return_value = sum(coin.value for coin in swapThis)
    mocked_giving.return_value = forThat
    test = Bank()

    # Act
    output = test.exchange(swapThis)

    # Assert
    assert output == forThat
    mocked_receiving.assert_called_once_with(test, swapThis)
    mocked_giving.assert_called_once_with(test, sum(coin.value for coin in swapThis))

def randomCoins() -> list[Coin]:
  ones = [One() for _ in range(random.randint(0,12))]
  fives = [Five() for _ in range(random.randint(0,12))]
  tens = [Ten() for _ in range(random.randint(0,12))]
  return ones + fives + tens