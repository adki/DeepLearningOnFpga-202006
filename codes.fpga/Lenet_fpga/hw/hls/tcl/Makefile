#-------------------------------------------------------------------------------
SHELL	=/bin/bash

#------------------------------------------------------------------
ifeq ($(MAKECMDGOALS),)
ifndef XILINX_VIVADO_HLS
       $(error XILINX_VIVADO_HLS environment variable not defined)
endif
endif
ifeq ($(MAKECMDGOALS),all)
ifndef XILINX_VIVADO_HLS
       $(error XILINX_VIVADO_HLS environment variable not defined)
endif
endif

#------------------------------------------------------------------
export VIVADO_HLS  = vivado_hls
export TOP        ?= lenet_wrapper
export PROJECT    ?= proj_lenet
export SOLUTION   ?= solution1
export PART       ?= xc7z020clg484-1

#-------------------------------------------------------------------------------
all: syn

syn:
	$(VIVADO_HLS) -f script.tcl

open:
	$(VIVADO_HLS) -p proj_lenet


#-------------------------------------------------------------------------------
clean:
	@\rm -f  vivado_hls.log

cleanup clobber: clean
	@if [ -d proj_lenet ]; then \rm -fr proj_lenet; fi

cleanupall distclean: cleanup

#-------------------------------------------------------------------------------
.PHONY: all syn open clean cleanup cleanupall distclean
#-------------------------------------------------------------------------------
