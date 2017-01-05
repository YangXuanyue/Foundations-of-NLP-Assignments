import numpy as np
import re
import time


class DataHelper:
    def __init__(self, pos_data_file, neg_data_file, training_data_proportion):
        pos_sents = list(open(pos_data_file, 'r', encoding='utf-8').readlines())
        pos_sents = [self.clean_str(sent.strip()) for sent in pos_sents]
        neg_sents = list(open(neg_data_file, 'r', encoding='utf-8').readlines())
        neg_sents = [self.clean_str(sent.strip()) for sent in neg_sents]
        sents = pos_sents + neg_sents
        self.vocab = set()
        self.word_to_idx = {}
        cur_idx = 0
        self.max_sent_len = 0
        for sent in sents:
            words = sent.split(' ')
            self.max_sent_len = max(self.max_sent_len, len(words))
            for word in words:
                if word not in self.vocab:
                    self.vocab.add(word)
                    self.word_to_idx[word] = cur_idx
                    cur_idx += 1
        padding_word = '#'
        assert(padding_word not in self.vocab)
        self.vocab.add(padding_word)
        self.word_to_idx[padding_word] = cur_idx
        self.vocab_size = len(self.vocab)
        self.sents = np.array(
            [
                [
                    cur_idx for j in range(self.max_sent_len)
                ] for i in range(len(sents))
            ]
        )
        for i, sent in enumerate(sents):
            for j, word in enumerate(sent.split(' ')):
                self.sents[i][j] = self.word_to_idx[word]

        pos_categories = [[0., 1.] for sent in pos_sents]
        neg_categories = [[1., 0.] for sent in neg_sents]
        self.categories = np.concatenate([pos_categories, neg_categories], 0)

        np.random.seed(np.uint32(time.time()))
        shuffled_idxes = np.random.permutation(np.arange(len(self.sents)))
        self.sents = self.sents[shuffled_idxes]
        self.categories = self.categories[shuffled_idxes]
        training_data_idx = int(training_data_proportion * float(len(self.sents)))
        self.training_sents, self.validation_sents = \
            self.sents[: training_data_idx], self.sents[training_data_idx:]
        self.training_categories, self.validation_categories = \
            self.categories[: training_data_idx], self.categories[training_data_idx:]

    @staticmethod
    def clean_str(sent):
        sent = re.sub(r"[^A-Za-z0-9(),!?\'`]", " ", sent)
        sent = re.sub(r"\'s", " \'s", sent)
        sent = re.sub(r"\'ve", " \'ve", sent)
        sent = re.sub(r"n\'t", " n\'t", sent)
        sent = re.sub(r"\'re", " \'re", sent)
        sent = re.sub(r"\'d", " \'d", sent)
        sent = re.sub(r"\'ll", " \'ll", sent)
        sent = re.sub(r",", " , ", sent)
        sent = re.sub(r"!", " ! ", sent)
        sent = re.sub(r"\(", " \( ", sent)
        sent = re.sub(r"\)", " \) ", sent)
        sent = re.sub(r"\?", " \? ", sent)
        sent = re.sub(r"\s{2,}", " ", sent)
        return sent.strip().lower()

    def gen_batches(self, batch_size, epoch_num, shuffle=True):
        data = np.array(
            list(
                zip(self.training_sents, self.training_categories)
            )
        )
        data_size = len(data)
        batch_num_per_epoch = int(len(data) / batch_size) + 1
        for epoch in range(epoch_num):
            if shuffle:
                shuffled_idxes = np.random.permutation(np.arange(data_size))
                shuffled_data = data[shuffled_idxes]
            else:
                shuffled_data = data
            for batch_idx in range(batch_num_per_epoch):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, data_size)
                yield zip(*shuffled_data[start_idx: end_idx])
