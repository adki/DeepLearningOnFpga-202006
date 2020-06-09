#-------------------------------------------------------------------------------
SHELL	=/bin/bash

#-------------------------------------------------------------------------------
ifeq ($(MAKECMDGOALS),)
ifndef XILINX_VIVADO
       $(error XILINX_VIVADO environment variable not defined)
endif
endif
ifeq ($(MAKECMDGOALS),all)
ifndef XILINX_VIVADO
       $(error XILINX_VIVADO environment variable not defined)
endif
endif
export VIVADO = $(XILINX_VIVADO)/bin/vivado

export GUI         ?= 1
export FIXED_POINT ?= 0
#-------------------------------------------------------------------------------
all:
	if [ "$(GUI)" = "1" ]; then\
		$(VIVADO) -mode gui -source run_zed_example.tcl;\
	else\
		$(VIVADO) -mode batch -source run_zed_example.tcl;\
	fi

#-------------------------------------------------------------------------------
.PHONY: all clean cleanup

clean:
	@\rm -f  vivado.jou
	@\rm -f  vivado.log
	@\rm -f  vivado_*.backup.jou
	@\rm -f  vivado_*.backup.log
	@\rm -f  hs_err_*.log
	@\rm -f  vivado_pid*.str
	@\rm -f  vivado_pid*.zip
	@if [ -d NA ]; then \rm -fr NA; fi
	@if [ -d .Xil ]; then \rm -fr .Xil; fi
	@if [ -d project_1 ]; then \rm -fr project_1; fi
	@if [ -d hd_visual ]; then \rm -fr hd_visual; fi

cleanup clobber: clean
	@if [ -d zed_example ]; then \rm -fr zed_example; fi

cleanupall distclean: cleanup
	@/bin/rm -f zed_bd_wrapper.bit
	@/bin/rm -f zed_bd_wrapper_fixed.bit

#-------------------------------------------------------------------------------
