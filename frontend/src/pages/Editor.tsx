import React, { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { Toolbar } from '@/components/Toolbar';
import { DocumentCanvas } from '@/components/DocumentCanvas';
import { Sidebar } from '@/components/Sidebar';
import { getDocument, updateDocument } from '@/services/api';
import { useAppSelector, useAppDispatch } from '@/store';
import { setCurrentDocument } from '@/store/documentSlice';

// HUMAN ASSISTANCE NEEDED
// The following component needs review for production readiness and potential improvements

const Editor: React.FC = () => {
  const dispatch = useAppDispatch();
  const currentDocument = useAppSelector((state) => state.document.currentDocument);
  const [content, setContent] = useState('');

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        const documentData = await getDocument(currentDocument.id);
        setContent(documentData.content);
        dispatch(setCurrentDocument(documentData));
      } catch (error) {
        console.error('Error fetching document:', error);
        // TODO: Add proper error handling
      }
    };

    if (currentDocument?.id) {
      fetchDocument();
    }
  }, [currentDocument?.id, dispatch]);

  useEffect(() => {
    const autoSave = async () => {
      try {
        await updateDocument(currentDocument.id, { content });
      } catch (error) {
        console.error('Error auto-saving document:', error);
        // TODO: Add proper error handling and user notification
      }
    };

    const timer = setTimeout(autoSave, 5000);
    return () => clearTimeout(timer);
  }, [content, currentDocument?.id]);

  const handleContentChange = (newContent: string) => {
    setContent(newContent);
  };

  return (
    <div className="editor-page">
      <Header />
      <div className="editor-main">
        <Toolbar />
        <div className="editor-content">
          <DocumentCanvas content={content} onContentChange={handleContentChange} />
          <Sidebar />
        </div>
      </div>
    </div>
  );
};

export default Editor;