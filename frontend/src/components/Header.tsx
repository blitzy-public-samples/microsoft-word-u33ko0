/**
 * Top navigation bar: branding, the link list, and either a local user block or a login link.
 *
 * The user block is local profile state, not authenticated identity. A non-null `currentUser`
 * proves only that some code dispatched `setUser`, and no token is read and no backend call is
 * made, so rendering the block is a presentation choice rather than an access decision.
 *
 * Unresolved references:
 * - `useAppSelector` does not exist in `frontend/src/store/index.ts`, and `selectCurrentUser` does
 *   not exist in `frontend/src/store/userSlice.ts`. The `@/` prefix on both specifiers is absent
 *   from the `paths` map in `frontend/tsconfig.json`, so each raises TS2307.
 * - `currentUser.avatar` and `currentUser.name` match no user contract.
 *   `frontend/src/schema/user.ts` declares `username` and optional `full_name`.
 * - The logo asset does not load, because `frontend/public/` holds only `index.html`.
 * - Two of the four links match no route. `App.tsx` declares `/`, `/editor`, `/templates` and
 *   `/settings`, so `/documents` and `/login` go nowhere.
 *
 * @see ./README.md for the directory register.
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAppSelector } from '@/store';
import { selectCurrentUser } from '@/store/userSlice';

/**
 * Render the application's top navigation bar.
 *
 * @returns A `header` element holding the branding block, the nav list and the conditional user
 * block.
 * @remarks The selector call is the only external read, and no dispatch or network call runs here.
 *
 * @remarks
 * The selector call at L7 is the only explicit data read, and no line dispatches an action or
 * calls an application programming interface. Rendering still makes browser requests. The `img`
 * at L28 sets `src` to `currentUser.avatar`, so the browser fetches that URL, and the `img` at
 * L13 fetches the static path `/microsoft-word-logo.png`. The avatar URL is the one that matters:
 * it arrives with the user object rather than from this repository, and no line validates,
 * allow-lists or rewrites it. A value pointing at an outside host makes the browser contact that
 * host on every render of a signed-in page, and the host learns the reader's internet protocol
 * (IP) address, user agent, and whatever referrer the page's policy permits.
 *
 * The branch at L26 tests `currentUser`, then reads `.avatar` and `.name` at L28 and L29.
 * `store/userSlice.ts:L5` types that value `User | null`, which `schema/user.ts:L13` infers
 * from a schema declaring neither field.
 *
 * The branch guards rendering, not access. A truthy `currentUser` means the local store holds an
 * object, so the component shows a profile block instead of the login link, and no content it
 * renders is protected by the test.
 * @example
 *     <Provider store={store}>
 *       <Header />
 *     </Provider>
 * The snippet cannot run: `@/store` raises `TS2307`, so the `useAppSelector` call never resolves.
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