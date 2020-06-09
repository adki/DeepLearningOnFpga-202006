SHELL=/bin/bash

TARGET=test
DIR_OUT=out

all: protobuffer
	g++ -o ${TARGET} main.cpp ${DIR_OUT}/person.pb.cc\
		-I${DIR_OUT} `pkg-config --cflags --libs protobuf`

protobuffer:
	@if [ ! -e ${DIR_OUT} ]; then mkdir ${DIR_OUT}; fi
	protoc --cpp_out=${DIR_OUT} person.proto

run:
	@if [ ! -e ${TARGET} ]; then\
		echo "Compile first.";\
	else\
		echo "./${TARGET}";\
		./${TARGET};\
	fi

clean:
	/bin/rm -f ${TARGET}
	/bin/rm -f myfile.protobin myfile.prototxt

cleanup: clean
	/bin/rm -rf ${DIR_OUT}

cleanupall: cleanup
