# Python 'hello.py'
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # in order to depress warnings

import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
