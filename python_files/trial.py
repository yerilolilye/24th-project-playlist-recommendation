import pandas as pd
import json

def read_json(path):
    with open(path, 'r',encoding='cp949') as f:
        json_objects = [json.loads(line) for line in f]
        json_objects = pd.DataFrame(json_objects)
    return json_objects.to_dict('records')

df = read_json('data/output_clustered.json')
print(df)