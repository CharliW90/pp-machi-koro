import pytest
from unittest.mock import patch, Mock, create_autospec, call
import random
from reference import reference
from player import Player, reset as reset_player_names
from game import Game

from coins.coinage import One, Five, Ten, CoinPiles, Coin
from coins.bank import Bank
from coins.transactions import giving, receiving, calculate_payment

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

  def test_coinage_mathematical_operations(self):
    # Arrange
    test_coin_A = One()
    test_coin_B = Five()
    test_coin_C = Ten()

    # Act / Assert
    assert test_coin_A + test_coin_B == 6
    assert test_coin_A + 123 == 124
    assert test_coin_B + test_coin_C == 15
    assert test_coin_B + 7 == 12
    assert test_coin_C + test_coin_A == 11
    assert test_coin_C + 73 == 83

    assert test_coin_C - test_coin_A == 9
    assert test_coin_C - 7 == 3
    assert test_coin_B - test_coin_C == -5
    assert test_coin_B - 2 == 3
    assert test_coin_A - test_coin_B == -4
    assert test_coin_A - 0 == 1

    assert test_coin_B * test_coin_C == 50
    assert test_coin_B * 17 == 85
    assert test_coin_C * test_coin_A == 10
    assert test_coin_C * 4 == 40
    assert test_coin_A * test_coin_B == 5
    assert test_coin_A * 11 == 11

    assert test_coin_C / test_coin_B == 2
    assert test_coin_C / 2 == 5
    assert test_coin_B / test_coin_A == 5
    assert test_coin_B / 5 == 1
    assert test_coin_A / 0 == 0

    assert test_coin_C // 3 == 3
    assert test_coin_B // 2 == 2
    assert test_coin_A // 0 == 0
  
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

  @patch("coins.bank.giving", wraps=giving)
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
    mocked_giving.assert_called_once_with(test, give, False)
  
  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
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
    mocked_receiving.assert_called_once_with(test, mock_payment, False)
    mocked_giving.assert_called_once_with(test, mock_pay_value-receive, False)

  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
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

  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
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

  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
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

  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
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
    mocked_receiving.assert_called_once_with(test, swap_this, False)
    mocked_giving.assert_called_once_with(test, sum(coin.value for coin in swap_this), False)

  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
  def test_Bank_functions_handle_transfer_balance_gt_payment(self, mocked_receiving, mocked_giving, capsys):
    reset_player_names()
    # Arrange
    test_payor: Player = Player("payor", 0)
    test_payee: Player = Player("payee", 1)
    test_bank: Bank = Bank()
    payment_amount: int = 8
    payor_balance: int = 10
    payee_balance: int = 3

    test_payor.receive(test_bank.give_player(payor_balance, True), True)
    test_payor.initialised = True
    test_payee.receive(test_bank.give_player(payee_balance, True), True)
    test_payee.initialised = True

    # Act
    test_bank.handle_transfer(test_payor, payment_amount, test_payee)

    # Assert
    assert payor_balance > payment_amount
    assert test_payor.coins.total() == payor_balance - payment_amount
    assert test_payee.coins.total() == payee_balance + payment_amount
    assert test_bank.total == 282
    assert mocked_receiving.call_count == 2
    assert mocked_giving.call_count == 4
    # assert player_receiving.call_count == 2

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 2
    assert console_lines[0] == f"{reference['ansi_colours']['red']}{test_payor.name} is giving {payment_amount} coins ==>{reference['ansi_colours']['reset']}"
    assert console_lines[1] == f"{reference['ansi_colours']['green']}==> {test_payee.name} received {payment_amount} coins{reference['ansi_colours']['reset']}"

  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
  def test_Bank_functions_handle_transfer_balance_lt_payment(self, mocked_receiving, mocked_giving, capsys):
    reset_player_names()
    # Arrange
    test_payor: Player = Player("payor", 0)
    test_payee: Player = Player("payee", 1)
    test_bank: Bank = Bank()
    payment_amount: int = 8
    payor_balance: int = 3
    payee_balance: int = 3

    test_payor.receive(test_bank.give_player(payor_balance, True), True)
    test_payor.initialised = True
    test_payee.receive(test_bank.give_player(payee_balance, True), True)
    test_payee.initialised = True

    # Act
    test_bank.handle_transfer(test_payor, payment_amount, test_payee)

    # Assert
    assert payor_balance < payment_amount
    assert test_payor.coins.total() == 0
    assert test_payee.coins.total() == payee_balance + payor_balance
    assert test_bank.total == 282
    assert mocked_receiving.call_count == 2
    assert mocked_giving.call_count == 4

    console = capsys.readouterr()
    console_lines = console.out.splitlines()
    assert len(console_lines) == 2
    assert console_lines[0] == f"{reference['ansi_colours']['red']}{test_payor.name} is giving all {payor_balance} of their coins ==>{reference['ansi_colours']['reset']}"
    assert console_lines[1] == f"{reference['ansi_colours']['green']}==> {test_payee.name} received {payor_balance} coins{reference['ansi_colours']['reset']}"

  @patch("coins.bank.giving", wraps=giving)
  @patch("coins.bank.receiving", wraps=receiving)
  def test_Bank_functions_handle_transfer_balance_error_handling(self, mocked_receiving, mocked_giving, capsys):
    reset_player_names()

    # Arrange
    test_payor: Player = Player("payor", 0)
    test_payee: Player = Player("payee", 1)
    test_bank: Bank = Bank()
    payment_amount: int = 3
    payor_balance: int = 3
    payee_balance: int = 3
    secret_payment_amount: int = 5

    test_payor.receive(test_bank.give_player(payor_balance, True), True)
    test_payor.initialised = True
    test_payee.receive(test_bank.give_player(payee_balance, True), True)
    test_payee.initialised = True

    assert test_payor.get_balance() == payor_balance
    assert test_payee.get_balance() == payee_balance

      # Act
    with patch.object(Player, "receive", autospec=True) as player_receive:
      def secret_payment(player, coins, silent):
        receiving(player, coins, silent)
        if player.name == "payor":
          for _ in range(secret_payment_amount): player.coins.coppers.append(One())
      
      player_receive.side_effect = secret_payment

      with pytest.raises(ArithmeticError) as error:
        test_bank.handle_transfer(test_payor, payment_amount, test_payee)

      assert error.value.args[0] == f"Payment calculation incorrect:\npayor_balance={payor_balance}, payee_balance={payee_balance}: {payor_balance + payee_balance}\nnew_payor_balance={secret_payment_amount}, new_payee_balance={payor_balance + payment_amount}: {secret_payment_amount + payor_balance +  payee_balance}\nbank_balance=282, new_bank_balance=282"

def random_coins() -> list[Coin]:
  ones = [One() for _ in range(random.randint(0,12))]
  fives = [Five() for _ in range(random.randint(0,12))]
  tens = [Ten() for _ in range(random.randint(0,12))]
  return ones + fives + tens

class TestTransactions:
  @pytest.mark.xfail(reason = "ToDo: transactions tests")
  def test_transactions_giving(self):
    assert False

  @pytest.mark.xfail(reason = "ToDo: transactions tests")
  def test_transactions_receiving(self):
    assert False

  @pytest.mark.xfail(reason = "ToDo: transactions tests")
  def test_transactions_calculate_payment(self):
    assert False