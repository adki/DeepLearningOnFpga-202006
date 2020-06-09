
all:

run:
	GLOG_minloglevel=2\
		python caffe-yolov2/yolo_detect.py\
		caffe-yolov2/prototxt/tiny_yolo_deploy.prototxt\
		model/tiny_yolo.caffemodel caffe-yolov2/images/dog.jpg

get:
	git clone https://github.com/tsingjinyun/caffe-yolov2.git

clean:

cleanup clobber: clean

cleanupall: cleanup
