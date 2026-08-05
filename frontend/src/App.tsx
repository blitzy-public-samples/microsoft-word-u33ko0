/**
 * Compose the application shell, and declare the client-side route table.
 *
 * @remarks
 * Seven imports do not resolve. L4-L9 and L10 use the `@/` prefix, and
 * `frontend/tsconfig.json:L10-L16` declares five aliases that do not include it. L10 fails twice,
 * binding `{ store }` by name where `store/index.ts:L15` exports `store` only as the default.
 *
 * Three router call sites use react-router-dom v5 APIs while `frontend/package.json:L11` declares
 * `^6.11.1`: `Switch` at L2 and L19, `exact` at L20, and `component` at L20-L23. Version 6 exports
 * `Routes` rather than `Switch`, and `Route` accepts neither `component` nor `exact`.
 *
 * The `Provider` at L14 is the second wrapping this store, because `index.tsx:L17` already wraps
 * one. The module declares four routes and exports one symbol, the default `App` at L33. Every
 * `Lnn` here numbers the frozen revision 06be74c that precedes this documentation pass.
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
 * @remarks
 * The component declares the complete routed surface: `/` to `Home`, `/editor` to `Editor`,
 * `/templates` to `Templates`, `/settings` to `Settings`. Five links elsewhere target paths
 * absent from that list. Every page repeats part of this shell, adding a second `Header` on all
 * four routes and a second `Footer` on three. `./README.md` registers both under Known Limitations.
 *
 * Intended behavior per `documentation/Technical Specifications.md`, "USER INTERFACE DESIGN"
 * heading: `Toolbar`, `DocumentCanvas` and `Sidebar` sit under `App` rather than under `Editor`.
 *
 * @returns The provider, router and shell element tree wrapping the routed page area.
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