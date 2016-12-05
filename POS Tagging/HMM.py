from codecs import open
from math import log
from gen_word_and_tag_idx import *

MAX_ASCII_VAL = 127
MIN_LOG_VAL = -1e5


class HMM:
    def __init__(self, state_num, observation_num):
        self.state_num = state_num
        self.observation_num = observation_num
        self.start_prob = [0] * state_num
        self.transition_prob = [[0] * state_num for i in range(state_num)]
        self.transitable_prv_states = [set() for i in range(state_num)]
        self.emission_prob = [[0] * observation_num for i in range(state_num)]
        return

    @staticmethod
    def lidstone_smooth(prob, cnt, total_cnt, size, delta=.001):
        for i in range(size):
            prob[i] = log(cnt[i] + delta) - log(total_cnt + delta * size)

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

    def supervised_learn(self, training_data_set_ids, delta):  # delta is for add-delta smoothing
        state_cnt = [0] * self.state_num
        total_state_cnt = 0
        transition_cnt = [[0] * self.state_num for i in range(self.state_num)]
        total_transition_cnt = [0] * self.state_num
        emission_cnt = [[0] * self.observation_num for i in range(self.state_num)]
        total_emission_cnt = [0] * self.state_num
        # observation_vis = [0] * self.observation_num
        # total_observation_cnt = 0

        for data_set_id in training_data_set_ids:
            tagged_data = open("data/tagged/data_" + str(data_set_id) + ".txt",
                               'r', encoding='utf-8')
            for line in tagged_data:
                cur_sequence = line.strip().split(' ')
                cur_state = -1
                for word_and_tag in cur_sequence:
                    word = ""
                    tag = ""
                    for char in word_and_tag:
                        if ord(char) > MAX_ASCII_VAL:
                            word += char
                        else:
                            tag += char
                    prv_state = cur_state
                    cur_state = tag_to_idx[tag]
                    cur_observation = word_to_idx[word]
                    emission_cnt[cur_state][cur_observation] += 1
                    total_emission_cnt[cur_state] += 1
                    state_cnt[cur_state] += 1
                    total_state_cnt += 1
                    if prv_state != -1 and cur_state != -1:
                        transition_cnt[prv_state][cur_state] += 1
                        total_transition_cnt[prv_state] += 1
        self.lidstone_smooth(self.start_prob,
                             state_cnt,
                             total_state_cnt,
                             self.state_num)
        for cur_state in range(self.state_num):
            for nxt_state in range(self.state_num):
                if transition_cnt[cur_state][nxt_state] > 0:
                    self.transitable_prv_states[nxt_state].add(cur_state)
                    self.transition_prob[cur_state][nxt_state] = log(transition_cnt[cur_state][nxt_state]) \
                                                                 - log(total_transition_cnt[cur_state])
            self.lidstone_smooth(self.emission_prob[cur_state],
                                 emission_cnt[cur_state],
                                 total_emission_cnt[cur_state],
                                 self.observation_num,
                                 delta)

    def unsupervised_learn(self, training_data):
        pass

    def viterbi_decode(self, test_data_set_ids):
        for data_set_id in test_data_set_ids:
            test_data = open("data/segmented/data_" + str(data_set_id) + ".txt",
                             'r', encoding='utf-8')
            result_file = open("results/result_" + str(data_set_id)
                               + ".txt", 'w+', encoding='utf-8')
            for line in test_data:
                sequence = line.strip().split(' ')
                if len(sequence) > 0:
                    observations = [word_to_idx[word] for word in sequence]
                    observations_len = len(observations)
                    max_prob = [[MIN_LOG_VAL] * self.state_num for t in range(observations_len)]
                    opt_prv_state = [[3] * self.state_num for t in range(observations_len)]
                    max_prob[0] = [self.start_prob[state]
                                   + self.emission_prob[state][observations[0]]
                                   for state in range(self.state_num)]
                    for t in range(1, observations_len):
                        for cur_state in range(self.state_num):
                            for prv_state in self.transitable_prv_states[cur_state]:
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
                        results.append(tags[cur_state])
                        cur_state = opt_prv_state[t][cur_state]
                    results.reverse()
                    print(' '.join(map(lambda observation, state: observation + state,
                                       sequence, results)),
                          file=result_file)

