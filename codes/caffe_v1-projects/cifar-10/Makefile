SHELL=/bin/bash
CAFFE_HOME?=${HOME}/caffe_v1/caffe
CAFFE_ROOT?=${CAFFE_HOME}
SOLVER=prototxt/cifar10_quick_solver.prototxt
TRAIN=prototxt/cifar10_quick_train_test.prototxt
DEPLOY=prototxt/cifar10_quick_deploy.prototxt
LOG=log/cifar10.log

all:

step0:
	(cd data; ./get_cifar10.sh)

step1:
	./data/create_cifar10.sh

step2 train:
	if [ ! -d $(dir ${LOG}) ]; then mkdir $(dir ${LOG}); fi
	${CAFFE_ROOT}/build/tools/caffe train \
		--solver=${SOLVER} 2>&1\
		| tee ${LOG}

step3 deploy:
	python scripts/cifar10_deploy.py samples/airplane1.jpg
#	python scripts/cifar10_deploy.py samples/cat1.jpg
#	python scripts/cifar10_deploy.py samples/dog1.jpg
#	python scripts/cifar10_deploy.py samples/dogcat1.jpg

draw:
	${CAFFE_ROOT}/python/draw_net.py ${TRAIN} $(basename $(notdir ${TRAIN})).png
	${CAFFE_ROOT}/python/draw_net.py ${TRAIN} $(basename $(notdir ${DEPLOY})).png

plot:
	if [ ! -d ${LOG} ]; then\
		echo ${LOG} not found;\
	fi
	${CAFFE_ROOT}/tools/extra/parse_log.py ${LOG} $(dir ${LOG})
	gnuplot -persist -e "log_train='${LOG}.train';\
		log_test='${LOG}.test'"\
		scripts/gnuplot_commands

clean:
	/bin/rm -f  $(basename $(notdir ${TRAIN})).png
	/bin/rm -fr log

cleanup clobber: clean
#following by create_cifar10.sh
	/bin/rm -rf data/cifar10_train_lmdb
	/bin/rm -rf data/cifar10_test_lmdb
	/bin/rm -f  data/mean.binaryproto

cleanupall: cleanup
#following by get_cifar10.sh
	/bin/rm -f  data/batches.meta.txt
	/bin/rm -f  data/data_batch_1.bin
	/bin/rm -f  data/data_batch_2.bin
	/bin/rm -f  data/data_batch_3.bin
	/bin/rm -f  data/data_batch_4.bin
	/bin/rm -f  data/data_batch_5.bin
	/bin/rm -f  data/readme.html
	/bin/rm -f  data/test_batch.bin
