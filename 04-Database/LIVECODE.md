# Database - Livecode

Today, our livecode is not about database. It's about **Algorithmic**!
Let's practise with the "colorful number" problem using **TDD**.


For a given number N find if it's a COLORFUL number or not :

A number can be broken into different contiguous sub-subsequence parts.
Suppose, a number 3245 can be broken into parts like 3 2 4 5 32 24 45 324 245.
This number is a COLORFUL number, since product of every digit of a contiguous subsequence is different.

```
Example:

N = 23
2 3 23
2 -> 2
3 -> 3
23 -> 6
```
23 is a COLORFUL number since product of every digit of a sub-sequence are different.


## Setup

```bash
mkdir -p colorful && cd $_
pipenv --python 3.8
pipenv install nose
mkdir tests
touch colorful.py
touch tests/test_colorful.py

# We now can run:
pipenv run nosetests # => 0 tests for now
```

Bootstrap the testing class:

```python
# tests/test_colorful.py
import unittest

class ColorfulTest(unittest.TestCase):
    pass
```

## Solution

Please do not peek _before_ the livecode session!

<details><summary markdown="span">View solution
</summary>

```python
# test/test_colorful.py
from colorful import is_colorful
import unittest


class ColorfulTest(unittest.TestCase):
    def test_single_number(self):
        for i in range(10):
            self.assertTrue(is_colorful(i))

    def test_with_one_or_zero(self):
        self.assertFalse(is_colorful(1234))
        self.assertFalse(is_colorful(2304))

    def test_with_duplicate_numbers(self):
        self.assertFalse(is_colorful(32453))
        self.assertFalse(is_colorful(23456))

    def test_colorful_number(self):
        self.assertTrue(is_colorful(3245))

```

```python
# colorful.py
from typing import List


def is_colorful(number):
    number_as_string = str(number)
    if len(number_as_string) == 1:
        return True

    if "0" in number_as_string or "1" in number_as_string:
        return False

    number_list = [int(number) for number in number_as_string]

    if len(set(number_list)) != len(number_list):
        return False

    for width in range(2, len(number_as_string) - 1):
        for i in range(len(number_as_string) - width):
            slice = number_as_string[i : i + width]
            result = 1
            for digit in slice:
                result *= int(digit)

            if result in number_list:
                return False

            number_list.append(result)

    return True

```

</details>
