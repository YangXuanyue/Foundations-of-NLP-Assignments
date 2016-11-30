from codecs import open

MAX_WORD_NUM_PER_FILE = 111500
MAX_ASCII_VAL = 127


def gen_ordered_data():
    data_set_id = 0

    in_file = open("data/1998-01-105-带音.txt", 'r', encoding='gbk')
    raw_data_file = open("data/ordered/raw/raw_data_" + str(data_set_id) + ".txt", 'w+', encoding='utf-8')
    segmented_data_file = open("data/ordered/segmented/segmented_data_" + str(data_set_id) + ".txt",
                               'w+', encoding='utf-8')
    tagged_data_file = open("data/ordered/tagged/tagged_data_" + str(data_set_id) + ".txt", 'w+', encoding='utf-8')

    cur_word = []
    word_cnt = 0

    for line in in_file:
        line = line.strip()
        if len(line) > 0:
            for char in line:
                if ord(char) > MAX_ASCII_VAL:
                    cur_word.append(char)
                else:
                    if len(cur_word) > 0:
                        word_cnt += 1
                        raw_data_file.write(''.join(cur_word))
                        segmented_data_file.write(''.join(cur_word))
                        segmented_data_file.write(' ')
                        if len(cur_word) == 1:
                            tagged_data_file.write('3' + cur_word[0])
                        else:
                            word_len = len(cur_word)
                            tagged_data_file.write('0' + cur_word[0])
                            for i in range(1, word_len - 1):
                                tagged_data_file.write('1' + cur_word[i])
                            tagged_data_file.write('2' + cur_word[word_len - 1])
                        cur_word = []
        else:
            raw_data_file.write('\n')
            segmented_data_file.write('\n')
            tagged_data_file.write('\n')
            if word_cnt >= MAX_WORD_NUM_PER_FILE:
                data_set_id += 1
                raw_data_file.close()
                tagged_data_file.close()
                raw_data_file = open("data/ordered/raw/raw_data_" + str(data_set_id) + ".txt",
                                     'w+', encoding='utf-8')
                segmented_data_file = open("data/ordered/segmented/segmented_data_" + str(data_set_id) + ".txt",
                                           'w+', encoding='utf-8')
                tagged_data_file = open("data/ordered/tagged/tagged_data_" + str(data_set_id) + ".txt",
                                        'w+', encoding='utf-8')
                word_cnt = 0
