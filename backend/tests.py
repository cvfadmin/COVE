#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.auth.models import User
from app.datasets.models import Dataset, Tag
from config import Config
from flask import current_app


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
        username = 'cove'
        password = 'dolphin'
        wrong_password = 'sharks'
        user = User(
            username = username,
            password_hash = User.hash_password(password),
        )
        self.assertTrue(user.verify_password(password))
        self.assertFalse(user.verify_password(wrong_password))


class DatasetModelCase(unittest.TestCase):
    '''
    Tests dataset manipulation and searching functionality.

    Note: For elasticsearch, refresh index before search to ensure all index changes
          have been pushed.
    '''

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_new_dataset_is_searchable(self):
        '''
        Tests that a newly added dataset is properly indexed and searchable.

        Procedure:
            1) Start with an empty database.
            2) Assert that a search for 'dolphin' returns nothing.
            3) Create a new dataset with name='dolphin' and commit to db.
            4) Assert that a search for 'dolphin' returns the dataset just created.
        '''
        query, ___ = Dataset.search('dolphin')
        self.assertEqual(len(query.all()), 0)

        # Initialize an owner for the dataset
        user = User(
            username = 'cove',
            password_hash = User.hash_password('test')
        )
        db.session.add(user)
        db.session.commit()

        # Create dataset and add it
        new = Dataset(
            citation = '',
            description = '',
            name = 'dolphin',
            url = 'https://github.com/cvfadmin/COVE',
            owner_id = 1
        )
        db.session.add(new)
        db.session.commit()

        self.app.elasticsearch.indices.refresh(index='datasets')
        query, ___ = Dataset.search('dolphin')
        self.assertEqual(len(query.all()),  1)

    def test_updated_dataset_is_searchable(self):
        '''
        Tests that an updated dataset is properly indexed and searchable.

        Procedure 1: New additions can be searched for.
            1) Create and add a dataset with name='crackers' to the db.
            2) Assert that a search for 'soup' returns nothing.
            3) Update the name of the dataset to name='crackers and soup'.
            4) Assert that a search for 'soup' returns the dataset.

        Procedure 2: Deletions are no longer found when searched for.
            1) Use dataset from procedure 1.
            2) Update the name of the dataset to name='soup'
            3) Assert that a search for 'crackers' returns nothing.
        '''

        # -----------------------------Procedure 1--------------------------------
        # Initialize an owner for the dataset
        user = User(
            username = 'cove',
            password_hash = User.hash_password('test')
        )
        db.session.add(user)
        db.session.commit()

        # Create dataset and add it
        new = Dataset(
            citation = '',
            description = '',
            name = 'Crackers',
            url = 'https://github.com/cvfadmin/COVE',
            owner_id = 1
        )
        db.session.add(new)
        db.session.commit()

        # Assert 'soup' search returns nothing.
        self.app.elasticsearch.indices.refresh(index='datasets')
        query, __ = Dataset.search('soup')
        self.assertEqual(len(query.all()), 0)

        # 'name' now contains 'and' and 'soup'. A search for either should yield the dataset.
        new.name = 'crackers and soup'
        db.session.commit()
        self.app.elasticsearch.indices.refresh(index='datasets')
        query, __ = Dataset.search('soup')
        self.assertEqual(len(query.all()), 1)

        # -----------------------------Procedure 2--------------------------------
        # 'name' no longer contains 'crackers', so a search for it should return none.
        new.name = 'soup'
        db.session.commit()
        self.app.elasticsearch.indices.refresh(index='datasets')
        query, __ = Dataset.search('crackers')
        self.assertEqual(len(query.all()), 0)

    def test_deleted_dataset_is_not_searchable(self):
        '''
        Tests that a deleted dataset is no longer searchable.

        Procedure:
            1) Create and add a dataset name='racket'
            2) Assert that searching 'racket' returns the dataset.
            3) Delete the dataset.
            4) Assert that a search for 'racket' returns None.
        '''
        # Initialize an owner for the dataset
        user = User(
            username = 'cove',
            password_hash = User.hash_password('test')
        )
        db.session.add(user)
        db.session.commit()

        # Create dataset and add it
        new = Dataset(
            citation = '',
            description = '',
            name = 'racket',
            url = 'https://github.com/cvfadmin/COVE',
            owner_id = 1
        )
        db.session.add(new)
        db.session.commit()

        # Assert 'racket' search returns dataset.
        self.app.elasticsearch.indices.refresh(index='datasets')
        query, __ = Dataset.search('racket')
        self.assertEqual(len(query.all()), 1)

        db.session.delete(new)
        db.session.commit()

        # Assert 'racket' search returns dataset.
        self.app.elasticsearch.indices.refresh(index='datasets')
        query, __ = Dataset.search('racket')
        self.assertEqual(len(query.all()), 0)

    def test_dataset_text_search(self):
        '''
        Tests that a database can do full-text search for datasets.

        Test 1: Basic exact-text search example works.
        Test 2: Datasets with a match in any field (name, description, citation) are returned.
        Test 3: Datasets with matches in the 'name' field have higher relevance.
        '''
        # Initialize an owner for the dataset
        user = User(
            username = 'cove',
            password_hash = User.hash_password('test')
        )
        db.session.add(user)
        db.session.commit()

        # Create 3 datasets and commit them
        d1 = Dataset(
            id = 1,
            citation = 'Australia',
            description = 'Pictures of adult kangaroos in their habitat.',
            name = 'Video of Jumping Kangaroos',
            url = 'https://github.com/cvfadmin/COVE',
            owner_id = 1
        )
        d2 = Dataset(
            id = 2,
            citation = 'Eric Jiang',
            description = 'Video of a baby rabbit playing around the house.',
            name = 'A white rabbit hops onto the table.',
            url = 'https://github.com/cvfadmin/COVE',
            owner_id = 1
        )
        d3 = Dataset(
            id = 3,
            citation = 'A gym',
            description = 'An ad about why jumping jacks are healthy',
            name = 'Jumping jacks is your friend.',
            url = 'https://github.com/cvfadmin/COVE',
            owner_id = 1
        )
        db.session.add_all([d1, d2, d3])
        db.session.commit()

        # Some basic searching
        self.app.elasticsearch.indices.refresh(index='datasets')
        query, __ = Dataset.search('jacks')
        query2, __ = Dataset.search('A white rabbit hops onto the table')
        query3, __ = Dataset.search('Jumping')
        self.assertEqual(query.first().id, 3)
        self.assertEqual(query2.first().id, 2)
        self.assertEqual(len(query3.all()), 2)

        # Search different fields
        query4, __ = Dataset.search('habitat') # description field
        query5, __ = Dataset.search('Eric Jiang') # citation field
        self.assertEqual(query4.first().id, 1)
        self.assertEqual(query5.first().id, 2)

        # Matches in name have higher priority
        query6, __ = Dataset.search('Video')
        self.assertEqual(len(query6.all()), 2)
        self.assertEqual(query6.all()[0].id, 1)
        self.assertEqual(query6.all()[1].id, 2)

    def test_dataset_text_search_english_analyzer(self):
        '''
        Tests that our search functionality can successfully intepret english to an extent.

        Test 1: Search treats singular or plural forms the similarly.
        Test 2: Search ignores apostrophes ('s').
        Test 3: Search ignores tense.
        '''
        pass

class TokenBlacklistModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
