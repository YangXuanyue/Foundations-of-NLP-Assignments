from get_word_num import *

MAX_ASCII_VAL = 127
UNI = 1
BI = 2
TRI = 3


class NGramLM:
    def cal_prob(self, n, smoothing_method="lidstone", delta=.1):
        if smoothing_method == "lidstone":
            for n_gram, cnt in self.n_gram_cnt[n].items():
                self.n_gram_prob[n_gram] = (cnt + delta) \
                                           / (self.total_n_gram_cnt[n] + delta * self.n_gram_num[n])
        elif smoothing_method == "good-turing":
            pass

    def __init__(self, max_n, word_num):
        self.max_n = max_n
        self.word_num = word_num
        self.n_gram_num = [1] * (self.max_n + 1)
        for n in range(1, self.max_n + 1):
            self.n_gram_num[n] = self.word_num * self.n_gram_num[n - 1]
        self.n_gram_cnt = [{} for n in range(1, self.max_n + 1)]
        self.total_n_gram_cnt = [] * (self.max_n + 1)
        self.n_gram_prob = [{} for n in range(1, self.max_n + 1)]
        self.prf_words = ["S" + str(n) for n in range(1, self.max_n)]

    def add_n_gram(self, n, n_gram):
        self.total_n_gram_cnt[n] += 1
        if n_gram in self.n_gram_cnt[n].keys():
            self.n_gram_cnt[n][n_gram] += 1
        else:
            self.n_gram_cnt[n][n_gram] = 0

    def get_prob(self, n, n_gram):
        pass

    def learn(self, data_src, training_data_set_ids, delta):
        for data_set_id in training_data_set_ids:
            training_data = open("data\\" + data_src + "\\data_" + str(data_set_id) + ".txt",
                                 'r', encoding='utf-8').read().split('\n')
            for line in training_data:
                words = self.prf_words
                words.extend(line.split())
                for r in range(self.max_n - 1, len(words)):
                    for n in range(1, self.max_n + 1):
                        l_n = r - n + 1
                        self.add_n_gram(n, words[l_n:r])
        for n in range(1, self.max_n + 1):
            self.cal_prob(n, "lidstone", delta)

    def test(self, data_src, test_data_set_ids):
        perplexity = [] * (self.max_n + 1)
        for data_set_id in test_data_set_ids:
            test_data = open("data\\" + data_src + "\\data_" + str(data_set_id) + ".txt",
                             'r', encoding='utf-8').read().split('\n')
            for line in test_data:
                words = self.prf_words
                words.extend(line.split())

