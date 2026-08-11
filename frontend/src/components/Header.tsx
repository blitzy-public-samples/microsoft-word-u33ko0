/**
 * Render the top navigation bar and the signed-in user's identity.
 *
 * `useAppSelector` and `selectCurrentUser` are both imported and neither exists in
 * the store folder, so this component cannot compile. The `@/` prefix on both
 * imports raises TS2307 as well.
 *
 * @see ./README.md
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

/**
 * Render the brand mark, three navigation links and the user block.
 *
 * The logo file is not committed, so the image renders as broken alt text. Of the two
 * resource links, `/templates` is declared and `/documents` is not, so `/documents`
 * matches no route in `App.tsx`. The signed-in block reads `currentUser.avatar` and
 * `currentUser.name`, and no user contract on either side of the boundary declares
 * either field. The client schema has `username` and `full_name` instead.
 *
 * `App.tsx` and three pages each render this component, so a route paints it twice
 * and produces two navigation landmarks with the same accessible name.
 *
 * @returns The header element.
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