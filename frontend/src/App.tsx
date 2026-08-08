/**
 * Compose the application shell, and declare the client-side route table.
 *
 * @remarks
 * Seven `@/` specifiers do not resolve, because `tsconfig.json` declares aliases that
 * exclude the prefix. The store import fails twice, binding `{ store }` by name where
 * `store/index.ts` exports `store` only as the default.
 *
 * Three router call sites use react-router-dom v5 APIs while the manifest declares v6.
 * Version 6 exports `Routes` rather than `Switch`, and `Route` accepts neither
 * `component` nor `exact`.
 */

import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Home from '@/pages/Home';
import Editor from '@/pages/Editor';
import Templates from '@/pages/Templates';
import Settings from '@/pages/Settings';
import { store } from '@/store/index';

/**
 * Render the shared header and footer around a routed main area, inside a Redux and router shell.
 *
 * @returns The provider, router and shell element tree wrapping the routed page area.
 * @remarks
 * The component declares the complete routed surface: `/` to `Home`, `/editor` to `Editor`,
 * `/templates` to `Templates`, `/settings` to `Settings`. Five links elsewhere target absent paths.
 *
 * Accessibility: the shell owns the one `<main>` landmark, and `Home`, `Settings` and `Templates`
 * each render a second inside it, nesting one main within another. All four pages repeat the
 * `Header`, so `banner` and the unnamed `<nav>` at `components/Header.tsx:L66` both duplicate on
 * every route, leaving two indistinguishable navigation landmarks that each need a distinct name.
 * Three pages repeat the `Footer`, so `contentinfo` duplicates on three routes, not on `Editor`.
 *
 * Intended behavior per `documentation/Technical Specifications.md`, "USER INTERFACE DESIGN"
 * heading: `Toolbar`, `DocumentCanvas` and `Sidebar` sit under `App` rather than under `Editor`.
 *
 * @see ./README.md for the shell-level register of these findings.
 */
const App: React.FC = () => {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <div className="app">
          <Header />
          <main>
            <Switch>
              <Route exact path="/" component={Home} />
              <Route path="/editor" component={Editor} />
              <Route path="/templates" component={Templates} />
              <Route path="/settings" component={Settings} />
            </Switch>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </Provider>
  );
};

export default App;