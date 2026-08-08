/**
 * Compose the routed application shell: providers, chrome and four routes.
 *
 * `store` is imported as a named export and `store/index.ts` exports it as a
 * default, so the import resolves to `undefined`. `Switch` is the react-router-dom
 * version 5 API, and version 6.8.1 is the declared dependency, which replaced it
 * with `Routes`.
 *
 * @see ./README.md
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
 * Render the provider tree, the chrome and the four declared routes.
 *
 * The component wraps its tree in a second `Provider`, because `index.tsx` already
 * wraps `App` in one. `App` also renders `Header` and `Footer` here while `Home`,
 * `Editor`, `Templates` and `Settings` render their own, so every route paints the
 * chrome twice. Two `Header` instances mean two navigation landmarks with the same
 * accessible name, which a screen-reader user cannot tell apart.
 *
 * @returns The application element tree.
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