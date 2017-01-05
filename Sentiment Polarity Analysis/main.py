import tensorflow as tf
import numpy as np
from DataHelper import *
from Model import *

data_helper = DataHelper(
    pos_data_file="rt-polaritydata/rt-polarity.pos",
    neg_data_file="rt-polaritydata/rt-polarity.neg",
    training_data_proportion=.9
)

with tf.Session() as session:
    model = Model(
        sent_len=data_helper.max_sent_len,
        category_num=2,
        vocab_size=data_helper.vocab_size,
        emb_dim=300,
        filter_widths=[3, 4, 5, 6, 7],
        filter_num=100,
        l2_reg_lambda=100.
    )
    model.train(
        session=session,
        data_helper=data_helper,
        dropout_keep_prob=.5,
        max_norm_constraint=3.,
        batch_size=50,
        epoch_num=50,
        step_num_between_validations=50
    )
