import tensorflow as tf
import numpy as np

class TextCNN:
    def __init__(self,
                 sentence_len,
                 class_num,
                 vocab_size,
                 emb_dim,
                 filter_sizes,
                 filter_num):
        self.input_sentences = tf.placeholder(tf.int32, [None, sentence_len])
        self.input_classes = tf.placeholder(tf.float32, [None, class_num])
        self.dropout_keep_prob = tf.placeholder(tf.float32)



