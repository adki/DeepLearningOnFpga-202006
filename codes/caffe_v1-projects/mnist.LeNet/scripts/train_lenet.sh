#!/bin/bash
# train_mnist.sh <CAFFE_HOME> <SOLVER>
set -e

CAFFE_HOME=$1
SOLVER=$2

echo "${CAFFE_HOME}/build/tools/caffe train --solver=${SOLVER}"
${CAFFE_HOME}/build/tools/caffe train --solver=${SOLVER}
