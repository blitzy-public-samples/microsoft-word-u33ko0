import unittest
from unittest.mock import Mock, patch
from services.document_service import DocumentService
from services.collaboration_service import CollaborationService
from services.export_service import ExportService
from models.document import Document
from models.user import User

class TestDocumentService(unittest.TestCase):
    def setUp(self):
        self.document_service = DocumentService()

    def test_create_document(self):
        user = User(id=1, username="testuser")
        document = self.document_service.create_document(user, "Test Document")
        self.assertIsInstance(document, Document)
        self.assertEqual(document.title, "Test Document")
        self.assertEqual(document.owner, user)

    def test_get_document(self):
        document_id = 1
        document = self.document_service.get_document(document_id)
        self.assertIsInstance(document, Document)
        self.assertEqual(document.id, document_id)

    def test_update_document(self):
        document_id = 1
        new_content = "Updated content"
        updated_document = self.document_service.update_document(document_id, new_content)
        self.assertEqual(updated_document.content, new_content)

    def test_delete_document(self):
        document_id = 1
        result = self.document_service.delete_document(document_id)
        self.assertTrue(result)

class TestCollaborationService(unittest.TestCase):
    def setUp(self):
        self.collaboration_service = CollaborationService()

    def test_add_collaborator(self):
        document_id = 1
        user_id = 2
        result = self.collaboration_service.add_collaborator(document_id, user_id)
        self.assertTrue(result)

    def test_remove_collaborator(self):
        document_id = 1
        user_id = 2
        result = self.collaboration_service.remove_collaborator(document_id, user_id)
        self.assertTrue(result)

    def test_get_collaborators(self):
        document_id = 1
        collaborators = self.collaboration_service.get_collaborators(document_id)
        self.assertIsInstance(collaborators, list)
        self.assertTrue(all(isinstance(user, User) for user in collaborators))

class TestExportService(unittest.TestCase):
    def setUp(self):
        self.export_service = ExportService()

    @patch('services.export_service.generate_pdf')
    def test_export_to_pdf(self, mock_generate_pdf):
        document_id = 1
        mock_generate_pdf.return_value = b'mock_pdf_content'
        pdf_content = self.export_service.export_to_pdf(document_id)
        self.assertEqual(pdf_content, b'mock_pdf_content')
        mock_generate_pdf.assert_called_once_with(document_id)

    @patch('services.export_service.generate_docx')
    def test_export_to_docx(self, mock_generate_docx):
        document_id = 1
        mock_generate_docx.return_value = b'mock_docx_content'
        docx_content = self.export_service.export_to_docx(document_id)
        self.assertEqual(docx_content, b'mock_docx_content')
        mock_generate_docx.assert_called_once_with(document_id)

if __name__ == '__main__':
    unittest.main()