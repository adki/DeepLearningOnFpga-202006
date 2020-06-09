import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf

# Define a 2x1 matrix
matrix1 = tf.constant([[1., 2.]])

# Define a 1x2 matrix
matrix2 = tf.constant([[1], 
                       [2]])

# Define a rank 3 tensor
myTensor = tf.constant([ [[1,2], 
                          [3,4], 
                          [5,6]], 
                         [[7,8], 
                          [9,10], 
                          [11,12]] ])

# Try printing the tensors 
print(matrix1)
print(matrix2)
print(myTensor)

#
sess = tf.Session()
result = sess.run(matrix1)
print result

result = sess.run(matrix2)
print result

result = sess.run(myTensor)
print result

#---------------------------------------------
# Tensor("Const:0", shape=(1, 2), dtype=float32)
# Tensor("Const_1:0", shape=(2, 1), dtype=int32)
# Tensor("Const_2:0", shape=(2, 3, 2), dtype=int32)
# [[ 1.  2.]]
# [[1]
#  [2]]
# [[[ 1  2]
#   [ 3  4]
#   [ 5  6]]
# 
#  [[ 7  8]
#   [ 9 10]
#   [11 12]]]
