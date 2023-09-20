#!/usr/bin/python3
"""Unittest for db storage"""
import unittest
from models.state import State
from models.user import User
from models.place import Place
from models import DBStorage

class TestDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the DBStorage instance for testing
        cls.db_storage = DBStorage()
        cls.db_storage.reload()

    def setUp(self):
        # Create a new session for each test
        self.db_storage.new(State(name="TestState"))
        self.db_storage.save()
        self.session = self.db_storage._DBStorage__session

    def tearDown(self):
        # Clean up after each test by removing the test data
        self.session.query(State).filter(State.name == "TestState").delete()
        self.db_storage.save()

    @classmethod
    def tearDownClass(cls):
        # Close the session and clean up
        cls.db_storage._DBStorage__session.remove()
        cls.db_storage = None

    def test_all(self):
        # Test the 'all' method with a specific class (State)
        result = self.db_storage.all(State)
        self.assertTrue(isinstance(result, dict))
        self.assertIn("State.TestState", result)

    def test_new(self):
        # Test the 'new' method by adding a new State object
        new_state = State(name="NewState")
        self.db_storage.new(new_state)
        self.assertIn(new_state, self.session)

    def test_save(self):
        # Test the 'save' method by adding a new State object and checking if it's saved
        new_state = State(name="NewState")
        self.db_storage.new(new_state)
        self.db_storage.save()
        self.assertTrue(self.session.query(State).filter(State.name == "NewState").first() is not None)

    def test_delete(self):
        # Test the 'delete' method by deleting a State object
        state_to_delete = self.session.query(State).filter(State.name == "TestState").first()
        self.db_storage.delete(state_to_delete)
        self.assertIsNone(self.session.query(State).filter(State.name == "TestState").first())

if __name__ == "__main__":
    unittest.main()
