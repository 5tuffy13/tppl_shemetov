import pytest
from main import StackMachine, main


def test_basic_arithmetic():
    sm = StackMachine(verbose=False)
    assert sm.evaluate("5 3 +") == 8
    assert sm.evaluate("10 4 -") == 6
    assert sm.evaluate("3 7 -") == -4
    assert sm.evaluate("6 7 *") == 42
    assert sm.evaluate("15 3 /") == 5
    assert sm.evaluate("7 2 /") == 3.5


def test_tilde_operator_non_zero():
    sm = StackMachine(verbose=False)
    assert sm.evaluate("10 4 ~") == 6
    assert sm.evaluate("4 10 ~") == 6
    assert sm.evaluate("5 5 ~") == 0


def test_tilde_operator_with_zero():
    sm = StackMachine(verbose=False)
    assert sm.evaluate("5 0 ~") == 25
    assert sm.evaluate("0 5 ~") == 25
    assert sm.evaluate("0 0 ~") == 0
    assert sm.evaluate("3 0 4 ~") == 49


def test_examples_from_spec():
    sm = StackMachine(verbose=False)
    assert sm.evaluate("3 0 4 ~ 2 ~") == 47
    assert sm.evaluate("2 2 + 4 - 4 ~ 2 3 * +") == 22


def test_floats_and_negative_numbers():
    sm = StackMachine(verbose=False)
    assert sm.evaluate("-5 3 +") == -2
    assert sm.evaluate("1.5 2.5 +") == 4
    assert sm.evaluate("2.5 1.2 +") == 3.7


def test_empty_expression():
    sm = StackMachine(verbose=False)
    with pytest.raises(ValueError, match="Expression is empty"):
        sm.evaluate("")
    with pytest.raises(ValueError, match="Expression is empty"):
        sm.evaluate("   ")


def test_not_enough_operands():
    sm = StackMachine(verbose=False)
    with pytest.raises(ValueError, match="requires at least two operands"):
        sm.evaluate("+")
    with pytest.raises(ValueError, match="requires at least two operands"):
        sm.evaluate("5 +")


def test_division_by_zero():
    sm = StackMachine(verbose=False)
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        sm.evaluate("10 0 /")


def test_unknown_token():
    sm = StackMachine(verbose=False)
    with pytest.raises(ValueError, match="Unknown symbol"):
        sm.evaluate("2 3 &")


def test_incomplete_expression():
    sm = StackMachine(verbose=False)
    with pytest.raises(ValueError, match="More than one number left in stack"):
        sm.evaluate("1 2 3 +")


def test_verbose_logging(capsys):
    sm = StackMachine(verbose=True)
    res = sm.evaluate("2 3 +")
    assert res == 5
    captured = capsys.readouterr()
    assert "Step 1 (2): [2]" in captured.out
    assert "Step 3 (+): [5]" in captured.out


def test_cli_success(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py", "3 0 4 ~ 2 ~"])
    main()
    captured = capsys.readouterr()
    assert "3 0 4 ~ 2 ~ = 47" in captured.out


def test_cli_no_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Tip: pass an expression in quotes" in captured.out


def test_cli_error(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py", "5 0 /"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Cannot divide by zero" in captured.out


def test_module_entrypoint(monkeypatch):
    import runpy
    monkeypatch.setattr("sys.argv", ["main.py", "2 3 +"])
    runpy.run_module("main", run_name="__main__")
