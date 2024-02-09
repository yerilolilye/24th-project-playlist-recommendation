import pandas as pd
import json

path = './data/keyword.json'

def load_keyword(path):
    with open(path,'r',encoding='utf-8') as f:
        keywords = [json.loads(line) for line in f]
    return keywords

df = load_keyword(path)
print(df[0])