from based_on_HMM.HMM import *
from evaluate_result import *
from gen_char_idx import *

DATA_SET_NUM = 10
TRAINING_DATA_PROPORTION = .8

STATE_NUM = 4  # BEGIN, MIDDLE, END, SINGLE
# MAX_UTF8_VAL = 65535

# gen_reordered_data(DATA_SET_NUM)
# gen_ordered_data()

'''
delta f
.1    81.2853%
.099  81.2855%
'''

observation_num = load_char_idx()

data_src = "based_on_HMM"
data_type = "reordered"
training_data_set_ids = [i for i in range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM))]
test_data_set_ids = [i for i in range(int(TRAINING_DATA_PROPORTION * DATA_SET_NUM), DATA_SET_NUM)]

hmm = HMM(STATE_NUM, observation_num)
hmm.supervised_learn(data_type, training_data_set_ids, delta=.099)
hmm.viterbi_decode(data_type, test_data_set_ids)

evaluate_result(data_src, data_type, test_data_set_ids)
