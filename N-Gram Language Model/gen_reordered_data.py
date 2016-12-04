from codecs import open
from random import randint

MAX_BUF_LEN = 10000
MAX_ASCII_VAL = 127


def gen_reordered_data(data_set_num):
    in_file = open("data\\1998-01-105-带音.txt", 'r', encoding='gbk')
    data_buf = [[] for i in range(data_set_num)]
    data_buf_len = [0] * data_set_num

    cur_word = ""
    cur_sentence = ""
    cur_para = []

    for data_set_id in range(data_set_num):
        data_file = open("data\\reordered\\data_" + str(data_set_id) + ".txt", 'w+',
                         encoding='utf-8')
        data_file.write('')

    for line in in_file:
        line = line.strip()
        if len(line) > 0:
            for char in line:
                if ord(char) > MAX_ASCII_VAL:
                    cur_word += char
                else:
                    if len(cur_word) > 0:
                        cur_sentence += cur_word + ' '
                        cur_word = ""
            cur_para.append(cur_sentence)
            cur_sentence = ""
        else:
            if len(cur_para) > 0:
                data_set_id = randint(0, data_set_num - 1)
                data_buf[data_set_id].append('/ '.join(cur_para))
                cur_para = []
                data_buf_len[data_set_id] += 1
                if data_buf_len[data_set_id] == MAX_BUF_LEN:
                    data_file = open("data\\reordered\\data_" + str(data_set_id) + ".txt",
                                     'a', encoding='utf-8')
                    data_file.write('\n'.join(data_buf[data_set_id]))
                    data_buf[data_set_id] = []
                    data_buf_len[data_set_id] = 0
    for data_set_id in range(data_set_num):
        if data_buf_len[data_set_id] > 0:
            data_file = open("data\\reordered\\data_" + str(data_set_id) + ".txt", 'a',
                             encoding='utf-8')
            data_file.write('\n'.join(data_buf[data_set_id]))
            data_buf[data_set_id] = []
            data_buf_len[data_set_id] = 0
