# Three ways to represent a tensor.
# tensor.py

import tensorflow as tf
import numpy as np   

# Define a 2x2 matrix in 3 different ways
m1 = [[1.0, 2.0], 
      [3.0, 4.0]]
m2 = np.array([[1.0, 2.0], 
               [3.0, 4.0]], dtype=np.float32)
m3 = tf.constant([[1.0, 2.0], 
                  [3.0, 4.0]])

# Print the type for each matrix
print(type(m1)) # <type 'list'>
print(type(m2)) # <type 'numpy.ndarray'>
print(type(m3)) # <class 'tensorflow.python.framework.ops.Tensor'>

# Create tensor objects out of the different types
t1 = tf.convert_to_tensor(m1, dtype=tf.float32)
t2 = tf.convert_to_tensor(m2, dtype=tf.float32)
t3 = tf.convert_to_tensor(m3, dtype=tf.float32)

# Notice that the types will be the same now
print(type(t1)) # <class 'tensorflow.python.framework.ops.Tensor'>
print(type(t2)) # <class 'tensorflow.python.framework.ops.Tensor'>
print(type(t3)) # <class 'tensorflow.python.framework.ops.Tensor'>

#-----------------------------------------------------
# <type 'list'>
# <type 'numpy.ndarray'>
# <class 'tensorflow.python.framework.ops.Tensor'>
# <class 'tensorflow.python.framework.ops.Tensor'>
# <class 'tensorflow.python.framework.ops.Tensor'>
# <class 'tensorflow.python.framework.ops.Tensor'>
