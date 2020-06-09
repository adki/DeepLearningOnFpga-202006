# xor_tensorboard.py'
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # in order to depress warnings

#-------------------------------------------------------------
import tensorflow as tf

#-------------------------------------------------------------
# variables for input and output
with tf.name_scope("input"):
     x = tf.placeholder(shape=[4, 2], dtype=tf.float32, name="x-input")
     y = tf.placeholder(shape=[4, 1], dtype=tf.float32, name="y-expected")

#-------------------------------------------------------------
# 1st layer
# W1: Shape [2,2]
# b1: shape [2]
with tf.name_scope("layer-1st"):
     W1 = tf.Variable(tf.random_uniform([2,2],-1,1), name="W1")
     b1 = tf.Variable([.0,.0], dtype=tf.float32, name="b1")
     h1 = tf.sigmoid(tf.matmul(x, W1) + b1) # (2x1) * (2x2) * (2x1)

#-------------------------------------------------------------
# 2nd layer
# W2: Shape [2,1]
# b2: shape [1]
with tf.name_scope("layer-2nd"):
     W2 = tf.Variable(tf.random_uniform([2,1],-1,1), name="W2")
     b2 = tf.Variable([.0], dtype=tf.float32, name="b2")
     h2 = tf.sigmoid(tf.matmul(h1, W2) + b2, name="op_to_restore") 

#-------------------------------------------------------------
# cost function: MSE (Mean Square Estimate)
with tf.name_scope("cost"):
     cost = tf.reduce_mean(tf.square(y - h2))

#-------------------------------------------------------------
# optimizer with learning rate 0.05
optimizer = tf.train.GradientDescentOptimizer(0.05)
train = optimizer.minimize(cost)

#-------------------------------------------------------------
# dynamic log
w1_hist = tf.summary.histogram("W1-weight", W1)
b1_hist = tf.summary.histogram("b1-bias", b1)
w2_hist = tf.summary.histogram("W2-weight", W2)
b2_hist = tf.summary.histogram("b2-bias", b2)
cost_summ = tf.summary.scalar("cost", cost)
summary_op = tf.summary.merge_all()

#-------------------------------------------------------------
sess = tf.Session()
sess.run(tf.global_variables_initializer())

#-------------------------------------------------------------
# tensorboard --logdir=./logs
# http://localhost:6006
writer = tf.summary.FileWriter('./logs', sess.graph)

#-------------------------------------------------------------
# training data set
x_train = [[0,0], [0,1], [1,0], [1,1]] # all input patterns
y_train = [[0], [1], [1], [0]] # expected output

#-------------------------------------------------------------
for i in range(10000):
    sess.run(fetches=train, feed_dict={x:x_train, y:y_train})
    if i%1000==0:
       summary = sess.run(fetches=summary_op, feed_dict={x:x_train, y:y_train})
       writer.add_summary(summary, i)
       print('Batch:     ', i)
       print('W1:        ', sess.run(W1))
       print('b1:        ', sess.run(b1))
       print('W2:        ', sess.run(W2))
       print('b2:        ', sess.run(b2))
       print('Inference: ', sess.run(h2, {x:x_train, y:y_train}))
       print('Cost:      ', sess.run(cost,  {x:x_train, y:y_train}))

