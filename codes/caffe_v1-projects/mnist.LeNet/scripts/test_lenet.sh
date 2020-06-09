#!/bin/bash
# test_lenet.sh <CAFFE_HOME> <NET> <MODEL>
set -e

CAFFE_HOME=$1
CAFFE_NET=$2
CAFFE_MODEL=$3
${CAFFE_HOME}/build/tools/caffe test\
                -model ${CAFFE_NET}\
                -weights ${CAFFE_MODEL}
