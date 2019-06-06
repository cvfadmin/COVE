#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.auth.models import User
from app.auth.schemas import user_schema
from app.datasets.models import Dataset, Tag
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
        pass


if __name__ == '__main__':
    unittest.main()
