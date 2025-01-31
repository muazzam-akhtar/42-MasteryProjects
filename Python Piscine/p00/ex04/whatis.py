import sys


def main():
    _arg = sys.argv
    if len(_arg) == 1:
        return
    assert len(_arg) == 2, "more than one argument is provided"
    assert _arg[1].lstrip('-+').isdigit(), "argument is not an integer"
    number = int(_arg[1])
    if number % 2 == 0:
        print("I'm Even.")
    else:
        print("I'm Odd.")


if __name__ == "__main__":
    main()
