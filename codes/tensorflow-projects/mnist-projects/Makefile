DIRS	= $(subst /,, $(dir $(wildcard */Makefile)))

all:

clean cleanup clobber:
	for D in $(DIRS); do\
		if [ -f $$D/Makefile ] ; then \
			echo "make -C $$D -s $@";\
			make -C $$D -s $@;\
		fi;\
	done
	/bin/rm -rf single/logs
	/bin/rm -rf single/model
	/bin/rm -rf mlp/logs
	/bin/rm -rf mlp/model
	/bin/rm -rf cnn/logs
	/bin/rm -rf cnn/model

.PHONY: all clean cleanup clobber
