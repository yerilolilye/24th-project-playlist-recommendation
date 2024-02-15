import ReactPlayer from 'react-player/lazy';
import React, {useState } from 'react';
import './App.css';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faPlay } from '@fortawesome/free-solid-svg-icons';

export default function Playlist(props) {
    const [videos, setVideos] = useState(props.data);

    const [currentIndex, setIndex] = useState(0);

    const handleVideoSelect = (index) => {
        setIndex(index)
    };

    const handleVideo = () => {
        const newIndex = (currentIndex + 1) % videos.length;;
        setIndex(newIndex);
    };

    const handleRemoveTrack = (indexToRemove) => {
        setVideos(videos.filter((_, index) => index !== indexToRemove));
    };

    return (
        <>
        <div className = 'container'>
            <h2>Player Test</h2>
            <div className='player-wrapper'>
                <ReactPlayer
                    className='react-player'
                    url={videos[currentIndex].url}    // 플레이어 url
                    playing={true}        // 자동 재생 on
                    muted={false}          // 자동 재생 on
                    controls={true}       // 플레이어 컨트롤 노출 여부
                    onEnded={handleVideo}  // 플레이어 끝났을 때 이벤트
                />
            </div>
            <div className = 'Playlist'>
                <div className = 'header'>
                    <FontAwesomeIcon icon={faPlay} className='play' />
                    <h3>Playlist</h3>
                </div>
                <div className = 'items'>
                    {videos.map((video, index) => (
                             <div
                             key={index}
                             className={`item ${index === currentIndex ? 'selected' : ''}`}
                             onClick={() => handleVideoSelect(index)}
                         >
                             <span className="item-index">{index + 1}. </span>
                             <span className="track-name">{video.title}</span> | <span className="artist">{video.artist}</span>
                             <FontAwesomeIcon icon={faTrash} onClick={(e) => { e.stopPropagation(); handleRemoveTrack(index); }} className="item-remove" />
                         </div>
                     ))}
                 </div>
            </div>
        </div>
        </>
    );
}