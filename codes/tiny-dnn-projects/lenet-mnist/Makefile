#-------------------------------------------------------------------------------
# How to run:
# 1. Preparing programs for training and inference
#     $ make train
#     $ make test
# 2. Running training, i.e., learning (may take time; use "LeNet-model-ref" instead)
#     $ make learn
# 3. Running inference
#     $ make inference
#-------------------------------------------------------------------------------
SHELL	=/bin/bash

#-------------------------------------------------------------------------------
#CXX	=g++-4.9
CXX	=g++
TINY_DNN=${TINYDNN_HOME}
USER_DEFINES=-DVERBOSE
DEFINES=-DCNN_USE_DOUBLE -DDNN_USE_IMAGE_API $(USER_DEFINES)
#DEFINES=-DDNN_USE_IMAGE_API $(USER_DEFINES)
CXXFLAGS=-I$(TINY_DNN) $(DEFINES) -std=c++14 -pthread -O2
LDFLAGS	=
LDLIBS	=-lpthread
#-------------------------------------------------------------------------------
.cpp.o:; $(CXX) -c $< $(CXXFLAGS) 2>&1 | tee compile.log.$*

#-------------------------------------------------------------------------------
all: train test

#-------------------------------------------------------------------------------
train: train.o
	$(CXX) -o $@ $^ $(LDFLAGS) $(LDLIBS) 2>&1 | tee -a compile.log.$@

#-------------------------------------------------------------------------------
test: test.o
	$(CXX) -o $@ $^ $(LDFLAGS) $(LDLIBS) 2>&1 | tee -a compile.log.$@

#-------------------------------------------------------------------------------
.PHONY: run
run: train test
	make learn
	make inference

#-------------------------------------------------------------------------------
.PHONY: learn
DATASET=t10k-images.idx3-ubyte t10k-labels.idx1-ubyte\
        train-images.idx3-ubyte train-labels.idx1-ubyte
learn: train
	for D in ${DATASET};do\
		if [ ! -f dataset/$${D} ]; then\
			(cd dataset; gzip -d -k -f $${D}.gz);\
		fi;\
	done
	./train --epochs 30 --data_path dataset

#-------------------------------------------------------------------------------
.PHONY: inference
inference: test
#	./test  testset/2.jpg
#	./test  testset/3.bmp
#	./test  testset/3.jpg
	./test  testset/4.bmp LeNet-model-ref

#-------------------------------------------------------------------------------
.PHONE: datasetX
.IGNORE: datasetX
datasetX:
	(cd dataset;\
	gzip -d -k -f t10k-images.idx3-ubyte.gz;\
	gzip -d -k -f t10k-labels.idx1-ubyte.gz;\
	gzip -d -k -f train-images.idx3-ubyte.gz;\
	gzip -d -k -f train-labels.idx1-ubyte.gz;)

#-------------------------------------------------------------------------------
.PHONE: testsetX
.IGNORE: testsetX
testsetX:
	(cd testset;\
	./mnist_to_png/convert_mnist_to_png.py ../dataset png;)

#-------------------------------------------------------------------------------
.PHONY: clean cleanup

clean:
	/bin/rm -f  train.o compile.log.train
	/bin/rm -f  test.o compile.log.test
	/bin/rm -f  layer*.png weights*.png
	/bin/rm -f  dataset/t10k-images-idx3-ubyte
	/bin/rm -f  dataset/t10k-labels-idx1-ubyte
	/bin/rm -f  dataset/train-images-idx3-ubyte
	/bin/rm -f  dataset/train-labels-idx1-ubyte
	/bin/rm -rf testset/png

cleanup: clean
	/bin/rm -f train
	/bin/rm -f test
	/bin/rm -f LeNet-model

cleanupall: cleanup
	for D in ${DATASET};do\
		/bin/rm -f dataset/$${D};\
	done

#-------------------------------------------------------------------------------
