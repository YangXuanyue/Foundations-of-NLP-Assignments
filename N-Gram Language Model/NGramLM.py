from math import *

MAX_ASCII_VAL = 127


class NGramLM:
    def __init__(self, max_n, vocab_size):
        self.max_n = max_n
        self.vocab_size = vocab_size
        self.n_gram_cnt = [{} for n in range(self.max_n + 1)]
        self.vis_n_grams = [set() for n in range(self.max_n + 1)]
        # self.total_n_gram_cnt = [0] * (self.max_n + 1)
        self.pre_padding_words = ["S" + str(n) for n in range(1, self.max_n)]

    def get_cnt(self, n, n_gram):
        n_gram_str = ' '.join(n_gram)
        return self.n_gram_cnt[n][n_gram_str] \
            if n_gram_str in self.vis_n_grams[n] \
            else 0

    def get_prob(self, n, n_gram, smoothing_method, delta):
        if smoothing_method == "lidstone":
            return log(self.get_cnt(n, n_gram) + delta) \
                   - log(self.get_cnt(n - 1, n_gram[: n - 1]) + delta * self.vocab_size)
        elif smoothing_method == "good-turing":
            pass

    def add_n_gram(self, n, n_gram):
        n_gram_str = ' '.join(n_gram)
        if n_gram_str in self.vis_n_grams[n]:
            self.n_gram_cnt[n][n_gram_str] += 1
        else:
            self.vis_n_grams[n].add(n_gram_str)
            self.n_gram_cnt[n][n_gram_str] = 1

    def learn(self, data_type, training_data_set_ids):
        for data_set_id in training_data_set_ids:
            paras = open("data/" + data_type + "/data_" + str(data_set_id) + ".txt",
                         'r', encoding='utf-8').read().split('\n')
            for para in paras:
                words = self.pre_padding_words.copy()
                words.extend(para.split())
                for r in range(self.max_n - 1, len(words)):
                    for n in range(self.max_n + 1):
                        self.add_n_gram(n, words[r - n + 1: r + 1])

    def test(self, data_src, test_data_set_ids, delta):
        total_prob = [0.] * (self.max_n + 1)
        total_word_cnt = 0
        for data_set_id in test_data_set_ids:
            paras = open("data/" + data_src + "/data_" + str(data_set_id) + ".txt",
                         'r', encoding='utf-8').read().split('\n')
            for para in paras:
                para_prob = [0.] * (self.max_n + 1)
                words = self.pre_padding_words.copy()
                words.extend(para.split())
                for r in range(self.max_n - 1, len(words)):
                    total_word_cnt += 1
                    for n in range(1, self.max_n + 1):
                        print(words[r - n + 1: r + 1])
                        print(self.get_prob(n, words[r - n + 1: r + 1],
                                            smoothing_method="lidstone", delta=delta))
                        para_prob[n] += self.get_prob(n, words[r - n + 1: r + 1],
                                                      smoothing_method="lidstone", delta=delta)
                    print(para_prob)
                for n in range(1, self.max_n + 1):
                    total_prob[n] += para_prob[n]
        perplexity = [exp(-total_prob[n] / total_word_cnt) for n in range(self.max_n + 1)]
        for n in range(1, self.max_n + 1):
            print("perplexity of " + str(n) + "-gram = %f" % perplexity[n])
