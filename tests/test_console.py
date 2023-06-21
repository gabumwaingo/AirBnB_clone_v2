#!/usr/bin/python3
""" test for the console """

import unittest
from unittest.mock import patch
from console import HBNBCommand

class ConsoleTestCase(unittest.TestCase):
    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        self.console = None

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_do_create_with_parameters(self, mock_stdout):
        self.console.onecmd("create BaseModel name=\"My_little_house\" value=10.5 quantity=5")
        output = mock_stdout.getvalue().strip()

        # Assert the expected output
        self.assertTrue(output.startswith("b"))
        self.assertIn("name: My little house", output)
        self.assertIn("value: 10.5", output)
        self.assertIn("quantity: 5", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_do_create_missing_class_name(self, mock_stdout):
        self.console.onecmd("create")
        output = mock_stdout.getvalue().strip()

        # Assert the expected output
        self.assertEqual(output, "** class name missing **")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_do_create_nonexistent_class(self, mock_stdout):
        self.console.onecmd("create NonExistentClass name=\"My_little_house\" value=10.5 quantity=5")
        output = mock_stdout.getvalue().strip()

        # Assert the expected output
        self.assertEqual(output, "** class doesn't exist **")

if __name__ == '__main__':
    unittest.main()
