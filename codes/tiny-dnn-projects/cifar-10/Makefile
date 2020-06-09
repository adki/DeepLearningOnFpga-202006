#-------------------------------------------------------------------------------
# How to run:
# 1. Preparing programs for training and inference
#     $ make train
#     $ make test
# 2. Preparing training dataset
#     $ make dataset
# 3. Preparing testing dataset, i.e., testset
#     $ make testset
# 4. Running training, i.e., learning (may take time; use "cifar-weights-ref" instead)
#     $ make learn
# 5. Running inference
#     $ make inference
#-------------------------------------------------------------------------------
SHELL	=/bin/bash

#-------------------------------------------------------------------------------
#CXX	=g++-4.9
CXX	=g++
TINY_DNN=$(TINYDNN_HOME)
CXXFLAGS=-I$(TINY_DNN) -DCNN_USE_DOUBLE -DDNN_USE_IMAGE_API -DVERBOSE -std=c++14 -pthread -O2
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
learn: train
	@if [ ! -d dataset/cifar-10-batches-bin ]; then\
		echo "dataset/cifar-10-batches-bin not found";\
		echo "run \"$$ make dataset\"";\
		exit 1;\
	fi
	./train --data_path dataset/cifar-10-batches-bin\
		--learning_rate 0.01 --epochs 30\
		--minibatch_size 10 --backend_type internal

#-------------------------------------------------------------------------------
.PHONY: inference
inference: test
	@if [ ! -f cifar-weights ]; then\
		echo "cifar-weights not found";\
		echo "run \"$$ make learn\"";\
		echo "or copy cifar-weights-ref";\
		exit 1;\
	fi
	@if [ ! -f testset/test_batch.bin-00*.png ]; then\
		echo "tesetset/test_batch.bin-*.png not found";\
		echo "run \"$$ make testset\"";\
		exit 1;\
	fi
	./test  testset/test_batch.bin-00-3.png
#	./test  testset/test_batch.bin-01-8.png
#	./test  testset/test_batch.bin-02-8.png
#	./test  testset/test_batch.bin-03-0.png
#	./test  testset/test_batch.bin-04-6.png
#	./test  testset/test_batch.bin-05-6.png
#	./test  testset/test_batch.bin-06-1.png
#	./test  testset/test_batch.bin-07-6.png
#	./test  testset/test_batch.bin-08-3.png
#	./test  testset/test_batch.bin-09-1.png
#	./test  testset/test_batch.bin-10-0.png
#	./test  testset/test_batch.bin-11-9.png
#	./test  testset/test_batch.bin-12-5.png
#	./test  testset/test_batch.bin-13-7.png
#	./test  testset/test_batch.bin-14-9.png
#	./test  testset/test_batch.bin-15-8.png
#	./test  testset/test_batch.bin-16-5.png
#	./test  testset/test_batch.bin-17-7.png
#	./test  testset/test_batch.bin-18-8.png
#	./test  testset/test_batch.bin-19-6.png


#-------------------------------------------------------------------------------
.PHONY: dataset
dataset:
	(cd dataset;\
	tar xvf cifar-10-binary.tar.gz)

#-------------------------------------------------------------------------------
.PHONY: testset
testset:
	@if [ ! -f dataset/cifar-10-batches-bin/test_batch.bin ]; then\
		echo "dataset/cifar-10-batches-bin/test_batch.bin not found";\
		echo "run \"$$ make dataset\"";\
		exit 1;\
	fi
	(cd testset;\
	unzip cifar-10-load-converter-master.zip;\
	python cifar-10-load-converter-master/convert_cifar10_png.py\
		--offset 0 --count 20\
		--data ../dataset/cifar-10-batches-bin/test_batch.bin\
		--save_dir .)

#-------------------------------------------------------------------------------
.PHONY: clean cleanup

clean:
	/bin/rm -f train.o compile.log.train
	/bin/rm -f test.o compile.log.test
	/bin/rm -f layer*.png weights*.png

cleanup: clean
	/bin/rm -f  train
	/bin/rm -f  test
	/bin/rm -f  cifar-weights cifar-weights-json
	/bin/rm -fr dataset/cifar-10-batches-bin
	/bin/rm -f  testset/test_batch.bin*.png
	/bin/rm -fr testset/cifar-10-load-converter-master

cleanupall: cleanup

#-------------------------------------------------------------------------------
