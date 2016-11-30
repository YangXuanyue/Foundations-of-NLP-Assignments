from codecs import open

MAX_ASCII_VAL = 127
MAX_UTF8_VAL = 65535

char_ord_to_idx = [-1] * (MAX_UTF8_VAL + 1)
char_idx_to_ord = []


def gen_char_idx():
    in_file = open("../data/1998-01-105-带音.txt", 'r', encoding='gbk')
    out_file = open("../data/char_idx.txt", 'w+', encoding='utf-8')
    cur_idx = 0
    for line in in_file:
        line = line.strip()
        for char in line:
            if ord(char) > MAX_ASCII_VAL:
                if char_ord_to_idx[ord(char)] == -1:
                    char_ord_to_idx[ord(char)] = cur_idx
                    out_file.write(char + ' ' + str(cur_idx) + '\n')
                    cur_idx += 1
    return cur_idx


def load_char_idx():
    in_file = open("../data/char_idx.txt", 'r', encoding='utf-8').read()
    char_num = 0
    for line in in_file.split('\n'):
        char_and_idx = line.split(' ')
        char_ord_to_idx[ord(char_and_idx[0])] = int(char_and_idx[1])
        char_num += 1
    return char_num


def get_char_idx(char):
    return char_ord_to_idx[ord(char)]
