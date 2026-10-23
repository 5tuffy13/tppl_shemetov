import sys


class StackMachine:
    def __init__(self, verbose: bool = True):
        self.stack = []
        self.verbose = verbose

    def _format_value(self, val):
        if isinstance(val, float) and val.is_integer():
            return int(val)
        return val

    def log_step(self, step: int, token: str):
        if self.verbose:
            formatted_stack = [self._format_value(x) for x in self.stack]
            print(f"Step {step} ({token}): {formatted_stack}")

    def evaluate(self, expr: str):
        if not expr or not expr.strip():
            raise ValueError("Expression is empty. Please provide numbers and operators.")

        tokens = expr.strip().split()
        self.stack.clear()

        for step, token in enumerate(tokens, start=1):
            num = self._try_parse_number(token)
            if num is not None:
                self.stack.append(num)
                self.log_step(step, token)
                continue

            if token in ("+", "-", "*", "/", "~", "!"):
                if len(self.stack) < 2:
                    raise ValueError(
                        f"Operator '{token}' requires at least two operands, "
                        f"but current stack is: {self.stack}."
                    )

                b = self.stack.pop()
                a = self.stack.pop()

                if token == "+":
                    res = a + b
                    self.stack.append(self._format_value(res))
                elif token == "-":
                    res = a - b
                    self.stack.append(self._format_value(res))
                elif token == "*":
                    res = a * b
                    self.stack.append(self._format_value(res))
                elif token == "/":
                    if b == 0:
                        raise ZeroDivisionError(f"Cannot divide by zero ({a} / {b}).")
                    res = a / b
                    self.stack.append(self._format_value(res))
                elif token == "~":
                    if a != 0 and b != 0:
                        res = abs(a - b)
                        self.stack.append(self._format_value(res))
                    else:
                        total = sum(self.stack) + a + b
                        res = total ** 2
                        self.stack = [self._format_value(res)]
		elif token == "!":
			res = a ** b
			self.stack.append(self._format_value(res))

                self.log_step(step, token)
            else:
                raise ValueError(
                    f"Unknown symbol '{token}'. "
                    f"Only numbers and operators +, -, *, /, ~, ! are supported."
                )

        if len(self.stack) != 1:
            raise ValueError(
                f"More than one number left in stack: {self.stack}. "
                f"Please check your expression."
            )

        return self._format_value(self.stack[0])

    @staticmethod
    def _try_parse_number(token: str):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return None


def main():
    if len(sys.argv) < 2:
        print("Tip: pass an expression in quotes.")
        print("Example: python main.py \"3 0 4 ~ 2 ~\"")
        sys.exit(1)

    raw_expr = " ".join(sys.argv[1:])
    machine = StackMachine(verbose=True)

    try:
        result = machine.evaluate(raw_expr)
        print(f"\n{raw_expr} = {result}")
    except (ValueError, ZeroDivisionError) as err:
        print(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
