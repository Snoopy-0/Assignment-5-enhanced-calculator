
"""
Command-line REPL acting as a Facade to the calculator internals.
"""
from __future__ import annotations
import sys
from typing import List
from .calculator_config import Config
from .history import History
from .operations import operation_factory
from .calculation import Calculation
from .input_validators import parse_command, parse_operation_args
from .exceptions import CalculatorError, OperationError, ValidationError, UndoRedoError

HELP_TEXT = """\
Commands:
  +, -, *, /, ^, root <operands...>   perform operation
  history                              show history
  save [path]                          save history to CSV
  load <path>                          load history from CSV
  undo | redo                          undo/redo last history change
  clear                                clear history
  help                                 show this help
  exit                                 quit
"""

class CalculatorFacade:
    def __init__(self, config: Config):
        self.config = config
        self.history = History(csv_path=config.history_csv, autosave=config.autosave)

    def perform(self, operator: str, args: List[str]) -> float:
        operands = parse_operation_args(args)
        strategy = operation_factory(operator)
        calc = Calculation(operator=operator, operands=operands, strategy=strategy)
        result = calc.perform()
        self.history.add_record(operator, operands, result)
        return result

def main(argv=None):  # pragma: no cover - interactive shell
    cfg = Config.load()
    calc = CalculatorFacade(cfg)
    print("Enhanced Calculator. Type 'help' for commands.")
    while True:
        try:
            line = input("calc> ").strip()
            if not line:
                continue
            cmd, args = parse_command(line)
            if cmd in {"+", "-", "*", "/", "^", "root"}:
                res = calc.perform(cmd, args)
                print(res)
            elif cmd == "history":
                print(calc.history.df.to_string(index=False))
            elif cmd == "save":
                path = args[0] if args else None
                calc.history.save(path)
                print("Saved.")
            elif cmd == "load":
                if not args:
                    print("Usage: load <path>")
                    continue
                calc.history.load(args[0])
                print("Loaded.")
            elif cmd == "undo":
                calc.history.undo()
                print("Undone.")
            elif cmd == "redo":
                calc.history.redo()
                print("Redone.")
            elif cmd == "clear":
                calc.history.clear()
                print("Cleared.")
            elif cmd == "help":
                print(HELP_TEXT)
            elif cmd == "exit":
                print("Bye!")
                break
            else:
                print("Unknown command. Type 'help'.")
        except (OperationError, ValidationError, UndoRedoError, CalculatorError) as e:
            print(f"Error: {e}")
        except EOFError:
            print("\nBye!")
            break
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
            continue

if __name__ == "__main__":  # pragma: no cover - CLI entry
    main(sys.argv[1:])
