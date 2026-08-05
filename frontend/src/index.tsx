/**
 * Locate the `#root` mount point and render the application into it once, at module load.
 *
 * L7 reads `#root`, which `frontend/public/index.html:L12` supplies. L25 calls `renderApp` at
 * module evaluation, so importing this module mounts the application. The module exports nothing,
 * so `renderApp` at L9 stays private to this file.
 *
 * L4 takes `@/App` and L5 takes `@/store`, and neither resolves, because
 * `frontend/tsconfig.json:L10-L16` declares five aliases that exclude `@/`. L5 is otherwise
 * correct: `store/index.ts:L15` exports `store` only as the default, which `App.tsx:L10` binds
 * by name instead.
 *
 * L15 renders through `ReactDOM.render`, the React 17 API, while `frontend/package.json:L9`
 * declares `react-dom` at `^18.2.0`. The `Provider` at L17 is the first of two wrapping this
 * store, because `App.tsx:L14` wraps a second.
 *
 * Every `Lnn` here numbers the frozen revision 06be74c that precedes this documentation pass.
 * @see frontend/src/README.md for the register covering this directory.
 */

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from '@/App';
import store from '@/store';

const rootElement = document.getElementById('root');

/**
 * Render the application into the `#root` element, or log and return when the element is missing.
 *
 * @returns Nothing. The declared result is `void`.
 * @remarks The function takes no parameters. L15 writes to the DOM through `ReactDOM.render`,
 *   mounting the `React.StrictMode` tree into `rootElement`. When L7 finds no element, L11 writes
 *   `Root element not found` to the console and L12 returns, leaving no fallback on screen.
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