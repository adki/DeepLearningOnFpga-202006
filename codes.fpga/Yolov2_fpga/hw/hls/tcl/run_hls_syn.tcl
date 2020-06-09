#******************************************************************************
# Create a project
open_project $::env(PROJECT)

# Set the top-level function
set_top $::env(TOP)

set DIR_SRC  ../src
set DIR_TB   ../tb

# Add design files
add_files ${DIR_SRC}/cnn.cpp
add_files ${DIR_SRC}/cnn.h

# Add test bench & files
add_files -tb ${DIR_TB}/src/main.cpp
add_files -tb ${DIR_TB}/src/yolov2.h
add_files -tb ${DIR_TB}/src/stb_image_write.h
add_files -tb ${DIR_TB}/src/stb_image.h
add_files -tb ${DIR_TB}/src/labels
add_files -tb ${DIR_TB}/src/data/yolov2.cfg
add_files -tb ${DIR_TB}/src/data/coco.names
add_files -tb ${DIR_TB}/src/data/kite.jpg
add_files -tb ${DIR_TB}/src/data/biasv2_comb_ap16.bin
add_files -tb ${DIR_TB}/src/data/biasv2_comb_ap16_maxQ_23.bin
add_files -tb ${DIR_TB}/src/data/weightsv2_comb_reorg_ap16.bin
add_files -tb ${DIR_TB}/src/data/weightsv2_comb_reorg_ap16_maxQ_23.bin
add_files -tb ${DIR_TB}/src/data/yolov2_ap16_inout_maxQ_24.bin

# ########################################################
# Create a solution
open_solution $::env(SOLUTION)
# Define technology and clock rate
set_part  $::env(PART)
create_clock -period 6 -name default
#config_bind -effort high
#config_schedule -effort high
csynth_design
export_design -format ip_catalog
tclapp::reset_tclstore
exit
