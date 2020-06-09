#-------------------------------------------------------------------------------
SHELL	=/bin/bash

#-------------------------------------------------------------------------------
export VIVADO = xsdk
#export VIVADO = $(XILINX_SDK)/bin/xsdk


#-------------------------------------------------------------------------------
all:
	$(VIVADO) -batch -source run_xsct.tcl

#-------------------------------------------------------------------------------
.PHONY: clean cleanup

clean:
	@\rm -f  vivado.jou
	@\rm -f  vivado.log
	@\rm -f  vivado_*.backup.jou
	@\rm -f  vivado_*.backup.log
	@\rm -f  vivado_pid*.str
	@\rm -f  vivado_pid*.zip
	@if [ -d .Xil ]; then \rm -fr .Xil; fi
	@if [ -d project_1 ]; then \rm -fr project_1; fi
	@if [ -d hd_visual ]; then \rm -fr hd_visual; fi
	@if [ -d fsbl_workspace ]; then \rm -fr fsbl_workspace; fi

#-------------------------------------------------------------------------------
