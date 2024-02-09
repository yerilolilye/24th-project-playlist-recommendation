# 클러스터 선택을 위한 파이썬 파일
# ./scripts/cluster_retrieval.sh 파일 실행해서 분류

import pandas as pd
import numpy as np
import random
import json
import argparse
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, pipeline


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--model',type=str,default='"Ehsanl/Roberta-DNLI')
    parser.add_argument('--key_data',type=str)
    parser.add_argument('--song_data',type=str)
    parser.add_argument('--n_cluster',type=int, help='number of clusters')
    parser.add_argument('--n_cluster_sample',type=int, help='number of samples used from each cluster for cluster selection')
    parser.add_argumnet('--n_songs',type=int,help='number of songs in final playlist')
    args = parser.parse_args()

    return args


def read_json(path):
    with open(path, 'r',encoding='cp949') as f:
        json_objects = [json.loads(line) for line in f]
        json_objects = pd.DataFrame(json_objects)
    return json_objects.to_dict('records')


def load_songs(args):
    print('**** Loading song data ... ****')
    songs = read_json(args.song_data)
    return songs


def group_by_cluster(songs, n_cluster):
    '''
    songs 데이터를 cluster별로 분류
    return format: [[cluster_1],[cluster_2],...,[cluster_n]]
    '''
    print('**** Sorting Songs by Clusters ... ****')
    for n in range(n_cluster): 
        # cluster 개수만큼 리스트 생성
        globals()['cluster_{}'.format(n)] =[]

    for song in tqdm(range(len(songs))):
        # 음악 클러스터별 분류
        globals()['cluster_{}',format(song['cluster'])].append(song)
    
    cluster = []
    
    # 분류된 리스트 하나의 리스트로 묶어 리턴
    for n in range(n_cluster):
        cluster.append(globals()['cluster_{}'.format(n)])
    
    print('**** Sorting completed !!! ****')
    return cluster 


def load_keyword(path):
    '''
    keyword file format이 리스트 한줄짜리 json이라고 가정
    input format : {"keywords":["줄거리키워드1","줄거리키워드2"]}
    output format : "줄거리키워드1 줄거리키워드2"
    
    ### book crawler 완성 이후 input() 함수로 사용자에게 input 받게끔 수정 ###
    '''
    print('**** Loading keyword input ****')
    with open(path,'r',encoding='utf-8') as f:
        keywords = [json.loads(line) for line in f]
        keywords = keywords[0]['keywords'].join(' ')

    return keywords # dtype: str


def pick_random_sample(cluster,n_sample):
    '''
    각 cluster에서 랜덤으로 n개의 샘플 추출하여 리턴
    return format : { 1:[cluster_1_samples], ..., n:[cluster_n_samples] }
    '''
    print('**** Random Sampling from each cluster ... ****')

    random_samples = {}
    for i in range(len(cluster)):
        random_sample = random.choice(cluster[i],n_sample)
        random_samples[i] = random_sample
    
    return random_samples
        

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = pipeline("text-classification", model=args.model,device="cpu")
    return model, tokenizer


def model_scoring(keywords, song_list, model):
    '''
    keyword와 각각의 song의 가사를 짝지어 데이터셋 구축
        - cluster selection 단계: song_list = random_samples[n]
        - cluster scoring 단계: song_list = selected_cluster 
            selected_cluster format : [{song},{song},{song},{song}]
    ############# song['lyrics']로 가정 ################
    '''

    # formatting inputs
    inputs = []
    keyword_lst = []
    track_name = []
    artist_name = []

    for song in song_list:
        track_name.append(song['track_name'])
        artist_name.append(song['artist_name'])
        keyword_lst.append(keywords)
        input = keywords + ' ' + tokenizer.sep_token + ' ' + song['lyrics']
        inputs.append(input)


    # model infernece
    outputs = model(inputs)
    output_dic = []
    for keyword, track_name, artist_name, output in zip(keyword_lst, track_name, artist_name, outputs):
        dic = {'track_name': track_name,
               'artist_name': artist_name,
               'keyword': keyword,
               'predicted_label': output['label'],
               'predicted_score': output['score']}
    output_dic.append(dic)

    return output_dic


def select_cluster(random_samples,keywords,model):
    mean_score = {}

    # 각 cluster별로 다음을 시행
    for n in range(len(random_samples)):
        output_dic = model_scoring(keywords=keywords,
                                   song_list=random_samples[n],
                                   model=model)
        
        score = []
        for output in output_dic:
            if output['predicted_label']=='ENTAILMENT': #레이블이 entailment인 것만 scoring
                score.append(output['predicted_score'])

        # 클러스터별로 평균 내기
        mean_score = np.mean(score)
        mean_score[n] = mean_score
        
    return max(mean_score,key=mean_score.get) # mean score가 가장 높은 cluster number 리턴


def playlist_recommendation(output_dic, n_songs):

    df = pd.DataFrame(output_dic)
    df_ent = df[ df['predicted_label']=='ENTAILMENT' ]
    playlist_df = df_ent['track_name','artist_name','predicted_score'].sort_values(by=['predicted_score'],ascending=False)

    return playlist_df.iloc[:n_songs,:]


def main(args):
    songs = load_songs(args)


if __name__ == '__main__':
    args = parse_args()
    main(args)