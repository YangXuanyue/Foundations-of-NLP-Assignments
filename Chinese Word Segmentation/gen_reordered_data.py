from codecs import open
from random import randint

MAX_BUF_LEN = 100
MAX_ASCII_VAL = 127


def gen_reordered_data(data_set_num):

    in_file = open("data/1998-01-105-带音.txt", 'r', encoding='gbk')
    raw_data_buf = [[] for i in range(data_set_num)]
    segmented_data_buf = [[] for i in range(data_set_num)]
    tagged_data_buf = [[] for i in range(data_set_num)]
    data_buf_len = [0] * data_set_num

    cur_word = []
    cur_raw_sentence = ""
    cur_segmented_sentence = ""
    cur_tagged_sentence = ""

    for data_set_id in range(data_set_num):
        raw_data_file = open("data/reordered/raw/raw_data_" + str(data_set_id) + ".txt", 'w+',
                             encoding='utf-8')
        raw_data_file.write('')
        segmented_data_file = open("data/reordered/segmented/segmented_data_" + str(data_set_id) + ".txt", 'w+',
                                   encoding='utf-8')
        segmented_data_file.write('')
        tagged_data_file = open("data/reordered/tagged/tagged_data_" + str(data_set_id) + ".txt", 'w+',
                                encoding='utf-8')
        tagged_data_file.write('')

    for line in in_file:
        line = line.strip()
        if len(line) > 0:
            for char in line:
                if ord(char) > MAX_ASCII_VAL:
                    cur_word.append(char)
                else:
                    if len(cur_word) > 0:
                        cur_raw_sentence += ''.join(cur_word)
                        cur_segmented_sentence += ''.join(cur_word) + ' '
                        if len(cur_word) == 1:
                            cur_tagged_sentence += '3' + cur_word[0]
                        else:
                            word_len = len(cur_word)
                            cur_tagged_sentence += '0' + cur_word[0]
                            for i in range(1, word_len - 1):
                                cur_tagged_sentence += '1' + cur_word[i]
                            cur_tagged_sentence += '2' + cur_word[word_len - 1]
                        cur_word = []
        else:
            data_set_id = randint(0, data_set_num - 1)
            raw_data_buf[data_set_id].append(cur_raw_sentence)
            cur_raw_sentence = ""
            segmented_data_buf[data_set_id].append(cur_segmented_sentence)
            cur_segmented_sentence = ""
            tagged_data_buf[data_set_id].append(cur_tagged_sentence)
            cur_tagged_sentence = ""
            data_buf_len[data_set_id] += 1
            if data_buf_len[data_set_id] == MAX_BUF_LEN:
                raw_data_file = open("data/reordered/raw/raw_data_" + str(data_set_id) + ".txt",
                                     'a', encoding='utf-8')
                raw_data_file.write('\n'.join(raw_data_buf[data_set_id]))
                raw_data_buf[data_set_id] = []
                segmented_data_file = open("data/reordered/segmented/segmented_data_" + str(data_set_id)
                                           + ".txt", 'a', encoding='utf-8')
                segmented_data_file.write('\n'.join(segmented_data_buf[data_set_id]))
                segmented_data_buf[data_set_id] = []
                tagged_data_file = open("data/reordered/tagged/tagged_data_" + str(data_set_id) + ".txt", 'a',
                                        encoding='utf-8')
                tagged_data_file.write('\n'.join(tagged_data_buf[data_set_id]))
                tagged_data_buf[data_set_id] = []
                data_buf_len[data_set_id] = 0

    for data_set_id in range(data_set_num):
        if data_buf_len[data_set_id] > 0:
            raw_data_file = open("data/reordered/raw/raw_data_" + str(data_set_id) + ".txt", 'a',
                                 encoding='utf-8')
            raw_data_file.write('\n'.join(raw_data_buf[data_set_id]))
            raw_data_buf[data_set_id] = []
            segmented_data_file = open("data/reordered/segmented/segmented_data_" + str(data_set_id) + ".txt", 'a',
                                       encoding='utf-8')
            segmented_data_file.write('\n'.join(segmented_data_buf[data_set_id]))
            segmented_data_buf[data_set_id] = []
            tagged_data_file = open("data/reordered/tagged/tagged_data_" + str(data_set_id) + ".txt", 'a',
                                    encoding='utf-8')
            tagged_data_file.write('\n'.join(tagged_data_buf[data_set_id]))
            tagged_data_buf[data_set_id] = []
            data_buf_len[data_set_id] = 0
