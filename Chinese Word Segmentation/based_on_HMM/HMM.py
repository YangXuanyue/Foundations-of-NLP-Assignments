from codecs import open
from math import log
from gen_char_idx import *

MAX_ASCII_VAL = 127
MIN_LOG_VAL = -1e5


class HMM:
    def __init__(self, state_num, observation_num):
        self.state_num = state_num
        self.observation_num = observation_num
        self.start_prob = [0] * state_num
        self.transition_prob = [[0] * state_num for i in range(state_num)]
        self.transitable = [[False] * state_num for i in range(state_num)]
        self.emission_prob = [[0] * observation_num for i in range(state_num)]
        return

    def lidstone_smooth(self, prob, cnt, total_cnt, delta):
        for observation in range(self.observation_num):
            prob[observation] = log(cnt[observation] + delta) - log(total_cnt + delta * self.observation_num)

    def good_turing_smooth(self, prob, cnt, total_cnt):
        cnt_to_observations = {}
        for observation in range(self.observation_num):
            if cnt[observation] in cnt_to_observations.keys():
                cnt_to_observations[cnt[observation]].append(observation)
            else:
                cnt_to_observations[cnt[observation]] = [observation]
        cnt_to_observations = sorted(cnt_to_observations.items(), key=lambda pair: pair[0])
        total_prob = 0.
        for i in range(1, len(cnt_to_observations)):
            for observation in cnt_to_observations[i - 1][1]:
                prob[observation] = cnt_to_observations[i][0] \
                                    * len(cnt_to_observations[i][1]) \
                                    / len(cnt_to_observations[i - 1][1]) \
                                    / total_cnt
                total_prob += prob[observation]
        for observation in cnt_to_observations[len(cnt_to_observations) - 1][1]:
            # print(observation)
            prob[observation] = cnt[observation] / total_cnt
            total_prob += prob[observation]
        for observation in range(self.observation_num):
            # print(prob[observation])
            prob[observation] = log(prob[observation]) - log(total_prob)

    def supervised_learn(self, data_type, training_data_set_ids, delta):  # delta is for add-delta smoothing
        state_cnt = [0] * self.state_num
        total_state_cnt = 0
        transition_cnt = [[0] * self.state_num for i in range(self.state_num)]
        total_transition_cnt = [0] * self.state_num
        emission_cnt = [[0] * self.observation_num for i in range(self.state_num)]
        total_emission_cnt = [0] * self.state_num
        # observation_vis = [0] * self.observation_num
        # total_observation_cnt = 0

        for data_set_id in training_data_set_ids:
            tagged_data = open("../data/" + data_type + "/tagged/tagged_data_" + str(data_set_id) + ".txt",
                               'r', encoding='utf-8')
            for line in tagged_data:
                line = line.strip()
                cur_state = -1
                for char in line:
                    if ord(char) > MAX_ASCII_VAL:
                        observation = get_char_idx(char)
                        emission_cnt[cur_state][observation] += 1
                        total_emission_cnt[cur_state] += 1
                    else:
                        prv_state = cur_state
                        cur_state = int(char)
                        state_cnt[cur_state] += 1
                        total_state_cnt += 1
                        if prv_state != -1 and cur_state != -1:
                            transition_cnt[prv_state][cur_state] += 1
                            total_transition_cnt[prv_state] += 1
        for cur_state in range(self.state_num):
            self.start_prob[cur_state] = log(state_cnt[cur_state]) \
                                         - log(total_state_cnt)
            for nxt_state in range(self.state_num):
                if transition_cnt[cur_state][nxt_state] > 0:
                    self.transitable[cur_state][nxt_state] = True
                    self.transition_prob[cur_state][nxt_state] = log(transition_cnt[cur_state][nxt_state]) \
                                                                 - log(total_transition_cnt[cur_state])
            self.lidstone_smooth(self.emission_prob[cur_state],
                                 emission_cnt[cur_state],
                                 total_emission_cnt[cur_state],
                                 delta)

    def unsupervised_learn(self, training_data):
        pass

    def viterbi_decode(self, data_type, test_data_set_ids):
        for data_set_id in test_data_set_ids:
            test_data = open("../data/" + data_type + "/raw/raw_data_" + str(data_set_id) + ".txt",
                             'r', encoding='utf-8')
            segmented_result_file = open("../based_on_HMM/results/" + data_type + "/segmented/segmented_result_" + str(data_set_id)
                                         + ".txt", 'w+', encoding='utf-8')
            tagged_result_file = open("../based_on_HMM/results/" + data_type + "/tagged/tagged_result_" + str(data_set_id)
                                      + ".txt", 'w+', encoding='utf-8')
            for line in test_data:
                line = line.strip()
                if len(line) > 0:
                    observations = [get_char_idx(char) for char in line]
                    observations_len = len(observations)
                    max_prob = [[MIN_LOG_VAL] * self.state_num for t in range(observations_len)]
                    opt_prv_state = [[3] * self.state_num for t in range(observations_len)]
                    max_prob[0] = [self.start_prob[state]
                                   + self.emission_prob[state][observations[0]]
                                   for state in range(self.state_num)]
                    for t in range(1, observations_len):
                        for cur_state in range(self.state_num):
                            for prv_state in range(self.state_num):
                                if self.transitable[prv_state][cur_state]:
                                    tmp_prob = max_prob[t - 1][prv_state] \
                                               + self.transition_prob[prv_state][cur_state] \
                                               + self.emission_prob[cur_state][observations[t]]
                                    if tmp_prob > max_prob[t][cur_state]:
                                        max_prob[t][cur_state] = tmp_prob
                                        opt_prv_state[t][cur_state] = prv_state
                    results = []
                    final_max_prob = MIN_LOG_VAL
                    cur_state = 3
                    for state in range(self.state_num):
                        if max_prob[observations_len - 1][state] > final_max_prob:
                            final_max_prob = max_prob[observations_len - 1][state]
                            cur_state = state
                    # cur_state = SINGLE  # given that the last word in the sentence is a single deliminator
                    for t in range(observations_len - 1, -1, -1):
                        results.append(cur_state)
                        cur_state = opt_prv_state[t][cur_state]
                    results.reverse()
                    for t in range(observations_len):
                        segmented_result_file.write(line[t])
                        if results[t] in [2, 3]:
                            segmented_result_file.write(' ')
                        tagged_result_file.write(str(results[t]) + line[t])
                segmented_result_file.write('\n')
                tagged_result_file.write('\n')
