SHELL=/bin/bash

PROG=lenet_confmc.py
DIR_IMAGE=../lenet.confmc/images

all:

run:
	python -O ./$(PROG) -i $(DIR_IMAGE)/0.png

run.all:
	for N in 0 1 2 3 4 5 6 7 8 9; do\
		echo "python -O ./$(PROG) -i $(DIR_IMAGE)/$$N.png";\
		python -O ./$(PROG) -i $(DIR_IMAGE)/$$N.png;\
	done

clean:

cleanup clobber:

cleanupall distclean:
