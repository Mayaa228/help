import math
from peremenie import MAX_USER_STT_BLOCKS, MAX_SYMBOLS
from datab import insert_stt, insert_tts, count_bloks, count_symbobl


def is_stt_block_limit(user_id, duration):
    if duration > 30:
        return None, 'слишком много сек мне лень'

    cur_blocks = math.ceil(duration / 15)
    insert_stt(user_id, cur_blocks)
    user_bloks = count_bloks(user_id)
    all_blocks = user_bloks + cur_blocks

    if all_blocks >= MAX_USER_STT_BLOCKS:
        return None, 'все кончилось'

    return all_blocks, ''


def is_tts_symbobl_limit(user_id, text):
    cur_sym = len(text)

    if cur_sym >= 50:
        return None, 'за раз больше 50 симбоболс не приму'

    insert_tts(user_id, text, cur_sym)
    user_sym = count_symbobl(user_id)
    all_symbobls = user_sym + cur_sym

    if all_symbobls >= MAX_SYMBOLS:
        return None, 'тебе слишком жирно озвучки'

    return all_symbobls, ''
