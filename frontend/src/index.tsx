/**
 * Mount the application into the `root` element of the served HTML shell.
 *
 * Both imports use the `@/` prefix, which `tsconfig.json` does not map and
 * `react-scripts` 5 would not apply to webpack resolution, so each raises TS2307.
 * `store` is imported as a default export, which `store/index.ts` provides.
 *
 * @see ./README.md
 */
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from '@/App';
import store from '@/store';

const rootElement = document.getElementById('root');

/**
 * Render the provider tree into the root element, or log and stop when it is absent.
 *
 * Uses `ReactDOM.render`, the React 17 entry point. React 18 is the declared
 * dependency and warns that `createRoot` replaces it, so strict-mode double
 * rendering and concurrent features stay off.
 *
 * @returns Nothing. The call at the end of the file invokes this once at load.
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