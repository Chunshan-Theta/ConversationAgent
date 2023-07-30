import unittest

# The class to test
class Calculator:
    def add(self, a: int, b: int):
        return a + b

# The test class
class TestCalculator(unittest.TestCase):

    def test_add(self):
        calc = Calculator()
        result = calc.add(2, 3)
        self.assertEqual(result, 5)  # Assertion to check if the result is as expected

# Run the tests
if __name__ == '__main__':
    unittest.main()
