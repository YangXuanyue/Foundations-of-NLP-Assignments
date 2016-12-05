DATA_SET_NUM = 10
MAX_ASCII_VAL = 127

vis_words = set()
words = []
word_to_idx = {}
vis_tags = set()
tags = []
tag_to_idx = {}


def gen_word_and_tag_idx():
    word_num = 0
    tag_num = 0
    words_file = open("data/words.txt", 'w+', encoding='utf-8')
    tags_file = open("data/tags.txt", 'w+', encoding='utf-8')
    for data_set_id in range(DATA_SET_NUM):
        word_and_tags = open("data/tagged/data_" + str(data_set_id) + ".txt",
                             'r', encoding='utf-8').read().split()
        for word_and_tag in word_and_tags:
            word = ""
            tag = ""
            for char in word_and_tag:
                if ord(char) > MAX_ASCII_VAL:
                    word += char
                else:
                    tag += char
            if word not in vis_words:
                vis_words.add(word)
                word_to_idx[word] = word_num
                print(word, file=words_file)
                word_num += 1
            if tag not in vis_tags:
                vis_tags.add(tag)
                tag_to_idx[tag] = tag_num
                print(tag, file=tags_file)
                tag_num += 1


def load_word_and_tag_idx():
    word_num = 0
    tag_num = 0
    words_file = open("data/words.txt", 'r', encoding='utf-8')
    tags_file = open("data/tags.txt", 'r', encoding='utf-8')
    for word in words_file.read().split('\n'):
        words.append(word)
        word_to_idx[word] = word_num
        word_num += 1
    for tag in tags_file.read().split('\n'):
        tags.append(tag)
        tag_to_idx[tag] = tag_num
        tag_num += 1
    return word_num, tag_num

gen_word_and_tag_idx()