#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.auth.models import User, TokenBlacklist
from app.datasets.models import Dataset, Tag
from config import Config
from flask_jwt_extended import get_jti


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    '''Tests basic user functionalities.'''
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

    Note: For elasticsearch, refresh index before search to ensure all index
          changes have been pushed.
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
            4) Assert that 'dolphin' search returns the dataset just created.
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

        # -------------------------- Procedure 1 -----------------------------
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

        # 'name' now contains 'and' and 'soup'.
        # Search for either should yield the dataset.
        new.name = 'crackers and soup'
        db.session.commit()
        self.app.elasticsearch.indices.refresh(index='datasets')
        query, __ = Dataset.search('soup')
        self.assertEqual(len(query.all()), 1)

        # -------------------------- Procedure 2 -----------------------------
        # 'name' no longer contains 'crackers'. Search should return none.
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

    def test_dataset_basic_text_search(self):
        '''
        Tests that a database can do full-text search for datasets.

        Test 1: Basic exact-text search example works.
        Test 2: Datasets with matches in any field (name, description, citation)
                of the dataset
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
        Tests that our search functionality can successfully intepret
        english to an extent.

        Test 1: Uppercase and lowercase are ignore.
        Test 2: Search treats singular or plural forms the similarly.
        Test 3: Search ignores apostrophes ('s').
        Test 4: Search ignores tense.
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

        # Refresh index before search
        self.app.elasticsearch.indices.refresh(index='datasets')

        query, __ = Dataset.search('KaNgAroos')
        query2, __ = Dataset.search('jack')
        query3, __ = Dataset.search('rabbits')
        query4, __ = Dataset.search("Eric's")
        query5, __ = Dataset.search('jumped')
        query6, __ = Dataset.search('babies')

        # Test letter cases
        self.assertEqual(query.first().id, 1)

        # Test plural and singular forms
        self.assertEqual(query2.first().id, 3)
        self.assertEqual(query3.first().id, 2)

        # Test 's
        self.assertEqual(query4.first().id, 2)

        # Test tense
        self.assertEqual(len(query5.all()), 2)
        self.assertEqual(query6.first().id, 2)


class LoginLogoutCase(unittest.TestCase):
    '''
    Tests that the reigster, login, and logout routes work and
    correctly handle token blacklisting.
    '''
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Make a client to send requests to routes
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_login_logout(self):
        with self.client as c:
            # -------------------------- Register -----------------------------------------
            # Using keyword 'json' sets content-type to 'application/json'
            register_resp = c.post('/users/register', json=dict(
                username = 'cove',
                password = 'test',
                email = 'cove@thecvf.com'
            ))
            self.assertEqual(register_resp.status_code, 200)

            # Check that we have successfully registered
            json_data = register_resp.get_json()
            register_access_token = json_data.get('access_token')
            self.assertNotEqual(register_access_token, None)
            self.assertNotEqual(json_data.get('user_id'), None)
            self.assertNotEqual(json_data.get('permissions').get('is_admin'), None)

            # Assert that access token is not blacklisted
            t1 = TokenBlacklist.query.filter_by(jti=get_jti(register_access_token)).first()
            self.assertFalse(t1.revoked)

            # -------------------------- Login ---------------------------------------------
            # Try to log in with the newly registered user
            login_resp = c.post('/users/login', json=dict(
                username = 'cove',
                password = 'test',
            ))
            self.assertEqual(login_resp.status_code, 200)

            # Check that we have successfully logged in
            json_data = login_resp.get_json()
            login_access_token = json_data.get('access_token')
            login_user_id = json_data.get('user_id')
            self.assertNotEqual(login_access_token, None)
            self.assertNotEqual(login_user_id, None)

            # Assert that access token is not blacklisted
            t2 = TokenBlacklist.query.filter_by(jti=get_jti(login_access_token)).first()
            self.assertFalse(t2.revoked)

            # -------------------------- Logout --------------------------------------------
            # Log out of session from register. Register token should now be blacklisted
            c.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + register_access_token
            logout_resp = c.post('/users/logout')
            self.assertEqual(logout_resp.status_code, 200)
            t1 = TokenBlacklist.query.filter_by(jti=get_jti(register_access_token)).first()
            self.assertTrue(t1.revoked)

            # Log out of session from login. Login token should now be blacklisted
            c.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + login_access_token
            logout_resp = c.post('/users/logout')
            self.assertEqual(logout_resp.status_code, 200)
            t2 = TokenBlacklist.query.filter_by(jti=get_jti(login_access_token)).first()
            self.assertTrue(t2.revoked)


class TokenBlacklistCase(unittest.TestCase):
    '''Test that blacklisted tokens can't access protected endpoints.'''
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Make client to send requests to routes
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_blacklist_token_vs_protected_endpoint(self):
        with self.client as c:
            # Register a user to get an access token
            access_token = c.post('/users/register', json=dict(
                username = 'cove',
                password = 'test',
                email = 'cove@thecvf.com'
            )).get_json().get('access_token')

            # Invalidate the token by logging out
            c.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
            c.post('/users/logout')

            # Assert that trying to access protected endpoints return status
            # code of 401
            self.assertEqual(c.get('/users/me').status_code, 401)
            self.assertEqual(c.post('/users/logout').status_code, 401)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
