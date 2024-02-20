import React from "react";
import "./result.css"; // ResultPage에 대한 스타일 시트
import logo from "./images/brand.png"; // 로고 이미지를 import합니다.
import { FcApproval } from "react-icons/fc";

const ResultPage = ({ bookTitle, songsData, keywords }) => {
  // 키워드 문자열을 #태그로 분리하여 배열로 변환
  const keywordTags = keywords.split(" ").map((keyword, index) => (
    <span key={index} className="keyword">
      #{keyword}
    </span>
  ));

  return (
    <div className="result-page">
      <header className="result-header">
        <div className="service-title">
          <span>Play</span>
          <img src={logo} alt="logo" className='logo-image' />
          <span>Book</span>
        </div>
      <hr />
      </header>
      <div className='total'>
        <div className="content">
          <div className="playlist-info-box">
            <h2>My</h2>
            <h2>Book</h2>
            <h2>Playlist</h2>

            <div className='detail'>
              <h4>나만의 도서 플레이리스트가 완성되었어요!</h4>
              <h4>지금 바로 감상하세요.</h4>
            </div>
            <hr className='innerline'/>
            <button onClick = {() => window.location.reload()} className="go-back-button">다른 도서로 검색하기</button>

          </div>
        </div>
          <div className='playlist-container'>
            <div className="playlist-box">
              <div className="music-icon-container">
                <FcApproval className="music-icon" />
              </div>
              <div className="book-title">
                <strong>Title: </strong> {bookTitle}
              </div>
              <div className="keywords">
                {keywordTags}
              </div>
            </div>
            <div className='songs-list-container'>
              <div className="songs-list">
                <div className='song-header'>
                  <span className="track-name">노래</span>
                  <span className="artist-name">아티스트</span>
                  <span className="predicted-score">예상 점수</span>
                </div>
                <hr className='innerline'/>
                {/* songsData를 매핑하여 노래 목록을 표시하는 로직 */}
                {songsData.map((song, index) => (
                  <div key={index} className="song">
                    <span className="track-name">{song.trackName}</span>
                    <span className="artist-name">{song.artistName}</span>
                    <span className="predicted-score">{song.predictedScore}</span>
                  </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
  );
};

export default ResultPage;

