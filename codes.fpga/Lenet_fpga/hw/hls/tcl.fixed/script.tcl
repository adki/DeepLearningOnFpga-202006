############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 2015 Xilinx Inc. All rights reserved.
############################################################
open_project $::env(PROJECT)

set_top $::env(TOP)

set DIR_SRC ../src.fixed
set DIR_TB  ../tb

add_files ${DIR_SRC}/biases.h     -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/conv.cpp     -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/conv_net.cpp -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/conv_net.h   -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/flatten.cpp  -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/linear.cpp   -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/pooling.cpp  -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/relu.cpp     -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files ${DIR_SRC}/weights.h    -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"

add_files -tb ${DIR_TB}/src/conv_net_tb.cpp -cflags "-DFIXED_POINT=1 -DDTYPE=ap_fixed<32,8>"
add_files -tb ${DIR_TB}/data/input_10.dat
add_files -tb ${DIR_TB}/data/input_5.dat
add_files -tb ${DIR_TB}/data/out_10.gold.dat
add_files -tb ${DIR_TB}/data/out_5.gold.dat

open_solution $::env(SOLUTION)
set_part $::env(PART)
create_clock -period 10 -name default
#source "./conv_net/baseline/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -format ip_catalog
tclapp::reset_tclstore
exit
