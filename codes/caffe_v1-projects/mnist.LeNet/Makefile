
CAFFE_HOME?=${HOME}/caffe_v1/caffe
CAFFE_ROOT?=${CAFFE_HOME}
DIR_SCRIPT=scripts
DIR_DATA=data
DIR_PROT=prototxt
CAFFE_MODEL=snapshots_iter_1000.caffemodel

.PHONNY: all lmdb train run test clean cleanup cleanupall

all:

datasetX: #prepare data set
        # "make lmdb" will do this
	(cd dataset;\
	gzip -d -k -f t10k-images-idx3-ubyte.gz;\
	gzip -d -k -f t10k-labels-idx1-ubyte.gz;\
	gzip -d -k -f train-images-idx3-ubyte.gz;\
	gzip -d -k -f train-labels-idx1-ubyte.gz)

lmdb: # get dataset and convert MNIST to Caffe LMDB
	./${DIR_SCRIPT}/get_mnist.sh ${DIR_DATA}
	./${DIR_SCRIPT}/create_mnist.sh ${CAFFE_HOME} ${DIR_DATA}

train: # training
	if [ ! -d log ]; then mkdir log; fi
	./${DIR_SCRIPT}/train_lenet.sh\
		${CAFFE_HOME} ${DIR_PROT}/lenet_solver.prototxt\
		2>&1 | tee log/lenet_model.log

run test: # testing
	./${DIR_SCRIPT}/test_lenet.sh ${CAFFE_HOME}\
		${DIR_PROT}/lenet_train_test.prototxt\
                ${CAFFE_MODEL}

deploy: # inference; requires Caffe model as a result of 'train'
	python scripts/lenet_deploy.py samples/4.png

draw: # network diagrams for training and deployment
	if [ ! -f prototxt/lenet_train_test.prototxt ]; then\
		echo "prototxt/lenet_train_test.prototxt not found";\
	fi
	${CAFFE_ROOT}/python/draw_net.py prototxt/lenet_train_test.prototxt lenet_train_test.png
	if [ ! -f prototxt/lenet_deploy.prototxt ]; then\
		echo "prototxt/lenet_deploy.prototxt not found";\
	fi
	${CAFFE_ROOT}/python/draw_net.py prototxt/lenet_deploy.prototxt lenet_deploy.png

plot: # loss and accuracy plot; requires log file as a result of 'train'
	if [ ! -d log/lenet_model.log ]; then\
		echo "log/lenet_model.log not found";\
	fi
	${CAFFE_ROOT}/tools/extra/parse_log.py log/lenet_model.log log
	gnuplot -persist -e "log_train='log/lenet_model.log.train';\
		log_test='log/lenet_model.log.test'"\
		scripts/gnuplot_commands

clean:
	/bin/rm -f gmon.out

cleanup:
	/bin/rm -f  t10k-images-idx3-ubyte
	/bin/rm -f  t10k-labels-idx1-ubyte
	/bin/rm -f  train-images-idx3-ubyte
	/bin/rm -f  train-labels-idx1-ubyte
	/bin/rm -rf data/mnist_test_lmdb
	/bin/rm -rf data/mnist_train_lmdb
	/bin/rm -f  lenet_train_test.png
	/bin/rm -f  lenet_deploy.png
	/bin/rm -rf log

cleanupall:
	/bin/rm -rf log
	/bin/rm -rf data
	/bin/rm -rf snapshots_*
