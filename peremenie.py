FOLDER_ID = 'b1gtm0ldgri21qmdko11'
IAM_TOKEN = 't1.9euelZqNmZTNi86KmsuWm8rGjIuXi-3rnpWajYzIi5XJmpGYkouJyZTKzJzl8_dkRwdO-e8MBRxU_t3z9yR2BE757wwFHFT-zef1656Vms-MlsbIz83GmZuZzM_NjJWZ7_zF656Vms-MlsbIz83GmZuZzM_NjJWZveuelZrMnM7PkJOcipWczM_Li5iNlLXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye._0V0pz1oedo7EC1x7PiYQeA6bu02A_VFPNM2Q4C1_Vx2j6Wfpb9wbZDKoUn09WLJZWvhIaHgfHlU3Wcfu9_cDQ'


MAX_SYMBOLS = 100
MAX_USER_STT_BLOCKS = 15

headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
tts_url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
params = "&".join([
    "topic=general",
    f"folderId={FOLDER_ID}",
    "lang=ru-RU"
])
stt_url = f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}"

DB_NAME = 'database.db'
TABLE_NAME = 'sos'

count = {"tok": 120} #da ya znau pochemy ne db
history = []
gpt_url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
gpt_headers = {
    'Authorization': f'Bearer {IAM_TOKEN}',
    'Content-Type': 'application/json'
}