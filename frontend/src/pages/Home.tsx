/**
 * Render the landing page: a greeting and three quick-access links.
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
 * The three quick-access links at L18, L21 and L24 target /new-document, /open-document and
 * /recent-documents. App.tsx:L20-L23 declares only /, /editor, /templates and /settings, so
 * none of the three targets matches a declared route.
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
 * Reads currentUser from the store, and performs no write, no request and no imperative
 * navigation. The page renders three declarative `Link` elements instead, which navigate when
 * a reader clicks one.
 *
 * @returns The home page element.
 * @remarks App renders Header and Footer around every route, so this page renders a second
 * header and a second footer. The three links at L18, L21 and L24 target /new-document,
 * /open-document and /recent-documents. App declares only /, /editor, /templates and
 * /settings, so each of the three targets an undeclared route and a click reaches no page.
 * The page calls no router hook, so nothing here navigates on its own.
 *
 * Accessibility: the page renders a second `main` element inside App's `main`, so one main
 * landmark nests inside another, and the repeated header and footer duplicate the banner and
 * contentinfo landmarks.
 * @example
 * <Route path="/" element={<Home />} />
 * // `frontend/package.json:L11` declares `react-router-dom` at `^6.11.1`, which takes an
 * // `element` prop and dropped both the v5 `component` prop and `exact`. `App.tsx:L19-L24`
 * // holds the committed route table, still written in the version 5 form.
 * // `App.tsx:L20` is the registration this snippet reproduces.
 * // Cannot run today: the four `@/` specifiers at L3-L6 fail module resolution, and neither
 * // `useAppSelector` at L5 nor `selectCurrentUser` at L6 is exported by the module it names.
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