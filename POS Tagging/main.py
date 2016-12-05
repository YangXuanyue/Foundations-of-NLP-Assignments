from gen_reordered_data import *
from gen_word_and_tag_idx import *
from HMM import *
from evaluate_result import *

DATA_SET_NUM = 10
TRAINING_DATA_PROPORTION = .8
training_data_set_ids = range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM))
test_data_set_ids = range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM), DATA_SET_NUM)

# gen_reordered_data(DATA_SET_NUM)
word_num, tag_num = load_word_and_tag_idx()
hmm = HMM(state_num=tag_num, observation_num=word_num)
hmm.supervised_learn(training_data_set_ids, delta=.1)
hmm.viterbi_decode(test_data_set_ids)
evaluate_result(test_data_set_ids)

# 92.3718%
