/**
 * Render the landing page: a greeting and three quick-access links.
 *
 * `Header` and `Footer` are imported as defaults here, which is correct, unlike the
 * three sibling pages. `useAppSelector` and `selectCurrentUser` are both imported
 * and neither exists in the store folder.
 *
 * @see ./README.md
 */
import React from 'react';
import { Link } from 'react-router-dom';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

/**
 * Render the greeting and the quick-access links.
 *
 * The greeting reads `currentUser.name`, and no user contract declares that field.
 * All three links point at routes `App.tsx` does not declare, so each one navigates
 * to an unmatched path. The page renders its own `Header` and `Footer`, which
 * `App.tsx` has already rendered.
 *
 * @returns The home page element.
 */
const Home: React.FC = () => {
  const currentUser = useAppSelector(selectCurrentUser);

  return (
    <div className="home-container">
      <Header />
      <main className="home-content">
        <h1>Welcome to Microsoft Word</h1>
        {currentUser && <p>Hello, {currentUser.name}!</p>}
        <div className="quick-access">
          <Link to="/new-document" className="quick-access-button">
            New Document
          </Link>
          <Link to="/open-document" className="quick-access-button">
            Open Document
          </Link>
          <Link to="/recent-documents" className="quick-access-button">
            Recent Documents
          </Link>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Home;