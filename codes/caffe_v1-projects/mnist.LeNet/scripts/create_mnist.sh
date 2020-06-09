#!/bin/bash
# This script converts the mnist data into lmdb/leveldb format,
# depending on the value assigned to $BACKEND.
#
# create_mnist.sh <CAFFE_HOME> <DIR_DATA>
set -e

EXAMPLE=.
DATA=$2
CAFFE_HOME=$1
BUILD=${CAFFE_HOME}/build/examples/mnist

BACKEND="lmdb"

echo "Creating ${BACKEND}..."

if [ ! -e ${DATA}/mnist_train_${BACKEND} ]; then
${BUILD}/convert_mnist_data.bin\
  --backend=${BACKEND}\
  ${DATA}/train-images-idx3-ubyte\
  ${DATA}/train-labels-idx1-ubyte\
  ${DATA}/mnist_train_${BACKEND}
fi
if [ ! -e ${DATA}/mnist_test_${BACKEND} ]; then
${BUILD}/convert_mnist_data.bin\
  --backend=${BACKEND}\
  ${DATA}/t10k-images-idx3-ubyte\
  ${DATA}/t10k-labels-idx1-ubyte\
  ${DATA}/mnist_test_${BACKEND}
fi

echo "Done."
