import pandas as pd

from play_by_play_data_extraction import extract_game_data

data = []
for i in range(1, 8):
    df = extract_game_data(f'./data/okc_sas_game_{i}.html')
    df['game'] = i
    data.append(df)

combined = pd.concat(data, ignore_index=True)
combined.to_csv('./data/okc_sas_play_by_play.csv', index=False)
