import requests
import argparse
import json

# VOICEVOXをインストールしたPCのホスト名を指定してください
HOSTNAME = 'Giru28noMacBook-Air.local'

# コマンド引数
parser = argparse.ArgumentParser(description='VOICEVOX API')
parser.add_argument('-i', '--input_file', type=str, required=True, help='読み込むテキストファイルのパス')
parser.add_argument('-id', '--speaker_id', type=int, default=2, help='話者ID')
parser.add_argument('-f', '--filename', type=str, default='voicevox', help='ファイル名')
parser.add_argument('-o', '--output_path', type=str, default='.', help='出力パス名')

# コマンド引数分析
args = parser.parse_args()
input_file = args.input_file
speaker = args.speaker_id
filename = args.filename
output_path = args.output_path

# テキストファイルを読み込む
with open(input_file, 'r', encoding='utf-8') as file:
    input_text = file.read()

# 「。」で文章を区切り、1行ずつ音声合成させる
texts = input_text.split('。')

# 音声合成処理のループ
for i, text in enumerate(texts):
    # 文字列が空の場合は処理しない
    if not text.strip():
        continue

    # audio_query (音声合成用のクエリを作成するAPI)
    res1 = requests.post(f'http://{HOSTNAME}:50021/audio_query', params={'text': text, 'speaker': speaker})
    
    # synthesis (音声合成するAPI)
    res2 = requests.post(f'http://{HOSTNAME}:50021/synthesis', params={'speaker': speaker}, data=json.dumps(res1.json()))

    # WAVファイルに書き込み
    output_filename = f'{filename}_{i:03d}.wav'
    output_file_path = f'{output_path}/{output_filename}'
    with open(output_file_path, mode='wb') as f:
        f.write(res2.content)

    print(f'合成された音声を {output_file_path} に保存しました。')
