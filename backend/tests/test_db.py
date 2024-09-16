import unittest
from unittest.mock import patch, MagicMock
from google.cloud import firestore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.firestore_operations import FirestoreOperations
from backend.db.sql_operations import SQLOperations
from backend.models.user import User

class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        self.firestore_mock = patch('google.cloud.firestore.Client').start()
        self.sql_engine_mock = patch('sqlalchemy.create_engine').start()
        self.session_mock = MagicMock()
        self.sql_engine_mock.return_value.connect.return_value.__enter__.return_value = self.session_mock

    def tearDown(self):
        patch.stopall()

    def test_firestore_create_user(self):
        firestore_ops = FirestoreOperations()
        user_data = {"id": "123", "name": "John Doe", "email": "john@example.com"}
        
        firestore_ops.create_user(user_data)
        
        self.firestore_mock.return_value.collection.assert_called_once_with('users')
        self.firestore_mock.return_value.collection().document.assert_called_once_with('123')
        self.firestore_mock.return_value.collection().document().set.assert_called_once_with(user_data)

    def test_firestore_get_user(self):
        firestore_ops = FirestoreOperations()
        user_id = "123"
        mock_user_data = {"id": "123", "name": "John Doe", "email": "john@example.com"}
        
        self.firestore_mock.return_value.collection().document().get().to_dict.return_value = mock_user_data
        
        result = firestore_ops.get_user(user_id)
        
        self.assertEqual(result, mock_user_data)
        self.firestore_mock.return_value.collection.assert_called_once_with('users')
        self.firestore_mock.return_value.collection().document.assert_called_once_with(user_id)

    def test_sql_create_user(self):
        sql_ops = SQLOperations()
        user_data = {"id": "123", "name": "John Doe", "email": "john@example.com"}
        
        sql_ops.create_user(user_data)
        
        self.session_mock.add.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_sql_get_user(self):
        sql_ops = SQLOperations()
        user_id = "123"
        mock_user = User(id="123", name="John Doe", email="john@example.com")
        
        self.session_mock.query().filter().first.return_value = mock_user
        
        result = sql_ops.get_user(user_id)
        
        self.assertEqual(result.id, mock_user.id)
        self.assertEqual(result.name, mock_user.name)
        self.assertEqual(result.email, mock_user.email)
        self.session_mock.query.assert_called_once_with(User)
        self.session_mock.query().filter.assert_called_once()

    # HUMAN ASSISTANCE NEEDED
    # Additional test cases may be required for update, delete, and other CRUD operations
    # for both Firestore and SQL databases. Also, consider adding edge cases and error handling tests.

if __name__ == '__main__':
    unittest.main()