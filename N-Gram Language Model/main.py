from gen_reordered_data import *
from get_word_num import *
from NGramLM import *
import matplotlib as mpl

DATA_SET_NUM = 10
TRAINING_DATA_PROPORTION = .9
data_type = "reordered"
MAX_N = 3

# gen_reordered_data(DATA_SET_NUM, text_level="article")
# gen_reordered_data(DATA_SET_NUM, text_level="paragraph")

training_data_set_ids = range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM))
test_data_set_ids = range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM), DATA_SET_NUM)
vocab_size = get_word_num(data_type, "paragraph", range(DATA_SET_NUM))

n_gram_lm = NGramLM(MAX_N, vocab_size)
n_gram_lm.train(data_type, "paragraph", training_data_set_ids)
# n_gram_lm.test(data_type, "paragraph", test_data_set_ids, 'katz')

for delta in [1, .005, .001, .0006, .0005, .0004, .0003, .0001, .00008, .00005]:
    print("delta = %f" % delta)
    n_gram_lm.test(data_type, "paragraph", test_data_set_ids, smoothing_method='lidstone', lidstone_delta=delta)
    print()

