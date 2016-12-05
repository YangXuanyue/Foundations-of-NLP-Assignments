MAX_ASCII_VAL = 127


def evaluate_result(test_data_set_ids):
    total_word_cnt = 0
    correct_tag_cnt = 0
    for data_set_id in test_data_set_ids:
        standard_word_and_tags = open("data/tagged/data_" + str(data_set_id) + ".txt",
                                      'r', encoding='utf-8').read().split()
        result_word_and_tags = open("results/result_" + str(data_set_id) + ".txt",
                                    'r', encoding='utf-8').read().split()
        diff_file = open("results/difference_" + str(data_set_id) + ".txt",
                         'w+', encoding='utf-8')
        for standard_word_and_tag, result_word_and_tag in zip(standard_word_and_tags, result_word_and_tags):
            total_word_cnt += 1
            standard_word = ""
            standard_tag = ""
            result_word = ""
            result_tag = ""
            for char in standard_word_and_tag:
                if ord(char) > MAX_ASCII_VAL:
                    standard_word += char
                else:
                    standard_tag += char
            for char in result_word_and_tag:
                if ord(char) > MAX_ASCII_VAL:
                    result_word += char
                else:
                    result_tag += char
            assert(standard_word == result_word)
            if standard_tag == result_tag:
                correct_tag_cnt += 1
            else:
                print(standard_word_and_tag, result_word_and_tag, file=diff_file)
    print("%f%%" % (correct_tag_cnt * 100 / total_word_cnt))
