from math import *
import matplotlib.pyplot as plt

MAX_ASCII_VAL = 127


class NGramLM:
    def __init__(self, max_n, vocab_size):
        self.max_n = max_n
        self.vocab_size = vocab_size
        self.pre_padding_words = ["S" + str(n) for n in range(1, self.max_n)]
        self.n_gram_cnt = [{} for n in range(self.max_n + 1)]
        self.vis_n_grams = [set() for n in range(self.max_n + 1)]
        self.vis_n_gram_cnts = [set() for n in range(self.max_n + 1)]
        self.cnt_to_n_grams = [{} for n in range(self.max_n + 1)]
        # self.vis_n_gram_probs = [{} for n in range(self.max_n + 1)]
        self.n_gram_katz_prob = [{} for n in range(self.max_n + 1)]
        self.max_cnt_for_katz_d = 5
        self.katz_d = [[0] * (self.max_cnt_for_katz_d + 1) for n in range(self.max_n + 1)]
        self.katz_alpha = [{} for n in range(self.max_n)]

    def get_cnt(self, n, n_gram):
        n_gram_str = " ".join(n_gram)
        return self.n_gram_cnt[n][n_gram_str] if n_gram_str in self.vis_n_grams[n] else 0

    def get_katz_d(self, n, cnt):
        return 1 if cnt > self.max_cnt_for_katz_d else self.katz_d[n][cnt]

    def get_katz_alpha(self, n, n_gram):
        n_gram_str = " ".join(n_gram)
        return self.katz_alpha[n][n_gram_str] if n_gram_str in self.vis_n_grams[n] else 1.

    '''def get_katz_cnt(self, n, n_gram):
        cnt = self.get_cnt(n, n_gram)
        return self.get_katz_d(cnt) * cnt if cnt > 0 \
            else self.katz_alpha[n - 1][" ".join(n_gram[: -1])] * self.get_prob(1, n_gram[-1], 'lidstone')'''

    def get_prob(self, n, n_gram, smoothing_method, delta=4e-4):
        if smoothing_method == 'lidstone':
            return (self.get_cnt(n, n_gram) + delta) \
                   / (self.get_cnt(n - 1, n_gram[: -1]) + delta * self.vocab_size)
        elif smoothing_method == 'katz':
            if n == 1:
                return self.get_prob(n, n_gram, 'lidstone')
            n_gram_str = " ".join(n_gram)
            prob = self.n_gram_katz_prob[n][n_gram_str] if n_gram_str in self.vis_n_grams[n] \
                else self.get_katz_alpha(n - 1, n_gram[: -1]) * self.get_prob(n - 1, n_gram[1:], 'katz')
            if prob == 0.:
                print(self.get_katz_alpha(n - 1, n_gram[: -1]))
            return prob

    def add_n_gram(self, n, n_gram):
        n_gram_str = " ".join(n_gram)
        if n_gram_str in self.vis_n_grams[n]:
            self.n_gram_cnt[n][n_gram_str] += 1
        else:
            self.vis_n_grams[n].add(n_gram_str)
            self.n_gram_cnt[n][n_gram_str] = 1

    def add_n_gram_cnt(self, n, n_gram_str):
        cnt = self.n_gram_cnt[n][n_gram_str]
        if cnt in self.vis_n_gram_cnts[n]:
            self.cnt_to_n_grams[n][cnt].append(n_gram_str)
        else:
            self.vis_n_gram_cnts[n].add(cnt)
            self.cnt_to_n_grams[n][cnt] = [n_gram_str]

    def train(self, data_type, text_level, training_data_set_ids):
        for data_set_id in training_data_set_ids:
            paras = open("data/" + data_type + "/" + text_level + "_level/data_" + str(data_set_id) + ".txt",
                         'r', encoding='utf-8').read().split('\n')
            for para in paras:
                words = self.pre_padding_words.copy()
                words.extend(para.split())
                '''for n in range(1, self.max_n):
                    self.add_n_gram(n , self.pre_padding_words[self.max_n - 1 - n:])'''
                for n in range(self.max_n + 1):
                    for r in range(n - 1, len(words)):
                        # for n in range(self.max_n + 1):
                        self.add_n_gram(n, words[r - n + 1: r + 1])
        katz_prob_sum = [{} for n in range(self.max_n + 1)]
        backoff_katz_prob_sum = [{} for n in range(self.max_n + 1)]
        for n in range(1, self.max_n + 1):
            for n_gram_str in self.vis_n_grams[n]:
                self.add_n_gram_cnt(n, n_gram_str)
            for cnt in range(1, self.max_cnt_for_katz_d + 1):
                good_turing_cnt = (cnt + 1) * \
                                  len(self.cnt_to_n_grams[n][cnt + 1]) \
                                  / len(self.cnt_to_n_grams[n][cnt])
                t = (self.max_cnt_for_katz_d + 1.) \
                    * len(self.cnt_to_n_grams[n][self.max_cnt_for_katz_d + 1.]) \
                    / len(self.cnt_to_n_grams[n][1])
                self.katz_d[n][cnt] = ((good_turing_cnt / cnt) - t) / (1. - t)
            for n_gram_str in self.vis_n_grams[n]:
                katz_prob_sum[n][n_gram_str] = 0.
                backoff_katz_prob_sum[n][n_gram_str] = 0.
                cnt = self.n_gram_cnt[n][n_gram_str]
                self.n_gram_katz_prob[n][n_gram_str] = self.get_katz_d(n, cnt) \
                                                       * cnt \
                                                       / self.get_cnt(n - 1, n_gram_str.split(" ")[: -1]) if n > 1 \
                    else self.get_prob(n, n_gram_str.split(" "), 'lidstone')
                if n > 1:
                    katz_prob_sum[n - 1][" ".join(n_gram_str.split(" ")[: -1])] \
                        += self.n_gram_katz_prob[n][n_gram_str]
                    backoff_katz_prob_sum[n - 1][" ".join(n_gram_str.split(" ")[: -1])] \
                        += self.n_gram_katz_prob[n - 1][" ".join(n_gram_str.split(" ")[1:])]
            if n > 1:
                for n_gram_str in self.vis_n_grams[n - 1]:
                    backoff_katz_prob_sum[n - 1][n_gram_str] = min(backoff_katz_prob_sum[n - 1][n_gram_str], .95)
                    katz_prob_sum[n - 1][n_gram_str] = min(katz_prob_sum[n - 1][n_gram_str], .95)
                    self.katz_alpha[n - 1][n_gram_str] = (1. - katz_prob_sum[n - 1][n_gram_str]) \
                                                         / (1. - backoff_katz_prob_sum[n - 1][n_gram_str])

    def test(self, data_type, text_level, test_data_set_ids, smoothing_method, lidstone_delta=4e-4):
        for data_set_id in test_data_set_ids:
            total_prob = [0.] * (self.max_n + 1)
            total_word_cnt = 0
            sentences = open("data/" + data_type + "/" + text_level + "_level/data_" + str(data_set_id) + ".txt",
                             'r', encoding='utf-8').read().split('\n')
            for sentence in sentences:
                sentence_prob = [0.] * (self.max_n + 1)
                for n in range(1, self.max_n + 1):
                    sentence_prob[n] = \
                        log(self.n_gram_cnt[n - 1][" ".join(self.pre_padding_words[self.max_n - n:])]) \
                        - log(len(self.vis_n_grams[n - 1]))
                words = self.pre_padding_words.copy()
                words.extend(sentence.split())
                for r in range(self.max_n - 1, len(words)):
                    total_word_cnt += 1
                    for n in range(1, self.max_n + 1):
                        sentence_prob[n] += log(self.get_prob(n, words[r - n + 1: r + 1],
                                                              smoothing_method=smoothing_method,
                                                              delta=lidstone_delta))
                for n in range(1, self.max_n + 1):
                    total_prob[n] += sentence_prob[n]
            perplexity = [exp(-total_prob[n] / total_word_cnt) for n in range(self.max_n + 1)]
            print("result of test_data_set %d:" % data_set_id)
            for n in range(1, self.max_n + 1):
                print("\tperplexity of " + str(n) + "-gram = %f" % perplexity[n])
            print()
