// src/index.js

import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App.js'; // App 컴포넌트의 경로에 맞게 수정

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

