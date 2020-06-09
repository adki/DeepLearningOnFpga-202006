SHELL=/bin/bash
ARCH=$(shell uname -s)
ifeq ($(findstring MINGW,$(ARCH)),MINGW)
      PLATFORM=mingw
else ifeq ($(findstring CYGWIN,$(ARCH)),CYGWIN)
      PLATFORM=cygwin
else ifeq ($(findstring Linux,$(ARCH)),Linux)
      PLATFORM=linux
endif
KERN:=$(PLATFORM)
MACHINE:=$(shell uname -m)
MACH:=$(MACHINE)
PROCESSOR:=$(uname -p)

ifeq ($(MAKECMDGOALS),)
ifndef CONFMC_HOME
       $(error CONFMC_HOME environment variable not defined)
endif
endif
ifeq ($(MAKECMDGOALS),all)
ifndef CONFMC_HOME
       $(error CONFMC_HOME environment variable not defined)
endif
endif

OBJECTDIR ?= obj
ifeq (${wildcard $(OBJECTDIR)},)
  DUMMY:= $(shell mkdir $(OBJECTDIR))
endif

PROG    = yolov2
SRCS	= main.cpp trx_axi_api.c
OBJS	= main.o trx_axi_api.o

all: $(addprefix $(OBJECTDIR)/,$(OBJS))
	g++ -O3 -o $(PROG) $^\
		-I$(CONFMC_HOME)/include\
		`pkg-config opencv --cflags --libs`\
		-L$(CONFMC_HOME)/lib/$(PLATFORM)_$(MACHINE) -lconapi\
		-lusb-1.0

$(OBJECTDIR)/main.o: src/main.cpp
	g++ -O3 -DUSE_CON_FMC -DSILENCE\
		-I$(CONFMC_HOME)/include\
		-c $< -o $@

$(OBJECTDIR)/trx_axi_api.o: src/trx_axi_api.c
	gcc -O3 -I$(CONFMC_HOME)/include -c $< -o $@

run:
	./$(PROG)

run.cam:
	./$(PROG) --camera=1

clean:
	/bin/rm -rf $(OBJECTDIR)
	/bin/rm -f  $(PROG)
	/bin/rm -f  sample.dat
	/bin/rm -f  predictions.png  sized.png captured_image.jpg

cleanup: clean

cleanupall clobber distclean: cleanup

.PHONY: clean cleanup clobber cleanupall distclean
