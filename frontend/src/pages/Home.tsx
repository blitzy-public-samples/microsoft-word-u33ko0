/** Render the landing page: a greeting and three quick-access links.
 *
 * Header and Footer are default imports of default exports, so both match their
 * modules. Editor, Settings and Templates request a named Header export instead, and
 * Settings and Templates also request a named Footer export. Neither named export exists.
 * The `@/` prefix is absent from the tsconfig paths, so all four `@/` specifiers below fail
 * module resolution.
 * useAppSelector and selectCurrentUser do not exist. store/index.ts exports only RootState,
 * AppDispatch and a default store. store/userSlice.ts exports setUser, clearUser, setLoading,
 * setError and a default reducer, and no selector.
 * The greeting reads currentUser.name, which no user contract declares. schema/user.ts
 * models username and full_name, and Settings reads the same absent field.
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
 * Reads currentUser from the store, and performs no write, no request and no navigation.
 *
 * @returns The home page element.
 * @remarks App renders Header and Footer around every route, so this page renders a second
 * header and a second footer. The three links target /new-document, /open-document and
 * /recent-documents. App declares only /, /editor, /templates and /settings, so each link
 * reaches no route.
 * @example
 * <Route exact path="/" component={Home} />
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