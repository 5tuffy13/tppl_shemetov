# Postfix Notation Stack Machine

A simple stack machine that evaluates arithmetic expressions written in postfix (Reverse Polish) notation.

## Operations
- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division
- `~` : Special operator:
  - If both operands are non-zero: computes `|x - y|`.
  - If at least one operand is 0: computes the sum of all values in the stack (including popped operands), squares the sum, and pushes it back onto the stack.

## Running via make

Makefile sets up a local virtual environment and installs testing dependencies:

```bash
# Run default example:
make run

# Run custom expression:
make run ARGS="2 2 + 4 - 4 ~ 2 3 * +"

# Run tests with 100% coverage report:
make test
```

## Running directly with Python

```bash
python main.py "3 0 4 ~ 2 ~"
```

Example output:
```text
Step 1 (3): [3]
Step 2 (0): [3, 0]
Step 3 (4): [3, 0, 4]
Step 4 (~): [49]
Step 5 (2): [49, 2]
Step 6 (~): [47]

3 0 4 ~ 2 ~ = 47
```
