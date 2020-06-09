# xor_inference.py'
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # in order to depress warnings

#-------------------------------------------------------------
import tensorflow as tf

#-------------------------------------------------------------
sess = tf.Session()

#-------------------------------------------------------------
# create the network
saver = tf.train.import_meta_graph("./model/model.ckpt.meta")

#-------------------------------------------------------------
# restore parameters, i.e., weights
saver.restore(sess,"./model/model.ckpt")

#-------------------------------------------------------------
graph = tf.get_default_graph()

#-------------------------------------------------------------
# get references of tensors
x = graph.get_tensor_by_name("x-input:0");
y = graph.get_tensor_by_name("y-expected:0");
ops = graph.get_tensor_by_name("op_to_restore:0")

#-------------------------------------------------------------
# testing data-set
feed_dict = {x:[[0,0],[0,1],[1,0],[1,1]], # pattern to infer
             y:[[0], [0], [0], [0]]} # it doesn't matter
            #y:[[0], [1], [1], [0]]}

#-------------------------------------------------------------
# inference
print sess.run(ops, feed_dict)

#-------------------------------------------------------------
