import requests
from telebot import TeleBot
from telebot.types import Message
from peremenie import count, history, gpt_url, gpt_headers, TG_TOKEN


bot = TeleBot(TG_TOKEN)

def process_resp(response):
    if response.status_code != 200:
        return f'Ошибка, код {response.status_code}'
    resp = response.json()
    messagegpt = resp["result"]["alternatives"][0]["message"]["text"]
    return messagegpt



def zaproc(message: Message):
    if len(message.text) > 30:
        bot.send_message(message.chat.id, "Запрос превышает количество символов!")
        return
    else:
        if count["tok"] >= 30:
            answer = message.text
            history_str = '/n'.join(history)
            count["tok"] -= 30
            response = requests.post(gpt_url, headers=gpt_headers, json=make_promt(answer + ": " + history_str))
            messagee = process_resp(response)
            history.append(messagee)
            return messagee
        else:
            bot.send_message(message.chat.id, "Токены кончились")
            return



def make_promt(user_request):
    json = {
        "modelUri": f"gpt://b1gtm0ldgri21qmdko11/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "30"
        },
        "messages": [
            {
                "role": "user",
                "text": user_request
            }
        ]
    }
    return json