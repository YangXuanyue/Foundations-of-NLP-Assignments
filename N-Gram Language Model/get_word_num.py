def get_word_num(data_type, text_level, training_data_set_ids):
    vis_words = set()
    word_num = 0
    for data_set_id in training_data_set_ids:
        words = open("data/" + data_type + "/" + text_level + "_level/data_" + str(data_set_id) + ".txt",
                     'r', encoding='utf-8').read().split()
        for word in words:
            if word not in vis_words:
                vis_words.add(word)
                word_num += 1
    return word_num

