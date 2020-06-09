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
# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("../dataset", one_hot=True)

# Parameters
learning_rate = 0.001
training_epochs = 1000
#training_iters = 200000
batch_size = 100
display_step = 10
accuracy_goal = 0.95

# Network Parameters
n_input = 784 # MNIST data input (img shape: 28*28)
n_classes = 10 # MNIST total classes (0-9 digits)
dropout = 0.75 # Dropout, probability to keep units

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input], name="x-input")
y = tf.placeholder(tf.float32, [None, n_classes], name="y-output")
keep_prob = tf.placeholder(tf.float32, name="keep_prob") #dropout (keep probability)

#-----------------------------------------------------------------------
# Create some wrappers for simplicity
def conv2d(x, W, b, strides=1):
    with tf.name_scope("CONV"):
         # Conv2D wrapper, with bias and relu activation
         # tf.nn.conv2d(input, filter, strides, padding, name=None)
         x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
         x = tf.nn.bias_add(x, b)
         return tf.nn.relu(x)

#-----------------------------------------------------------------------
def maxpool2d(x, k=2):
    with tf.name_scope("POOL"):
         # MaxPool2D wrapper
         # tf.nn.max_pool(input, ksize, stride, padding, name=None)
         return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                               padding='SAME')

#-----------------------------------------------------------------------
# Create model
def conv_net(x, weights, biases, dropout):
    # Reshape input picture: 784-leng vector to 28x28 2D array
    x = tf.reshape(x, shape=[-1, 28, 28, 1])

    with tf.name_scope("CONV-POOL-1"):
         # Convolution Layer
         conv1 = conv2d(x, weights['wc1'], biases['bc1'])
         # Max Pooling (down-sampling)
         conv1 = maxpool2d(conv1, k=2)

    with tf.name_scope("CONV-POOL-2"):
         # Convolution Layer
         conv2 = conv2d(conv1, weights['wc2'], biases['bc2'])
         # Max Pooling (down-sampling)
         conv2 = maxpool2d(conv2, k=2)

    with tf.name_scope("FC"):
         # Fully connected layer
         # Reshape conv2 output to fit fully connected layer input
         fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
         fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
         fc1 = tf.nn.relu(fc1)
         # Apply Dropout
         fc1 = tf.nn.dropout(fc1, dropout)

    with tf.name_scope("OUT"):
         # Output, class prediction
         out = tf.add(tf.matmul(fc1, weights['out']), biases['out'], name="add-output")

    return out

#-----------------------------------------------------------------------
# Store layers weight & bias
with tf.name_scope("WEIGHT-BIAS"):
     weights = {
             # 5x5 conv, 1 input, 32 outputs
             'wc1': tf.Variable(tf.random_normal([5, 5, 1, 32]), name="wc1"),
             # 5x5 conv, 32 inputs, 64 outputs
             'wc2': tf.Variable(tf.random_normal([5, 5, 32, 64]), name="wc2"),
             # fully connected, 7*7*64 inputs, 1024 outputs
             'wd1': tf.Variable(tf.random_normal([7*7*64, 1024]), name="wd1"),
             # 1024 inputs, 10 outputs (class prediction)
             'out': tf.Variable(tf.random_normal([1024, n_classes]), name="wout")
     }

     biases = {
         'bc1': tf.Variable(tf.random_normal([32]), name="bc1"),
         'bc2': tf.Variable(tf.random_normal([64]), name="bc2"),
         'bd1': tf.Variable(tf.random_normal([1024]), name="bd1"),
         'out': tf.Variable(tf.random_normal([n_classes]), name="bout")
     }

#-----------------------------------------------------------------------
# Construct model
with tf.name_scope("CNN"):
     pred = conv_net(x, weights, biases, keep_prob)

#-----------------------------------------------------------------------
# Define loss and optimizer
with tf.name_scope("COST-OPT"):
     cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,
                                                                   labels=y),
                           name="cost")
     optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

#-----------------------------------------------------------------------
# Evaluate model
with tf.name_scope("EVALUATE"):
     correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
     accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

#-----------------------------------------------------------------------
# Initializing the variables
init = tf.global_variables_initializer()

#-----------------------------------------------------------------------
# Add ops to save and restore all the variables
saver = tf.train.Saver()

#-----------------------------------------------------------------------
# Launch the graph
with tf.Session() as sess:
     sess.run(init)
     
     # tensorboard --logdir=./logs
     # http://localhost:6006
     write = tf.summary.FileWriter('./logs', sess.graph)
     
     # Keep training until reach max epochs
     for epoch in range(training_epochs):
         avg_cost = 0.
         avg_accu = 0.
         total_batch = int(mnist.train.num_examples / batch_size)
         print "==epoch:", epoch, "total_batch:", total_batch
         # Loop over all batches
         for i in range(total_batch):
             if i % 50 == 0:
                print "==i:", i
             batch_xs, batch_ys = mnist.train.next_batch(batch_size)
             # Run optimization op (backprop)
             sess.run(optimizer, feed_dict={x: batch_xs, y: batch_ys,
                                            keep_prob: dropout})
             # Compute average loss and accuracy
             #avg_cost += sess.run(cost, feed_dict={x:batch_xs, y:batch_ys,
             #                               keep_prob: dropout})
             #avg_accu += sess.run(accuracy, feed_dict={x:batch_xs, y:batch_ys,
             #                               keep_prob: dropout})
             C, A = sess.run([cost, accuracy], feed_dict={x:batch_xs,
                                                          y:batch_ys,
                                                          keep_prob: dropout})
             avg_cost += C; avg_accu += A

         avg_cost /= total_batch
         avg_accu /= total_batch

         # Display logs per epoch step
         if epoch % display_step == 0:
            print "Epoch:", "%04d" % (epoch + 1),\
                  "cost=", "{:.5f}".format(avg_cost),\
                  "accuracy=", "{:.5f}".format(avg_accu)
            sys.stdout.flush()
         if avg_accu>accuracy_goal:
            break

     print "Optimization Finished!"
     
     #-------------------------------------------------------------------
     # Save weights
     saver.save(sess, "./model/model.ckpt")
     
     #-------------------------------------------------------------------
     # Calculate accuracy for 256 mnist test images
     print "Testing Accuracy:", \
           sess.run(accuracy, feed_dict={x: mnist.test.images[:256],
                                         y: mnist.test.labels[:256],
                                         keep_prob: 1.})
     
     #-------------------------------------------------------------------
     # predict & show
     r = randint(0, mnist.test.num_examples - 1)
     print "Label: ", sess.run(tf.argmax(mnist.test.labels[r:r+1], 1))
     print "Prediction: ", sess.run(tf.argmax(pred, 1), {x: mnist.test.images[r:r+1],
                                                         keep_prob: 1.})
     # show the img
     plt.imshow(mnist.test.images[r:r+1].reshape(28, 28), cmap="Greys", interpolation="nearest")
     plt.show()

#-----------------------------------------------------------------------
