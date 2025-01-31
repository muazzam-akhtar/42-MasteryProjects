from ft_filter import ft_filter
import argparse
import sys


def is_valid_str(s) -> bool:
    return all(c.isalpha() or c.isspace() for c in s)


def main():
    parser = argparse.ArgumentParser(prog='ProgramName')
    parser.add_argument('string', help='An optional argument')
    parser.add_argument('integer', help='An optional argument')

    _list = sys.argv
    assert len(_list) == 3, "the arguments are bad"
    args = parser.parse_args()
    assert is_valid_str(args.string) is True, "the arguments are bad"
    assert args.integer.isdigit() is True, "the arguments are bad"
    res = ft_filter(args.string, args.integer)
    print(res)


if __name__ == '__main__':
    main()
