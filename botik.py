from telebot import TeleBot
import logging
from telebot.types import Message
from peremenie import TG_TOKEN
from datab import prepare_db
from speechk import speech_to_text, text_to_speech
from yandex import zaproc
from validt import is_stt_block_limit, is_tts_symbobl_limit

bot = TeleBot(TG_TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)


@bot.message_handler(commands=['debug'])
def logi_typie(message):
    logging.info("Отправка логов")
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я самый удобный бот помощник, напиши и проверь. Для списка команд нажми на /help')
    logging.info("Отправка приветственного сообщения")



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Cписок возможных команд:\n'
                                      '/tts - преобразовать текст в гс\n'
                                      '/stt - преобразовать гс в текст\n'
                                      '/gpt - задать вопрос нейросети (текстом или голосом)')



@bot.message_handler(commands=['gpt'])
def send_request(message):
    bot.send_message(message.chat.id, "Введи запрос к GPT: ")
    bot.register_next_step_handler(message, proverko)

def proverko(message: Message):
    logging.info("Отправка запроса к гпт")
    if message.voice:
        logging.info("Обработка голоса")
        user_id = message.chat.id
        stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)
        if not stt_blocks:
            bot.send_message(user_id, error_message)
            return

        voice_id = message.voice.file_id
        file_info = bot.get_file(voice_id)
        file = bot.download_file(file_info.file_path)

        status, message = speech_to_text(file)
        if not status:
            bot.send_message(user_id, message)
            return
        messagee = zaproc(message['result'])
        status, message = text_to_speech(messagee)
        if not status:
            bot.send_message(user_id, message)
            return
        bot.send_message(message.chat.id, 'Ответ от нейросетки: ')
        bot.send_voice(user_id, message)

    elif message.text:
        logging.info("Обработка текста")
        messagee = zaproc(message)
        bot.send_message(message.chat.id, f'Ответ от нейросетки: {messagee}')




@bot.message_handler(commands=['stt'])
def stt_handler(message):
    bot.send_message(message.chat.id, 'пр кинь гс я разберу')
    bot.register_next_step_handler(message, stt)


def stt(message: Message):
    user_id = message.chat.id
    if not message.voice:
        bot.send_message(user_id, 'не гс')
        return


    stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)
    if not stt_blocks:
        bot.send_message(user_id, error_message)
        return

    voice_id = message.voice.file_id
    file_info = bot.get_file(voice_id)
    file = bot.download_file(file_info.file_path)

    status, message = speech_to_text(file)
    if not status:
        bot.send_message(user_id, message)
        return

    bot.send_message(user_id, message['result'])




@bot.message_handler(commands=['tts'])
def tts_handler(message: Message):
    bot.send_message(message.chat.id, 'кидай че спеть в гс')
    bot.register_next_step_handler(message, tts)


def tts(message: Message):
    user_id = message.chat.id
    if message.content_type != 'text':
        bot.send_message(user_id, 'это не текст')
        bot.register_next_step_handler(message, tts)
        return

    tts_sym, error_message = is_tts_symbobl_limit(user_id, message.text)
    if not tts_sym:
        bot.send_message(user_id, error_message)
        return

    status, message_data = text_to_speech(message.text)
    if not status:
        bot.send_message(user_id, message_data)
        return

    bot.send_voice(user_id, message_data)


if __name__ == '__main__':
    prepare_db()
    bot.polling()