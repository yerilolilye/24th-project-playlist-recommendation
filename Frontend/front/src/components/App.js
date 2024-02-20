import React, { useState, useEffect } from 'react';
import { FaSearch  } from 'react-icons/fa'; 
import { Helmet } from 'react-helmet';
import logo from './images/brand.png';
import './App.css';
import Loading from './loading';
import ResultPage from './result';

export default function App() {
  const [inputText, setInputText] = useState('');
  const [isError, setIsError] = useState(false);
  const [loading, setIsLoading] = useState(false);
  const [showResultPage, setShowResultPage] = useState(false);
  const [result, setResult] = useState('');

  const handleRunPythonScript = async () => {
    if (!(inputText.startsWith('https://www.yes24.com/Product/Goods') || inputText.startsWith('https://m.yes24.com/Goods/Detail'))) {
        setIsError(true); 
        return; 
      } 
    if (inputText === '') {setIsError(true); return;}
    
    setIsError(false);
    setIsLoading(true);

    try {
      const requestData = { inputData: inputText };
      console.log('Request Data:', requestData);
      const response = await fetch('http://34.64.113.59/runPythonScript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputData: inputText }),
      });
      if (!response.ok) {
      // 에러 응답 처리
      	throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
          // 데이터 구조 변환
      const formattedData = {
        bookTitle: data.book_title,
        songsData: data.track_name.map((trackName, index) => ({
          trackName: trackName,
          artistName: data.artist_name[index],
          predictedScore: data.predicted_score[index]
        })),
        keywords: data.keywords
      };
      setResult(formattedData);
      setShowResultPage(true);
    } catch (error) {
      console.error('Error:', error);
      setIsError(true);
    } finally {
        setIsLoading(false);
    }
  };

  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleRunPythonScript();
    };
  }

  return (
    <div className="App">
      <Helmet>
        <title>Play Book</title>
        <link rel="icon" type="image/png" href={logo} />
        <meta
          name="description"
          content="Play Book은 yes24 도서 상세페이지 URL을 입력하면 해당 도서와 어울리는 음악 추천을 해주는 웹 애플리케이션입니다."
        />
      </Helmet>
      {!showResultPage ? (
      <div className="search-container">
        <div className="header">
          <img src={logo} alt="Brand Logo" className="brand-logo" />
          <div>
            <p className="tagline">From Pages to Music</p>
            <h1 className="title">Play Book</h1>
          </div>
          </div>
          <div className="search-box">
            <FaSearch className="search-icon" />
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown = {handleKeyDown}
              placeholder="yes24 도서 상세페이지 URL을 입력해주세요"
            />
          <button onClick={handleRunPythonScript} className='send-button'> Find Now</button>
            </div>
          
          {isError && (
              <div className="error-message">URL이 올바르지 않습니다. yes24 도서 상세페이지 URL을 입력해주세요.</div>
          )}
          {loading && <Loading />}
            {!loading && (
            <a href="https://www.yes24.com/main/default.aspx" target="_blank" rel="noopener noreferrer" className="yes24-link">
              yes24 홈페이지에서 도서 검색하러 가기
            </a>
          )}
        </div>) : (
          <ResultPage bookTitle={result.bookTitle} songsData={result.songsData} keywords={result.keywords} />
        )}
    </div>
  )
};


