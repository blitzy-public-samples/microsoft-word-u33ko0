/**
 * Top navigation bar. Renders branding, the primary link list, and either the signed-in user
 * or a login link. Every `L` reference numbers a file as committed, before any comment block.
 *
 * Four references in this file resolve to nothing:
 * - `useAppSelector` (L3). `frontend/src/store/index.ts` exports `RootState`, `AppDispatch`
 *   and a default `store`, and declares no such hook.
 * - `selectCurrentUser` (L4). `frontend/src/store/userSlice.ts` exports `setUser`,
 *   `clearUser`, `setLoading`, `setError` and a default reducer, and declares no selector.
 * - The logo at L13 does not load, because `frontend/public/` holds only `index.html`.
 * - `currentUser.avatar` and `currentUser.name` (L28, L29). No user contract declares either
 *   field; `frontend/src/schema/user.ts:L6-L7` declares `username` and optional `full_name`.
 *
 * Two of the four links go nowhere. `frontend/src/App.tsx:L20-L23` declares `/`, `/editor`,
 * `/templates` and `/settings`, so `/` (L19) and `/templates` (L21) resolve while
 * `/documents` (L20) and `/login` (L32) match no route.
 *
 * Every class name here is a Tailwind utility, and nothing compiles them.
 * `frontend/package.json:L12` declares `tailwindcss`, while the repository commits no
 * `tailwind.config.js`, no `postcss.config.js` and no stylesheet.
 *
 * `App.tsx:L4` imports the L42 default export correctly, while `pages/Editor.tsx:L2` imports
 * it as a named import. See `./README.md` for the directory register.
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

/**
 * Render the application's top navigation bar.
 *
 * @returns A `header` element holding the branding block (L12-L15), the nav list (L17-L23),
 * and the conditional user block (L25-L36).
 *
 * @remarks
 * The selector call at L7 is the only external read, and no dispatch or network call runs here.
 *
 * The branch at L26 tests `currentUser`, then reads `.avatar` and `.name` at L28 and L29.
 * `store/userSlice.ts:L5` types that value `User | null`, which `schema/user.ts:L13` infers
 * from a schema declaring neither field.
 *
 * @example
 *     <Provider store={store}>
 *       <Header />
 *     </Provider>
 * The snippet cannot run: `tsc` reports `TS2307` for `@/store` at `Header.tsx(3,32)`, so the
 * `useAppSelector` call at L7 never resolves.
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