import tensorflow as tf


class TextCNN:
    def __init__(
            self,
            sentence_len,
            category_num,  # len(["positive", "negative"])
            vocabulary_size,
            embedding_dim,
            filter_widths,
            filter_num
    ):
        # input placeholders
        #
        self.input_sentences = tf.placeholder(tf.int32,
                                              [None, sentence_len],
                                              name="input_sentences")
        self.input_categories = tf.placeholder(tf.double,
                                            [None, category_num],
                                            name="input_categories")
        self.dropout_keep_prob = tf.placeholder(tf.double, name="dropout_keep_prob")
        # embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding layer"):
            # TODO: initialize w using word2vec
            w = tf.Variable(
                tf.random_uniform(
                    [vocabulary_size, embedding_dim],
                    -1.0, 1.0
                )
            )
            # [batch_size, sentence_len, embedding_dim]
            self.embedded_sentences = tf.nn.embedding_lookup(w, self.input_sentences)
            # expand it for conv2d(), -1 indicates the position of insertion
            # of the new dimension in [None, sentence_len, embedding_dim]
            self.expanded_embedded_sentences = tf.expand_dims(self.embedded_sentences, -1)
        # convolution-pooling layer
        # [len(filter_widths), batch_size, 1, 1, filter_num]
        pooled_outputs = []
        for filter_width in filter_widths:
            with tf.name_scope("convolution-pooling layer with filter size %s" % filter_width):
                # convolution layer
                filter_shape = [filter_width, embedding_dim, 1, filter_num]
                # tf.truncated_normal() generates value bounded within 2 * stddev from the mean
                w = tf.Variable(tf.truncated_normal(filter_shape, stddev=0., name="w"))
                b = tf.Variable(tf.constant(0.1, shape=[filter_num]), name="b")
                # yields convolution of [batch_size, sentence_len - filter_width, 1, filter_num]
                convolution = tf.nn.conv2d(
                    # [batch_size, sentence_len, embedding_dim, 1]
                    self.expanded_embedded_sentences,
                    # [filter_width, embedding_dim, 1, filter_num]
                    w,
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="convolution"
                )
                # ReLU activation
                activation = tf.nn.relu(tf.nn.bias_add(convolution, b), name="ReLU")
                # max-pooling
                # [batch_size, 1, 1, filter_num]
                pooled_output = tf.nn.max_pool(
                    activation,
                    # size of the window in which a maximum value is extracted
                    ksize=[1, sentence_len - filter_width + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="max_pooling"
                )
                pooled_outputs.append(pooled_output)
        total_filter_num = len(filter_widths) * filter_num
        # [batch_size, total_filter_num]
        # for each batch: [(feature * filter_num) * len(filter_widths)]
        self.pooled_outputs = tf.reshape(
            # concatenation of pooled_output along the 3rd dimension
            # [batch_size, 1, 1, total_filter_num]
            tf.concat(3, pooled_outputs),
            [-1, total_filter_num]
        )
        # dropout layer
        with tf.name_scope("dropout layer"):
            self.dropout = tf.nn.dropout(self.pooled_outputs, self.dropout_keep_prob)
        # full-connected layer
        with tf.name_scope("full-connected layer"):
            w = tf.Variable(tf.truncated_normal([total_filter_num, category_num], stddev=0.1))
            b = tf.Variable(tf.constant(0.1, shape=[category_num]))
            # [batch_size, category_num]
            self.output_scores = tf.nn.xw_plus_b(self.pooled_outputs, w, b, name="output_scores")
            # reduces across the 1st dimension
            # [batch, 1]
            self.output_predictions = tf.argmax(self.output_scores, 1, name="output_predictions")
        # cross-entropy loss
        with tf.name_scope("loss"):
            self.loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(
                    self.output_scores, self.input_categories
                )
            )
        # accuracy
        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(self.output_predictions, tf.argmax(self.input_categories, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.double), name="accuracy")

    def train(self):
        pass

    def test(self):
        pass

