#!/usr/bin/env python

import os
import sys
import caffe
from caffe.proto import caffe_pb2
import numpy # for array

caffe_path = caffe.__path__
print(caffe_path)

caffe_home = os.environ["CAFFE_ROOT"];

net_path = caffe_home + '/examples/cifar10/cifar10_quick.prototxt'
model_path = '../cifar-10/cifar10_quick_iter_4000.caffemodel'
mean_path = '../cifar-10/data/mean.binaryproto'

cifar_map = {
        0: "airplane",
        1: "automobile",
        2: "bird",
        3: "cat",
        4: "deer",
        5: "dog",
        6: "frog",
        7: "hourse",
        8: "ship",
        9: "truck"
}

mean_blob = caffe_pb2.BlobProto()

with open(mean_path) as f:
    mean_blob.ParseFromString(f.read())

mean_array = numpy.asarray(
    mean_blob.data,
    dtype=numpy.float32
).reshape(
    (mean_blob.channels, mean_blob.height, mean_blob.width)
)

classifier = caffe.Classifier(
    net_path,
    model_path,
    mean=mean_array,
    raw_scale=255)

# sys.argv[0] is script name
# sys.argv[1] is image file
image = caffe.io.load_image(sys.argv[1])

# predict(target_image, oversample=True|False)
# oversample's default value is True
predictions = classifier.predict([image], oversample=False)
answer = numpy.argmax(predictions) # get max value's index

# RESULT
print("====================================")
print("possibility of each categoly")
for index, prediction in enumerate(predictions[0]):
    print (str(index)+"("+cifar_map[index]+"): ").ljust(15) + str(prediction)
print("====================================")
print("I guess this image is [" + cifar_map[answer] + "]")
