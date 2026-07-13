"""Run Sage-compatible Python read from standard input."""

import sys
from sage_run import sage_run

def main() -> None:
    input_code = sys.stdin.read()
    print(sage_run(input_code))

if __name__ == "__main__":
    main()
