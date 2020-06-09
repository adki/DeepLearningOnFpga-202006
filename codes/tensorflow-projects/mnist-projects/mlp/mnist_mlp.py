#-----------------------------------------------------------------------
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
sys.path.append(os.path.dirname("../../../tensorflow/tensorflow"))

#-----------------------------------------------------------------------
import tensorflow as tf
import tensorflow as tf
import numpy as np
from random import randint
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------
# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("../dataset", one_hot=True)

#-----------------------------------------------------------------------
# Parameters
learning_rate = 0.01
training_epochs = 1000
batch_size = 100
display_step = 10

#-----------------------------------------------------------------------
# tf Graph Input
x = tf.placeholder("float", [None, 784], name="x-input") # mnist data image of shape 28*28
y = tf.placeholder("float", [None, 10], name="y-output") # 0-9 digits recognition => 10 classes

#-----------------------------------------------------------------------
# Model weights
W1 = tf.Variable(tf.random_normal([784,256]), name="weight1")
b1 = tf.Variable(tf.random_normal([256]), name="bias1")
W2 = tf.Variable(tf.random_normal([256,256]), name="weight2")
b2 = tf.Variable(tf.random_normal([256]), name="bias2")
W3 = tf.Variable(tf.random_normal([256,10]), name="weight-out")
b3 = tf.Variable(tf.random_normal([10]), name="bias-out")

#-----------------------------------------------------------------------
# inference -> hypothesis
layer_1 = tf.add(tf.matmul(x, W1), b1)
layer_1 = tf.nn.sigmoid(layer_1, name="layer1-sigmoid")
layer_2 = tf.add(tf.matmul(layer_1, W2), b2)
layer_2 = tf.nn.sigmoid(layer_2, name="layer2-sigmoid")
#infer = tf.add(tf.matmul(layer_2, W3), b3, name="infer")
out_layer = tf.add(tf.matmul(layer_2, W3), b3)
infer = tf.nn.softmax(out_layer, name="infer")

#-----------------------------------------------------------------------
# Minimize error using cross entropy
cost = tf.reduce_mean(-tf.reduce_sum(y * tf.log(infer), reduction_indices=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
# softmanx_cross_entropy_with_logits()
# --> for calculate cross entropy loss between predictions and labels
#cost      = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=infer, labels=y))
#optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

#-----------------------------------------------------------------------
# Evaluate -- 0~1 accuracy
correct  = tf.equal(tf.argmax(infer, 1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct, "float"))

#-----------------------------------------------------------------------
# Initializing the variables
init = tf.global_variables_initializer()

#-----------------------------------------------------------------------
# Add ops to save and restore all the variables
saver = tf.train.Saver()

#-----------------------------------------------------------------------
with tf.Session() as sess:
     sess.run(init)

     # tensorboard --logdir=./logs
     # http://localhost:6006
     write = tf.summary.FileWriter('./logs', sess.graph)
     
     # Training cycle
     for epoch in range(training_epochs):
         avg_cost = 0.
         avg_accu = 0.
         total_batch = int( mnist.train.num_examples / batch_size )
         #print "num_examples:", mnist.train.num_examples
         #print "batch_size:", batch_size
         #print "total_batch:", total_batch
         # Loop over all batches
         for i in range(total_batch):
             batch_xs, batch_ys = mnist.train.next_batch(batch_size)
             # Fit training using batch data
             sess.run(optimizer, feed_dict={x: batch_xs, y: batch_ys})
             # Compute average loss and accuracy
             avg_cost += sess.run(cost, feed_dict={x: batch_xs, y: batch_ys})
             avg_accu += sess.run(accuracy, feed_dict={x: batch_xs, y: batch_ys})

         avg_cost /= total_batch
         avg_accu /= total_batch

         # Display logs per epoch step
         if epoch % display_step == 0:
            print "Epoch:", "%04d" % (epoch + 1),\
                  "cost=", "{:.5f}".format(avg_cost),\
                  "accuracy=", "{:.5f}".format(avg_accu)
         if avg_accu>0.95:
            break
         
     print "Optimization finished"

     # Save weights
     saver.save(sess, "./model/model.ckpt")

     #------------------------------------------------------------------
     # Test model
     #------------------------------------------------------------------
     # Calculate accuracy
     #correct_prediction = tf.equal(tf.argmax(infer, 1), tf.argmax(y,1))
     #accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
     print "Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels})

     #------------------------------------------------------------------
     # predict & show
     r = randint(0, mnist.test.num_examples - 1)
     print "Label: " , sess.run(tf.argmax(mnist.test.labels[r:r+1], 1))
     print "Prediction: " , sess.run(tf.argmax(infer, 1), {x: mnist.test.images[r:r+1]})
     # show the img
     plt.imshow(mnist.test.images[r:r+1].reshape(28, 28), cmap="Greys", interpolation="nearest")
     plt.show()
#-----------------------------------------------------------------------
