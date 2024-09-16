import unittest
from unittest.mock import patch, MagicMock
from google.cloud import firestore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.firestore_operations import FirestoreOperations
from backend.db.sql_operations import SQLOperations

class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        self.firestore_mock = patch('google.cloud.firestore.Client').start()
        self.sql_engine_mock = patch('sqlalchemy.create_engine').start()
        self.session_mock = MagicMock()
        self.sql_engine_mock.return_value.connect.return_value.__enter__.return_value = self.session_mock

    def tearDown(self):
        patch.stopall()

    def test_firestore_add_document(self):
        firestore_ops = FirestoreOperations()
        collection_mock = self.firestore_mock.return_value.collection.return_value
        collection_mock.add.return_value = MagicMock()

        result = firestore_ops.add_document('test_collection', {'key': 'value'})

        collection_mock.add.assert_called_once_with({'key': 'value'})
        self.assertIsNotNone(result)

    def test_firestore_get_document(self):
        firestore_ops = FirestoreOperations()
        doc_mock = self.firestore_mock.return_value.collection.return_value.document.return_value
        doc_mock.get.return_value.to_dict.return_value = {'key': 'value'}

        result = firestore_ops.get_document('test_collection', 'doc_id')

        self.assertEqual(result, {'key': 'value'})

    def test_sql_add_record(self):
        sql_ops = SQLOperations()
        
        sql_ops.add_record('test_table', {'column1': 'value1', 'column2': 'value2'})

        self.session_mock.execute.assert_called_once()
        self.session_mock.commit.assert_called_once()

    def test_sql_get_record(self):
        sql_ops = SQLOperations()
        self.session_mock.execute.return_value.fetchone.return_value = ('value1', 'value2')

        result = sql_ops.get_record('test_table', 'id', 1)

        self.session_mock.execute.assert_called_once()
        self.assertEqual(result, ('value1', 'value2'))

    # HUMAN ASSISTANCE NEEDED
    # Additional test cases should be added to cover more scenarios and edge cases.
    # Consider adding tests for update and delete operations, as well as error handling.