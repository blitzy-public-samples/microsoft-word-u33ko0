/**
 * Mount the React application into the `#root` element supplied by `public/index.html`.
 *
 * Importing this module renders the tree, because the last statement calls `renderApp`
 * during module evaluation. The module exports nothing.
 *
 * The `@/App` and `@/store` specifiers do not resolve, because `tsconfig.json` declares
 * path aliases that exclude `@/`. Rendering goes through `ReactDOM.render`, the React 17
 * entry point, while the manifest declares `react-dom` 18. The `Provider` here is the
 * first of two wrapping the same store, because `App` wraps a second.
 */

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from '@/App';
import store from '@/store';

const rootElement = document.getElementById('root');

/**
 * Render the application into the `#root` element, or log and return when it is missing.
 *
 * @returns Nothing.
 * @remarks Mounts the `StrictMode` tree into `#root`; logs and returns when the mount
 *   element is absent, leaving no fallback on screen.
 */
const renderApp = (): void => {
  if (!rootElement) {
    console.error('Root element not found');
    return;
  }

  ReactDOM.render(
    <React.StrictMode>
      <Provider store={store}>
        <App />
      </Provider>
    </React.StrictMode>,
    rootElement
  );
};

renderApp();