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
export TOP        ?= YOLO2_FPGA
export PROJECT    ?= proj_yolo
export SOLUTION   ?= solution1
export PART       ?= xc7z020clg484-1

#-------------------------------------------------------------------------------
all: syn

sim:
	$(VIVADO_HLS) -f run_hls_sim.tcl

syn:
	$(VIVADO_HLS) -f run_hls_syn.tcl

open:
	$(VIVADO_HLS) -p proj_yolo


#-------------------------------------------------------------------------------
.PHONY: clean cleanup clobber cleanupall distclean

clean:
	@\rm -f  vivado_hls.log

cleanup clobber: clean
	@if [ -d proj_yolo_sim ]; then \rm -fr proj_yolo_sim; fi
	@if [ -d proj_yolo ]; then \rm -fr proj_yolo; fi

cleanupall distclean: cleanup

#-------------------------------------------------------------------------------
