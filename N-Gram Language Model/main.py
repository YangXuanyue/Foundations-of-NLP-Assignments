from gen_reordered_data import *
from get_word_num import *
from NGramLM import *

DATA_SET_NUM = 10
TRAINING_DATA_PROPORTION = .8
data_type = "reordered"
MAX_N = 3

# gen_reordered_data(DATA_SET_NUM)
training_data_set_ids = [id for id in range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM))]
test_data_set_ids = [id for id in range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM) + 1, DATA_SET_NUM)]
word_num = get_word_num(data_type, training_data_set_ids)
alpha = 1.1 # suppose that the vocabulary size is alpha times the word_num of the training data sets
vocab_size = alpha * word_num

n_gram_lm = NGramLM(MAX_N, vocab_size)
n_gram_lm.learn(data_type, training_data_set_ids)
n_gram_lm.test(data_type, test_data_set_ids, delta=.001)
