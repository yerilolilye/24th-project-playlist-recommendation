# 책 기반 플레이리스트 추천

## Currently...
- spotify api 활용하여 음악 데이터셋 구성 중
- 사용자로부터 책 정보를 input으로 받는 크롤러 코드 작성 예정
- sample data 기반으로 playlist 추출하는 코드 작성 완료
    - 결과 샘플은 `./sample_result.txt`에서 확인 가능합니다
    - 참고로 데이터 샘플 5개(음악 데이터 가사 & 키워드는 제가 임의로 아무거나 추가했어요)로만 테스트해봐서 결과는 1개만 출력됨
  
## HOW TO
플레이리스트 추출을 위해서는 './scripts/playlist_recommendation.sh' 파일의 arguments를 수정한 후, linux 터미널에 다음을 입력하세요

    sh ./scripts/playlist_recommendation.sh

만약 GPU를 사용할 경우 다음을 입력하면 됩니다.

    CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 sh ./scripts/playlist_recommendation.sh 

