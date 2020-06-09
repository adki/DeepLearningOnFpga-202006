# xor_simple.py'
#
# activation function: tanh
# cost function:       square sum
# optimizater:         gradient descent
#
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # in order to depress warnings

#-------------------------------------------------------------
import tensorflow as tf

#-------------------------------------------------------------
# variables for input and output
x = tf.compat.v1.placeholder(shape=[4, 2], dtype=tf.float32, name="x-input")
y = tf.compat.v1.placeholder(shape=[4, 1], dtype=tf.float32, name="y-expected")

#-------------------------------------------------------------
# 1st layer
# W1: Shape [2,2]
# b1: shape [2]
W1 = tf.Variable(tf.random.uniform([2,2],-1,1), name="W1")
b1 = tf.Variable([.0,.0], dtype=tf.float32, name="b1")
h1 = tf.tanh(tf.matmul(x, W1) + b1) # (2x1) * (2x2) * (2x1)

#-------------------------------------------------------------
# 2nd layer
# W2: Shape [2,1]
# b2: shape [1]
W2 = tf.Variable(tf.random.uniform([2,1],-1,1), name="W2")
b2 = tf.Variable([.0], dtype=tf.float32, name="b2")
h2 = tf.tanh(tf.matmul(h1, W2) + b2, name="op_to_restore") 

#-------------------------------------------------------------
# cost function: Square Sum
cost = tf.reduce_sum(tf.square(y - h2))

#-------------------------------------------------------------
# optimizer with learning rate 0.05
optimizer = tf.compat.v1.train.GradientDescentOptimizer(0.05)
train = optimizer.minimize(cost)

#-------------------------------------------------------------
sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())

#-------------------------------------------------------------
# training data set
x_train = [[0,0], [0,1], [1,0], [1,1]] # all input patterns
y_train = [[0], [1], [1], [0]] # expected output

#-------------------------------------------------------------
for i in range(50000):
    sess.run(fetches=train, feed_dict={x:x_train, y:y_train})
    if i%200==0:
       print('Batch:     ', i)
       print('W1:        ', sess.run(W1))
       print('b1:        ', sess.run(b1))
       print('W2:        ', sess.run(W2))
       print('b2:        ', sess.run(b2))
       print('Inference: ', sess.run(h2, {x:x_train, y:y_train}))
       #print('Cost:      ', result = sess.run(cost,  {x:x_train, y:y_train}))
       result = sess.run(cost,  {x:x_train, y:y_train})
       print('Cost:      ', result)
       if (result<0.001):
           break

#-------------------------------------------------------------
