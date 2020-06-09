#-------------------------------------------------------------------------------
SHELL	=/bin/bash

#------------------------------------------------------------------
ifeq ($(MAKECMDGOALS),)
ifndef XILINX_SDK
       $(error XILINX_SDK environment variable not defined)
endif
endif
ifeq ($(MAKECMDGOALS),all)
ifndef XILINX_SDK
       $(error XILINX_SDK environment variable not defined)
endif
endif

#-------------------------------------------------------------------------------
export FIXED_POINT ?= 0
export BOOTGEN      = $(XILINX_SDK)/bin/bootgen
export PROG_FLASH   = $(XILINX_SDK)/bin/program_flash
export BOOT_FILE    = BOOT.bin
export BIF_FILE     = zed_bd.bif
export FSBL_FILE    = fsbl/fsbl_workspace/fsbl/Debug/fsbl.elf
export ELF_FILE     = hello/Debug/hello.elf
ifndef FIXED_POINT
#export BIT_FILE     = ../zed_example/zed_example.runs/impl_1/zed_bd_wrapper.bit
export BIT_FILE     = ../zed_bd_wrapper.bit
else ifeq ($(FIXED_POINT),0)
#export BIT_FILE     = ../zed_example/zed_example.runs/impl_1/zed_bd_wrapper.bit
export BIT_FILE     = ../zed_bd_wrapper.bit
else
#export BIT_FILE     = ../zed_example/zed_example.runs/impl_1/zed_bd_wrapper_fixed.bit
export BIT_FILE     = ../zed_bd_wrapper_fixed.bit
endif

#-------------------------------------------------------------------------------
all: boot

boot: bif
	$(BOOTGEN) -image $(BIF_FILE) -arch zynq -o $(BOOT_FILE) -w on

bif:
	@if [ ! -f ${BIT_FILE} ]; then echo "${BIT_FILE} not found"; exit; fi
	@if [ -f ${BIF_FILE} ]; then /bin/rm -f ${BIF_FILE}; fi
	echo "//arch = zynq; split = false; format = BIN" >  ${BIF_FILE}
	echo "the_ROM_image:"                             >> ${BIF_FILE}
	echo "{"                                          >> ${BIF_FILE}
	echo "  [bootloader]${FSBL_FILE}"                 >> ${BIF_FILE}
	echo "  ${BIT_FILE}"                              >> ${BIF_FILE}
	echo "  ${ELF_FILE}"                              >> ${BIF_FILE}
	echo "}"                                          >> ${BIF_FILE}

prog:
	@if [ ! -f ${BOOT_FILE} ]; then echo "${BOOT_FILE} not found"; exit; fi
	@if [ ! -f ${BIT_FILE} ]; then echo "${BIT_FILE} not found"; exit; fi
	$(PROG_FLASH) -f $(BOOT_FILE) -fsbl $(FSBL_FILE)\
		-flash_type qspi_single -verify\
		-cable type xilinx_tcf url TCP:127.0.0.1:3121

#-------------------------------------------------------------------------------
.PHONY: clean cleanup cleanupall distclean

clean:
	@\rm -f  $(BOOT_FILE)
	@\rm -f  vivado.log

cleanup: clean

cleanupall disclean: cleanup
	/bin/rm -f $(BIF_FILE)

#-------------------------------------------------------------------------------
