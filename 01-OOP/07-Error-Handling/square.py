# pylint: disable=missing-docstring
# pylint: disable=fixme
import sys

if __name__ == "__main__":
    try:
        print(int(sys.argv[1]) ** 2)
    except IndexError:
        print('No argument provided')
    except ValueError:
        print('Not a number')
