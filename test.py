"""
Test  main.py
"""
import unittest
import transform


class TestStringMethods(unittest.TestCase):
    """Test main.py"""

    def test_is_upper(self):
        """Test main.py"""
        sting = transform.to_upper_case("hello")
        self.assertEqual(sting, "HELLO")

    def test_is_lower(self):
        """Test main.py"""
        sting = transform.to_lower_case("HELLO")
        self.assertEqual(sting, "hello")

    def test_is_capitalize(self):
        """Test main.py"""
        sting = transform.to_capitalize("HELLO")
        self.assertEqual(sting, "Hello")


if __name__ == '__main__':
    unittest.main()
