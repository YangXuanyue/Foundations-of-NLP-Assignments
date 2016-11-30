from gen_dictionary import *
from evaluate_result import *

DATA_SET_NUM = 10
TRAINING_DATA_PROPORTION = .8
data_src = "based_on_BM"
data_type = "reordered"
test_data_set_ids = range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM), DATA_SET_NUM)

FORWARD = 0
BACKWARD = 1


def max_match(direction, sentence):
    if direction == BACKWARD:
        sentence = sentence[:: -1]
    in_dictionary_word_cnt = 0
    segmented_sentence = []
    i = 0
    sentence_len = len(sentence)
    dictionary = forward_dictionary \
        if direction == FORWARD \
        else backward_dictionary
    while i < sentence_len:
        max_match_len = dictionary.match(sentence[i:])
        if max_match_len > 0:
            segmented_sentence.append(sentence[i: i + max_match_len])
            i += max_match_len
            in_dictionary_word_cnt += 1
        else:
            segmented_sentence.append(sentence[i])
            i += 1
    if direction == BACKWARD:
        segmented_sentence_tmp = segmented_sentence[:: -1]
        segmented_sentence = []
        for word in segmented_sentence_tmp:
            segmented_sentence.append(word[:: -1])
    return segmented_sentence, in_dictionary_word_cnt


load_dictionary()

for data_set_id in test_data_set_ids:
    sentences = open("../data/" + data_type + "/raw/raw_data_" + str(data_set_id) + ".txt",
                     'r', encoding='utf-8').read().split('\n')
    result_file = open("../based_on_BM/results/" + data_type + "/segmented/segmented_result_" + str(data_set_id)
                       + ".txt", 'w+', encoding='utf-8')
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 0:
            segmented_sentence_f, in_dictionary_word_cnt_f = max_match(FORWARD, sentence)
            segmented_sentence_b, in_dictionary_word_cnt_b = max_match(BACKWARD, sentence)
            segmented_sentence = segmented_sentence_f \
                if (False
                    or len(segmented_sentence_f) < len(segmented_sentence_b)
                    or (len(segmented_sentence_f) == len(segmented_sentence_b)
                        and in_dictionary_word_cnt_f > in_dictionary_word_cnt_b)) \
                else segmented_sentence_b
            result_file.write(' '.join(segmented_sentence) + '\n')

print("precision = %.4f%%\n"
      "recall = %.4f%%\n"
      "f = %.4f%%"
      % (evaluate_result(data_src, data_type, test_data_set_ids)))

# 92.1624
