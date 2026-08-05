/** Render top navigation and the signed-in user summary.
 *
 * useAppSelector, selectCurrentUser, and the logo asset are unresolved.
 * The non-null Redux user is local profile state, not authenticated identity.
 * App and Home import the default export. Editor, Settings, and Templates request a named
 * Header export that this module does not provide.
 * The rendered avatar and name fields exist on no user contract. The documents and login
 * links also target routes that App does not declare.
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

/**
 * Render the application header.
 *
 * @returns The header element.
 *
 * @example
 * <Header />
 */
const Header: React.FC = () => {
  const currentUser = useAppSelector(selectCurrentUser);

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-2 flex items-center justify-between">
        <div className="flex items-center">
          <img src="/microsoft-word-logo.png" alt="Microsoft Word Logo" className="h-8 w-8 mr-2" />
          <span className="text-xl font-bold">Microsoft Word</span>
        </div>
        
        <nav>
          <ul className="flex space-x-4">
            <li><Link to="/" className="text-gray-600 hover:text-gray-900">Home</Link></li>
            <li><Link to="/documents" className="text-gray-600 hover:text-gray-900">Documents</Link></li>
            <li><Link to="/templates" className="text-gray-600 hover:text-gray-900">Templates</Link></li>
          </ul>
        </nav>
        
        <div>
          {currentUser ? (
            <div className="flex items-center">
              <img src={currentUser.avatar} alt={currentUser.name} className="h-8 w-8 rounded-full mr-2" />
              <span>{currentUser.name}</span>
            </div>
          ) : (
            <Link to="/login" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
              Login
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;