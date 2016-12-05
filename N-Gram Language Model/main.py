from gen_reordered_data import *
from get_word_num import *
from NGramLM import *
import matplotlib as mpl

DATA_SET_NUM = 10
TRAINING_DATA_PROPORTION = .8
data_type = "reordered"
MAX_N = 3

# gen_reordered_data(DATA_SET_NUM, text_level="article")
# gen_reordered_data(DATA_SET_NUM, text_level="paragraph")

training_data_set_ids = range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM))
word_num = get_word_num(data_type, "paragraph", training_data_set_ids)
alpha = 1.1  # suppose that the vocabulary size is alpha times the word_num of the training data sets
vocab_size = alpha * word_num

n_gram_lm = NGramLM(MAX_N, vocab_size)
n_gram_lm.learn(data_type, "paragraph", training_data_set_ids)
for delta in [.1, .01, .005, .001, .0005, .0001, .00005]:
    print("delta = %f" % delta)
    n_gram_lm.test(data_type, "paragraph", range(8, DATA_SET_NUM), delta=delta)
    print()


