from based_on_BM.Trie import *

forward_dictionary = Trie()
backward_dictionary = Trie()


def gen_dictionary(data_type, training_data_set_ids):
    out_file = open("../data/dictionary.txt", 'w+', encoding='utf-8')
    for data_set_id in training_data_set_ids:
        words = open("../data/" + data_type + "/segmented/segmented_data_" + str(data_set_id) + ".txt",
                     'r', encoding='utf-8').read().split()
        for word in words:
            if not forward_dictionary.match(word) < len(word):
                forward_dictionary.insert(word)
                backward_dictionary.insert(word[:: -1])
                out_file.write(word + '\n')


def load_dictionary():
    words = open("../data/dictionary.txt", 'r', encoding='utf-8')
    for word in words:
        word = word.strip()
        if len(word) > 0:
            forward_dictionary.insert(word)
            backward_dictionary.insert(word[:: -1])
