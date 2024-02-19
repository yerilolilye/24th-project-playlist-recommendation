// Loading.js
import React from 'react';
import {Background, LoadingText} from './styles';
import spinner from './images/loading.gif';
import loading from './images/716.gif';

export default () => {
  return (
    <Background>
      <LoadingText>입력하신 도서에 대한 플레이리스트를 생성하는 중입니다. 잠시만 기다려 주세요.</LoadingText>
      <img src={loading} alt="loading" width = '30%' style={{ marginLeft: '200px', marginTop: '40px' }}/>
    </Background>
  );
};
