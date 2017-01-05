import tensorflow as tf
from DataHelper import *

class Model:
    def __init__(
        self,
        sent_len,
        category_num,
        vocab_size,
        emb_dim,
        filter_widths,
        filter_num,
        l2_reg_lambda
    ):
        # input placeholders
        self.input_sents = tf.placeholder(
            tf.int32,
            [None, sent_len],
            name="input_sents"
        )
        self.stand_categories = tf.placeholder(
            tf.float32,
            [None, category_num],
            name="stand_categories"
        )
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
        # l2 loss
        l2_loss = tf.constant(0.0)
        # embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding-layer"):
            embeddings = tf.Variable(
                tf.random_uniform(
                    [vocab_size, emb_dim],
                    -1.0, 1.0
                )
            )
            # [batch_size, sent_len, emb_dim]
            self.embedded_sentences = tf.nn.embedding_lookup(embeddings, self.input_sents)
            # expand it for conv2d(), -1 indicates the position of insertion
            # of the new dimension in [None, sent_len, emb_dim]
            self.expanded_embedded_sentences = tf.expand_dims(self.embedded_sentences, -1)
        # convolution-pooling layer
        # [batch_size, 1, 1, filter_num] * len(filter_widths)
        pooled_outputs = []
        for filter_width in filter_widths:
            with tf.name_scope("convolution-pooling-layer-%s" % filter_width):
                # convolution layer
                filter_shape = [filter_width, emb_dim, 1, filter_num]
                # tf.truncated_normal() generates value bounded within 2 * stddev from the mean
                w = tf.Variable(tf.truncated_normal(filter_shape, stddev=0., name="w"))
                b = tf.Variable(tf.constant(0.1, shape=[filter_num]), name="b")
                # [batch_size, sent_len - filter_width, 1, filter_num]
                convolution = tf.nn.conv2d(
                    # [batch_size, sent_len, emb_dim, 1]
                    self.expanded_embedded_sentences,
                    # [filter_width, emb_dim, 1, filter_num]
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
                    ksize=[1, sent_len - filter_width + 1, 1, 1],
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
        with tf.variable_scope("dropout-layer"):
            self.dropout = tf.nn.dropout(self.pooled_outputs, self.dropout_keep_prob)
        # full-connected layer
        with tf.variable_scope("full-connected-layer"):
            # use tf.get_variable() in order to user specific initializer
            self.w = tf.get_variable(
                name="w",
                shape=[total_filter_num, category_num],
                initializer=tf.contrib.layers.xavier_initializer()
            )
            l2_loss += tf.nn.l2_loss(self.w)
            b = tf.Variable(tf.constant(0.1, shape=[category_num]))
            l2_loss += tf.nn.l2_loss(b)
            # [batch_size, category_num]
            self.output_scores = tf.nn.xw_plus_b(self.pooled_outputs, self.w, b, name="output_scores")
            # reduces across the 1st dimension
            # [batch, 1]
            self.output_predictions = tf.argmax(self.output_scores, 1, name="output_predictions")
        # cross-entropy loss + l2 regularization
        with tf.variable_scope("loss"):
            self.loss = \
                tf.reduce_mean(
                    tf.nn.softmax_cross_entropy_with_logits(
                        self.output_scores, self.stand_categories
                    )
                ) + l2_reg_lambda * l2_loss
        # accuracy
        with tf.variable_scope("accuracy"):
            correct_predictions = tf.equal(self.output_predictions, tf.argmax(self.stand_categories, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.double), name="accuracy")

    def train(
        self,
        session,
        data_helper,
        dropout_keep_prob,
        max_norm_constraint,
        batch_size,
        epoch_num,
        step_num_between_validations
    ):
        result_file = open("result.txt", 'w', encoding='utf-8')

        global_step = tf.Variable(0, name="global_step", trainable=False)
        optimizer = tf.train.AdamOptimizer(1e-3)
        grads_and_vars = optimizer.compute_gradients(self.loss)
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)
        constrain_norm_op = self.w.assign(tf.clip_by_norm(self.w, max_norm_constraint, axes=0))
        
        session.run(tf.initialize_all_variables())

        def train_on_batch(sent_batch, category_batch):
            _, step, loss, accuracy = session.run(
                [train_op, global_step, self.loss, self.accuracy],
                feed_dict={
                    self.input_sents: sent_batch,
                    self.stand_categories: category_batch,
                    self.dropout_keep_prob: dropout_keep_prob
                }
            )
            print("step %d, loss %.5f, accuracy %.5f" % (step, loss, accuracy))
            return step

        def validate():
            step, loss, accuracy = session.run(
                [global_step, self.loss, self.accuracy],
                feed_dict={
                    self.input_sents: data_helper.validation_sents,
                    self.stand_categories: data_helper.validation_categories,
                    self.dropout_keep_prob: 1.
                }
            )
            print("step %d, loss %.5f, accuracy %.5f\n" % (step, loss, accuracy))

        for sent_batch, category_batch in data_helper.gen_batches(batch_size, epoch_num):
            step = train_on_batch(sent_batch, category_batch)
            session.run(constrain_norm_op)
            if step % step_num_between_validations == 0:
                print("\nvalidate:")
                validate()
