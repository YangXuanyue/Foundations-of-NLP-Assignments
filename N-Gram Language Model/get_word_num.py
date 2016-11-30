def get_word_num(data_src, data_set_num):
    word_to_idx = {}
    cur_idx = 0
    for data_set_id in range(data_set_num):
        words = open("data\\" + data_src + "\\data_" + str(data_set_id) + ".txt",
                     'r', encoding='utf-8').read().split()
        for word in words:
            if word not in word_to_idx.keys():
                word_to_idx[word] = cur_idx
                cur_idx += 1
    return cur_idx

