import requests
from peremenie import FOLDER_ID, headers, tts_url, stt_url

def speech_to_text(data):
    response = requests.post(stt_url, headers=headers, data=data)
    decoded_data = response.json()

    if response.status_code == 200:
        return True, decoded_data
    else:
        return False, f"При запросе в SpeechKit возникла ошибка {response.status_code}"


def text_to_speech(text):
    data = {'text': text,
            'lang': 'ru-RU',
            'voice': 'ermil',
            'folderId': FOLDER_ID}

    response = requests.post(tts_url, headers=headers, data=data)
    if response.status_code == 200:
        return True, response.content
    else:
        return False, f"При запросе в SpeechKit возникла ошибка {response.status_code}"
