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

ifndef OBJECTDIR
  OBJECTDIR = obj
endif
ifeq (${wildcard $(OBJECTDIR)},)
  DUMMY:= $(shell mkdir $(OBJECTDIR))
endif
ifeq (${wildcard compile.log},)
  DUMMY:= $(shell /bin/rm -f compile.log)
endif

PROG   = lenet
SRCCXX = main.cpp
SRCC   = trx_axi_api.c
OBJS   = $(SRCCXX:.cpp=.o) $(SRCC:.c=.o)

CC          = g++
DEFINES     = -DRIGOR -DUSE_OPENCV -DSILENCE
INCDIRS     = -Isrc.fixed -I$(CONFMC_HOME)/include
CFLAGS     += -O3
LDFLAGS    += 
CONFMC      = -L$(CONFMC_HOME)/lib/$(PLATFORM)_$(MACHINE) -lconapi -lusb-1.0
OPENCV      = `pkg-config opencv --cflags --libs`
LIBS       += $(OPENCV) $(CONFMC)
ifdef FIXED_POINT
DEFINES    += -DFIXED_POINT -DDTYPE="ap_fixed<32,8>"
INCDIRS    += -I/opt/XilinxWebpack/Vivado/2018.3/include
endif

vpath %.cpp src.fixed
vpath %.c   src.fixed
ifdef FIXED_POINT
vpath %.h   src.fixed /opt/XilinxWebpack/Vivado/2018.3/include
else
vpath %.h   src.fixed
endif

$(OBJECTDIR)/%.o: %.c
	$(CC) -c $(DEFINES) $(CFLAGS) $(INCDIRS) -o $@ $<

$(OBJECTDIR)/%.o: %.cpp
	$(CC) -c $(DEFINES) $(CFLAGS) $(INCDIRS) -o $@ $<

all: $(addprefix $(OBJECTDIR)/,$(OBJS))
	$(CC) -o $(PROG) $^ $(LDFLAGS) $(LIBS)

run:
	./$(PROG) ./images/0.png

run.all:
	for N in 0 1 2 3 4 5 6 7 8 9; do\
		echo "./$(PROG) ./images/$$N.png";\
		./$(PROG) ./images/$$N.png;\
	done

clean:
	/bin/rm -rf $(OBJECTDIR)
	/bin/rm -f  $(PROG)

cleanup: clean

cleanupall clobber distclean: cleanup

.PHONY: all run clean cleanup clobber cleanupall distclean
