# doc-toolkit

document toolkit

## Setup

1. install Python 3.10
2. install Poetry
3. in git root folder
   1. python -m venv .venv
   2. poetry shell
   3. poetry install

## IDE

1. vscode
   1. Cmd-Shift-P type Show Recommended Extension. Install them
   2. open a terminal and type pre-commit install

## Samples

Refer to [README.md](./samples/README.md)

## Test cases

1. Test cases are available at [`tests/`](./tests/)
2. Click on Ctrl+shift+p for windows and search for Python: Discover tests
3. Select path to discover as tests
4. Tests can be debugged using test explorer on the left pane.

## Test Coverage

```sh
pytest --cov-report term-missing --cov=. tests
```
