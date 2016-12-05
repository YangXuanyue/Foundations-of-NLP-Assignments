from codecs import open
from random import randint

MAX_BUF_LEN = 100
MAX_ASCII_VAL = 127


def gen_reordered_data(data_set_num):
    in_file = open("data/1998-01-105-带音.txt", 'r', encoding='gbk')
    segmented_data_buf = [[] for i in range(data_set_num)]
    tagged_data_buf = [[] for i in range(data_set_num)]
    data_buf_len = [0] * data_set_num

    cur_word = ""
    cur_tag = ""
    cur_segmented_sentence = ""
    cur_tagged_sentence = ""

    for data_set_id in range(data_set_num):
        segmented_data_file = open("data/segmented/data_" + str(data_set_id) + ".txt", 'w+',
                                   encoding='utf-8')
        segmented_data_file.write('')
        tagged_data_file = open("data/tagged/data_" + str(data_set_id) + ".txt", 'w+',
                                encoding='utf-8')
        tagged_data_file.write('')

    for line in in_file:
        has_read_tag = True
        is_in_brace = False
        for char in line:
            if ord(char) > MAX_ASCII_VAL:
                cur_word += char
                has_read_tag = False
            else:
                if char == '{':
                    is_in_brace = True
                if not is_in_brace:
                    if char not in [' ', ']']:
                        if not has_read_tag:
                            cur_tag += char
                    else:
                        has_read_tag = True
                        if len(cur_word) > 0:
                            cur_segmented_sentence += cur_word + ' '
                            cur_tagged_sentence += cur_word + cur_tag[1:] + ' '
                            cur_word = ""
                            cur_tag = ""
                if char == '}':
                    is_in_brace = False
        if len(cur_segmented_sentence) > 0:
            data_set_id = randint(0, data_set_num - 1)
            segmented_data_buf[data_set_id].append(cur_segmented_sentence)
            cur_segmented_sentence = ""
            tagged_data_buf[data_set_id].append(cur_tagged_sentence)
            cur_tagged_sentence = ""
            data_buf_len[data_set_id] += 1
            if data_buf_len[data_set_id] == MAX_BUF_LEN:
                segmented_data_file = open("data/segmented/data_" + str(data_set_id)
                                           + ".txt", 'a', encoding='utf-8')
                segmented_data_file.write('\n'.join(segmented_data_buf[data_set_id]))
                segmented_data_buf[data_set_id] = []
                tagged_data_file = open("data/tagged/data_" + str(data_set_id) + ".txt", 'a',
                                        encoding='utf-8')
                tagged_data_file.write('\n'.join(tagged_data_buf[data_set_id]))
                tagged_data_buf[data_set_id] = []
                data_buf_len[data_set_id] = 0

    for data_set_id in range(data_set_num):
        if data_buf_len[data_set_id] > 0:
            segmented_data_file = open("data/segmented/data_" + str(data_set_id) + ".txt", 'a',
                                       encoding='utf-8')
            segmented_data_file.write('\n'.join(segmented_data_buf[data_set_id]))
            segmented_data_buf[data_set_id] = []
            tagged_data_file = open("data/tagged/data_" + str(data_set_id) + ".txt", 'a',
                                    encoding='utf-8')
            tagged_data_file.write('\n'.join(tagged_data_buf[data_set_id]))
            tagged_data_buf[data_set_id] = []
            data_buf_len[data_set_id] = 0
