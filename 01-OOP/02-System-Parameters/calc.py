# pylint: disable=missing-docstring


def main():
    # We need to import argv inside the main() body to make our tests pass
    # Importing in the main function will force Python to reload argv between each tests
    from sys import argv
    import operator

    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    return ops[argv[2]](int(argv[1]), int(argv[3]))


if __name__ == "__main__":
    print(main())
