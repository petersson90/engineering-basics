# pylint: disable=missing-docstring


def main():
    # We need to import argv inside the main() body to make our tests pass
    # Importing in the main function will force Python to reload argv between each tests
    from sys import argv

    pass  # TODO: implement the calculator


if __name__ == "__main__":
    print(main())
