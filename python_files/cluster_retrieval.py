# 클러스터 선택을 위한 파이썬 파일
# ./scripts/cluster_retrieval.sh 파일 실행해서 분류

import pandas as pd
import json
import argparse
from tqdm import tqdm
import scoring

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--key_data',type=str)
    parser.add_argument('--song_data',type=str)
    parser.add_argument('--n_cluster',type=int, help='number of clusters')
    args = parser.parse_args()

    return args


def read_json(path): #cp949 오류가 뜸...
    with open(path, 'r',encoding='utf-8') as f:
        json_objects = [json.loads(line) for line in f]
        df = pd.DataFrame(json_objects)
        df = df.to_dict('records')
    return df


def load_songs(args):
    songs = read_json(args.song_data)
    return songs


def group_by_cluster(songs, n_cluster):
    for n in range(n_cluster):
        globals()[''.format(n)] =[]
    # 클러스터 개수 조정에 따라 동적으로 구성
    return

def load_keyword(args):
    # TODO
    return


def main(args):
    songs = load_songs(args)


if __name__ == '__main__':
    args = parse_args()
    main(args)