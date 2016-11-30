from gen_reordered_data import *
from get_word_num import *
from NGramLM import *

DATA_SET_NUM = 10
TRAINING_DATA_PROPORTION = .8
data_src = "reordered"
MAX_N = 3

gen_reordered_data(DATA_SET_NUM)

word_num = get_word_num(data_src, DATA_SET_NUM)

training_data_set_ids = [id for id in range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM))]

n_gram_lm = NGramLM(MAX_N, word_num)
n_gram_lm.learn(data_src, training_data_set_ids, delta=.1)
