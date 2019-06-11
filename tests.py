#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.auth.models import User
from app.auth.schemas import user_schema
from app.datasets.models import Dataset, Tag
from app.datasets.schemas import dataset_schema
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        '''Tests that the user's password can be hashed verified.'''
        username = 'eric4jiang'
        password = 'dolphin'
        wrong_password = 'sharks'
        user = user_schema.load({
            'username': username,
            'password_hash': User.hash_password(password),
        }).data
        self.assertTrue(user.verify_password(password))
        self.assertFalse(user.verify_password(wrong_password))


class DatasetModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dataset_text_search(self):
        '''
        Tests that a database can do full-text search for datasets.

        Test 1: Basic search example works.
        Test 2: Datasets with a match in any field (name, description, citation) are returned.
        Test 3: Datasets with matches in the 'name' field have higher relevance.
        '''
        pass

    def test_dataset_indexed_after_commit():
        '''
        Tests that a dataset is properly indexed after it is commited to the dbself.

        Test 1:
            1) Start with an empty database.
            2) Assert that a search for 'dolphin' returns nothing.
            3) Create a new dataset with name='dolphin' and commit to db.
            4) Assert that a search for 'dolphin' returns the dataset just created.

        Test 2:
            1) Start with the database from the Test 1 (just one dataset).
            2) Assert that a search for 'whale' returns nothing.
            3) Create 2 datasets with name='whale 1' and name='whale 2' and commit.
            4) Assert that a search for 'whale' returns both these datasets.
        '''
        pass


if __name__ == '__main__':
    unittest.main()
