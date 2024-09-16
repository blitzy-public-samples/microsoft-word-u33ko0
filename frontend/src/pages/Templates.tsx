import React, { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { getTemplates } from '@/services/api';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

interface Template {
  id: string;
  name: string;
  description: string;
  thumbnail: string;
}

const Templates: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const currentUser = useAppSelector(selectCurrentUser);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const fetchedTemplates = await getTemplates();
        setTemplates(fetchedTemplates);
      } catch (error) {
        console.error('Error fetching templates:', error);
        // HUMAN ASSISTANCE NEEDED
        // TODO: Implement proper error handling and user feedback
      }
    };

    fetchTemplates();
  }, []);

  const handleTemplateSelection = (templateId: string) => {
    setSelectedTemplate(templateId);
    // HUMAN ASSISTANCE NEEDED
    // TODO: Implement navigation to template editing page or next step in the process
  };

  return (
    <div className="templates-page">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Document Templates</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template) => (
            <div
              key={template.id}
              className="template-card border rounded-lg p-4 cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => handleTemplateSelection(template.id)}
            >
              <img
                src={template.thumbnail}
                alt={template.name}
                className="w-full h-40 object-cover mb-4 rounded"
              />
              <h2 className="text-xl font-semibold mb-2">{template.name}</h2>
              <p className="text-gray-600">{template.description}</p>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Templates;