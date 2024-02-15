import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Playlist from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Playlist data = {[{url: 'https://www.youtube.com/watch?v=ZqJ7bfgacSA', artist: 'IU', title : 'Love Wins All'},
 {url: 'https://www.youtube.com/watch?v=dMoQpAY_H7w', artist: 'IU', title: '라일락'},
 {url: 'https://www.youtube.com/watch?v=es6bbfAjk3I', artist: 'IU', title: 'Celebrity'},
 {url : 'https://www.youtube.com/watch?v=g7TwWZjgtis', artist : 'IU', title : '이런 엔딩'}]} /> 
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
