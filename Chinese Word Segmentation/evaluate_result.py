def evaluate_result(data_src, data_type, test_data_set_ids):
    correct_word_cnt = 0
    total_stand_word_cnt = 0
    total_result_word_cnt = 0
    for data_set_id in test_data_set_ids:
        stand_data = open("../data/" + data_type + "/segmented/segmented_data_" + str(data_set_id) + ".txt",
                          'r', encoding='utf-8').read().split()
        result_data = open("../" + data_src + "/results/" + data_type + "/segmented/segmented_result_" + str(data_set_id) + ".txt",
                           'r', encoding='utf-8').read().split()
        diff_data = open("../" + data_src + "/results/" + data_type + "/different/different_result_" + str(data_set_id) + ".txt",
                         'w+', encoding='utf-8')
        stand_data_len = len(stand_data)
        result_data_len = len(result_data)
        total_stand_word_cnt += stand_data_len
        total_result_word_cnt += result_data_len
        i = 0
        j = 0
        stand_data_buf = []
        result_data_buf = []
        while i < stand_data_len and j < result_data_len:
            if stand_data[i] == result_data[j]:
                correct_word_cnt += 1
                i += 1
                j += 1
            else:
                stand_char_cnt = len(stand_data[i])
                stand_data_buf.append(stand_data[i])
                i += 1
                result_char_cnt = len(result_data[j])
                result_data_buf.append(result_data[j])
                j += 1
                while i < stand_data_len and j < result_data_len and stand_char_cnt != result_char_cnt:
                    if stand_char_cnt < result_char_cnt:
                        stand_char_cnt += len(stand_data[i])
                        stand_data_buf.append(stand_data[i])
                        i += 1
                    else:
                        result_char_cnt += len(result_data[j])
                        result_data_buf.append(result_data[j])
                        j += 1
                diff_data.write(' '.join(stand_data_buf)
                                + '\n'
                                + ' '.join(result_data_buf)
                                + '\n')
                stand_data_buf = []
                result_data_buf = []
    print("correct_word_cnt = %d\n"
          "total_stand_word_cnt = %d\n"
          "total_result_word_cnt = %d\n"
          % (correct_word_cnt, total_stand_word_cnt, total_result_word_cnt))
    precision = correct_word_cnt / total_result_word_cnt
    recall = correct_word_cnt / total_stand_word_cnt
    f = 2 * precision * recall / (precision + recall)
    print("precision = %.4f%%\n"
          "recall = %.4f%%\n"
          "f = %.4f%%"
          % (precision * 100, recall * 100, f * 100))

