    ## tclapp::reset_tclstore
    ### Get current directory, used throughout script
    set launchDir [file dirname [file normalize [info script]]]
    set sourcesDir ${launchDir}/sources
    
    ### Create the project using the board local repo
    set projName "zed_example"
    set projPart "xc7z020clg484-1"
    
    create_project $projName ./$projName -part $projPart -force
    set_property board_part em.avnet.com:zed:part0:1.4 [current_project]
	

    ### User IP dir
    set_property  ip_repo_paths  { ../../hls/tcl/proj_yolo/solution1/impl/ip \
	   	                   ../../iplib/bfm_axi/gen_ip/zed \
                                 } [current_project]
    update_ip_catalog

    ### XDC 
    set XDC_LIST "./xdc/con-fmc_lpc_zed.xdc"
    add_files -fileset constrs_1 -norecurse ${XDC_LIST}
    import_files -fileset constrs_1 -norecurse ${XDC_LIST}

    ### Create block design
    create_bd_design "zed_bd" 
    
    # con-fmc
    create_bd_port -dir I SL_RST_N   
    create_bd_port -dir I SL_FLAGA   
    create_bd_port -dir I SL_FLAGB   
    create_bd_port -dir I SL_FLAGC   
    create_bd_port -dir I SL_FLAGD   
    create_bd_port -dir I -from 1 -to 0 SL_MODE
    create_bd_port -dir O SL_CS_N
    create_bd_port -dir O SL_PCLK
    create_bd_port -dir O SL_RD_N    
    create_bd_port -dir O SL_WR_N    
    create_bd_port -dir O SL_OE_N    
    create_bd_port -dir O SL_PKTEND_N
    create_bd_port -dir O -from 1 -to 0 SL_AD      
    create_bd_port -dir IO -from 31 -to 0 SL_DT      
    
    ### Generate IP on block design
	# zynq core 
    create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0
	# add zynq core slave port
    apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config\
                        {make_external "FIXED_IO, DDR" apply_board_preset "1" Master "Disable" Slave "Disable" }  [get_bd_cells processing_system7_0]
    set_property -dict [list CONFIG.PCW_USE_M_AXI_GP0 {0}] [get_bd_cells processing_system7_0]
    set_property -dict [list CONFIG.PCW_USE_S_AXI_HP0 {1}] [get_bd_cells processing_system7_0]
    set_property -dict [list CONFIG.PCW_S_AXI_HP0_DATA_WIDTH {32}] [get_bd_cells processing_system7_0]
    set_property -dict [list CONFIG.PCW_USE_FABRIC_INTERRUPT {1} CONFIG.PCW_IRQ_F2P_INTR {1}] [get_bd_cells processing_system7_0]
    set_property -dict [list CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {200}] [get_bd_cells processing_system7_0]

	# YOLO2_FPGA 
    create_bd_cell -type ip -vlnv xilinx.com:hls:YOLO2_FPGA:1.0 YOLO2_FPGA_0

    # bfm_axi_if 
    create_bd_cell -type ip -vlnv future-ds.com:user:bfm_axi_if:1.0 u_bfm
	
    create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 proc_sys_reset_0

    create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 proc_sys_reset_1

	# smart connector
    create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 smc_0
    set_property -dict [list CONFIG.NUM_SI {6}] [get_bd_cells smc_0]
    set_property -dict [list CONFIG.NUM_MI {1}] [get_bd_cells smc_0]
    set_property -dict [list CONFIG.NUM_CLKS {2}] [get_bd_cells smc_0]

    create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 smc_1
    set_property -dict [list CONFIG.NUM_SI {1}] [get_bd_cells smc_1]
    set_property -dict [list CONFIG.NUM_MI {2}] [get_bd_cells smc_1]
    set_property -dict [list CONFIG.NUM_CLKS {1}] [get_bd_cells smc_1]

    create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 axi_ic_0
    set_property -dict [list CONFIG.NUM_MI {1}] [get_bd_cells axi_ic_0]

    create_bd_cell -type ip -vlnv xilinx.com:ip:clk_wiz:6.0 clk_wiz_0
    set_property -dict [list CONFIG.PRIM_SOURCE {No_buffer} CONFIG.USE_LOCKED {false} CONFIG.USE_RESET {false}] [get_bd_cells clk_wiz_0]
    set_property -dict [list CONFIG.CLKOUT1_REQUESTED_OUT_FREQ {200}] [get_bd_cells clk_wiz_0]
    set_property -dict [list CONFIG.CLKOUT2_USED {true} CONFIG.CLKOUT2_REQUESTED_OUT_FREQ {80.000}] [get_bd_cells clk_wiz_0]
    
    ### Connection 
    connect_bd_net [get_bd_pins processing_system7_0/FCLK_CLK0] [get_bd_pins clk_wiz_0/clk_in1]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins proc_sys_reset_0/slowest_sync_clk]
    connect_bd_net [get_bd_pins processing_system7_0/FCLK_RESET0_N] [get_bd_pins proc_sys_reset_0/ext_reset_in]
    connect_bd_net [get_bd_pins proc_sys_reset_0/peripheral_aresetn] [get_bd_pins YOLO2_FPGA_0/ap_rst_n]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins YOLO2_FPGA_0/ap_clk]
	
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out2] [get_bd_pins proc_sys_reset_1/slowest_sync_clk]
    connect_bd_net [get_bd_pins processing_system7_0/FCLK_RESET0_N] [get_bd_pins proc_sys_reset_1/ext_reset_in]
    connect_bd_net [get_bd_pins proc_sys_reset_1/peripheral_aresetn] [get_bd_pins u_bfm/SYS_RST_N]
    connect_bd_net [get_bd_pins u_bfm/m_axi_aresetn] [get_bd_pins proc_sys_reset_1/peripheral_aresetn]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out2] [get_bd_pins u_bfm/SYS_CLK]
    connect_bd_net [get_bd_pins u_bfm/m_axi_aclk] [get_bd_pins clk_wiz_0/clk_out2]

    connect_bd_net [get_bd_pins proc_sys_reset_1/interconnect_aresetn] [get_bd_pins smc_1/aresetn]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out2] [get_bd_pins smc_1/aclk]
    connect_bd_intf_net [get_bd_intf_pins u_bfm/m_axi] [get_bd_intf_pins smc_1/S00_AXI]
    connect_bd_intf_net [get_bd_intf_pins smc_1/M00_AXI] [get_bd_intf_pins smc_0/S05_AXI]
    connect_bd_intf_net [get_bd_intf_pins smc_1/M01_AXI] -boundary_type upper [get_bd_intf_pins axi_ic_0/S00_AXI]
    connect_bd_net [get_bd_pins axi_ic_0/ACLK] [get_bd_pins clk_wiz_0/clk_out2]
    connect_bd_net [get_bd_pins proc_sys_reset_1/interconnect_aresetn] [get_bd_pins axi_ic_0/ARESETN]
    connect_bd_net [get_bd_pins axi_ic_0/S00_ARESETN] [get_bd_pins proc_sys_reset_1/interconnect_aresetn]
    connect_bd_net [get_bd_pins axi_ic_0/S00_ACLK] [get_bd_pins clk_wiz_0/clk_out2]
    connect_bd_net [get_bd_pins proc_sys_reset_0/interconnect_aresetn] [get_bd_pins axi_ic_0/M00_ARESETN]
    connect_bd_net [get_bd_pins axi_ic_0/M00_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins smc_0/aclk1] [get_bd_pins clk_wiz_0/clk_out2]
    connect_bd_net [get_bd_pins smc_0/aresetn] [get_bd_pins proc_sys_reset_0/interconnect_aresetn]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins smc_0/aclk]
    connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axi_ic_0/M00_AXI] [get_bd_intf_pins YOLO2_FPGA_0/s_axi_CTRL_BUS]
    connect_bd_intf_net [get_bd_intf_pins YOLO2_FPGA_0/m_axi_DATA_BUS1] [get_bd_intf_pins smc_0/S00_AXI]
    connect_bd_intf_net [get_bd_intf_pins YOLO2_FPGA_0/m_axi_DATA_BUS2] [get_bd_intf_pins smc_0/S01_AXI]
    connect_bd_intf_net [get_bd_intf_pins YOLO2_FPGA_0/m_axi_DATA_BUS3] [get_bd_intf_pins smc_0/S02_AXI]
    connect_bd_intf_net [get_bd_intf_pins YOLO2_FPGA_0/m_axi_DATA_BUS4] [get_bd_intf_pins smc_0/S03_AXI]
    connect_bd_intf_net [get_bd_intf_pins YOLO2_FPGA_0/m_axi_DATA_BUS5] [get_bd_intf_pins smc_0/S04_AXI]
    connect_bd_intf_net [get_bd_intf_pins smc_0/M00_AXI] [get_bd_intf_pins processing_system7_0/S_AXI_HP0]

    connect_bd_net [get_bd_pins processing_system7_0/S_AXI_HP0_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins YOLO2_FPGA_0/interrupt] [get_bd_pins processing_system7_0/IRQ_F2P]
    
    connect_bd_net [get_bd_ports SL_RST_N] [get_bd_pins u_bfm/SL_RST_N]
    connect_bd_net [get_bd_ports SL_FLAGA] [get_bd_pins u_bfm/SL_FLAGA]
    connect_bd_net [get_bd_ports SL_FLAGB] [get_bd_pins u_bfm/SL_FLAGB]
    connect_bd_net [get_bd_ports SL_FLAGC] [get_bd_pins u_bfm/SL_FLAGC]
    connect_bd_net [get_bd_ports SL_FLAGD] [get_bd_pins u_bfm/SL_FLAGD]
    connect_bd_net [get_bd_ports SL_MODE]  [get_bd_pins u_bfm/SL_MODE]
    connect_bd_net [get_bd_ports SL_DT]    [get_bd_pins u_bfm/SL_DT]
    connect_bd_net [get_bd_ports SL_CS_N]  [get_bd_pins u_bfm/SL_CS_N]
    connect_bd_net [get_bd_ports SL_AD]    [get_bd_pins u_bfm/SL_AD]
    connect_bd_net [get_bd_ports SL_OE_N]  [get_bd_pins u_bfm/SL_OE_N]
    connect_bd_net [get_bd_ports SL_PCLK]  [get_bd_pins u_bfm/SL_PCLK]
    connect_bd_net [get_bd_ports SL_WR_N]  [get_bd_pins u_bfm/SL_WR_N]
    connect_bd_net [get_bd_ports SL_RD_N]  [get_bd_pins u_bfm/SL_RD_N]
    connect_bd_net [get_bd_ports SL_PKTEND_N] [get_bd_pins u_bfm/SL_PKTEND_N]
	
    ### set address
    assign_bd_address
    set_property offset 0x43C00000 [get_bd_addr_segs {u_bfm/m_axi/SEG_YOLO2_FPGA_0_Reg}]

    ### save block design 
    regenerate_bd_layout
    validate_bd_design
    save_bd_design
    
    ### Create top wrapper  
    make_wrapper -files [get_files ./$projName/$projName.srcs/sources_1/bd/zed_bd/zed_bd.bd] -top
    add_files -norecurse ./$projName/$projName.srcs/sources_1/bd/zed_bd/hdl/zed_bd_wrapper.v
   
    ### Synthesis   
    launch_runs synth_1 -jobs 16
    wait_on_run synth_1
    
    ### implementation and Bit file generation 
    launch_runs impl_1 -to_step write_bitstream -jobs 16
    wait_on_run impl_1
    
    #### copy hardware design files to sw directory  
    #file mkdir ./$projName/$projName.sdk
    #file copy -force ./$projName/$projName.runs/impl_1/zed_bd_wrapper.sysdef ./$projName/$projName.sdk/zed_bd_wrapper.hdf
    #file copy -force ./$projName/$projName.runs/impl_1/zed_bd_wrapper.bit ./$projName/$projName.sdk/zed_bd_wrapper.bit
