import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from '@/App';
import store from '@/store';

const rootElement = document.getElementById('root');

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