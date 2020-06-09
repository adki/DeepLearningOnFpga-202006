#-----------------------------------------------------------------------
# https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/3_NeuralNetworks/convolutional_network.py
#
# A Convolutional Network implementation example using TensorFlow library.
# This example is using the MNIST database of handwritten digits
# (http://yann.lecun.com/exdb/mnist/)
# Author: Aymeric Damien
# Project: https://github.com/aymericdamien/TensorFlow-Examples/
#-----------------------------------------------------------------------
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
sys.path.append(os.path.dirname("../../../tensorflow/tensorflow"))

#-----------------------------------------------------------------------
import tensorflow as tf
from random import randint
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------
sess = tf.Session()

#-----------------------------------------------------------------------
# Create the network
saver = tf.train.import_meta_graph("./model/model.ckpt.meta")

#-----------------------------------------------------------------------
# Restore parameters
saver.restore(sess, "./model/model.ckpt")

#-----------------------------------------------------------------------
# get references of graph and tensors
graph = tf.get_default_graph()
x = graph.get_tensor_by_name("x-input:0");
y = graph.get_tensor_by_name("y-output:0");
keep_prob = graph.get_tensor_by_name("keep_prob:0");
infer = graph.get_tensor_by_name("CNN/OUT/add-output:0")

#-----------------------------------------------------------------------
# testing data-set
#-----------------------------------------------------------------------
# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("../dataset", one_hot=True)

for i in range(10):
    # predict & show
    r = randint(0, mnist.test.num_examples - 1)
    print "Label: " , sess.run(tf.argmax(mnist.test.labels[r:r+1], 1))
    print "Prediction: ", sess.run(tf.argmax(infer, 1), {x: mnist.test.images[r:r+1],
                                                    keep_prob: 1.})
    # show the img
    plt.imshow(mnist.test.images[r:r+1].reshape(28, 28), cmap="Greys", interpolation="nearest")
    plt.show()
#-----------------------------------------------------------------------
