if {[info exists env(FIXED_POINT)] == 0} {
    set DIR_IP ../../hls/tcl/proj_lenet/solution1/impl/ip
} else {
    if { $::env(FIXED_POINT) == 0 } {
        set DIR_IP ../../hls/tcl/proj_lenet/solution1/impl/ip
    } else {
        set DIR_IP ../../hls/tcl.fixed/proj_lenet/solution1/impl/ip
    }
}

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
    set IP_DIR_LIST "${DIR_IP} ../../iplib/bfm_axi/gen_ip/zed"
    set_property  ip_repo_paths  ${IP_DIR_LIST} [current_project]
    update_ip_catalog

    ### XDC 
    set XDC_LIST "./xdc/con-fmc_lpc_zed.xdc ./xdc/fpga_zed.xdc ./xdc/ila.xdc"
    add_files -fileset constrs_1 -norecurse ${XDC_LIST}
    import_files -fileset constrs_1 -norecurse ${XDC_LIST}

    ### Create block design
    create_bd_design "zed_bd" 
    
    create_bd_port -dir I BOARD_CLK_IN   

    set BOARD_RST_SW             [ create_bd_port -dir I -type rst BOARD_RST_SW ];
    set_property -dict [ list CONFIG.POLARITY {ACTIVE_HIGH} ] $BOARD_RST_SW;

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
    # clk 
    create_bd_cell -type ip -vlnv xilinx.com:ip:clk_wiz:6.0 clk_wiz_0
    set_property -dict [list CONFIG.CLKOUT1_REQUESTED_OUT_FREQ {80} \
                             CONFIG.USE_LOCKED {false} \
                             CONFIG.USE_RESET {false} \
                             ] [get_bd_cells clk_wiz_0]
    
    # inter con 
    create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 axi_interconnect_0
    create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 axi_interconnect_1
    set_property -dict [list CONFIG.NUM_SI {2} CONFIG.NUM_MI {1}] [get_bd_cells axi_interconnect_1]

    # conv_net 
    create_bd_cell -type ip -vlnv xilinx.com:hls:lenet_wrapper:1.0 lenet_wrapper

    # bfm_axi_if 
    create_bd_cell -type ip -vlnv future-ds.com:user:bfm_axi_if:1.0 u_bfm

    create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 proc_sys_reset_0

    create_bd_cell -type ip -vlnv xilinx.com:ip:axi_bram_ctrl:4.1 axi_bram_ctrl_0
    set_property -dict [list CONFIG.SINGLE_PORT_BRAM {1}] [get_bd_cells axi_bram_ctrl_0]
    apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM "Auto" }  [get_bd_intf_pins axi_bram_ctrl_0/BRAM_PORTA]
    
    ### Connection 
    connect_bd_net [get_bd_pins proc_sys_reset_0/peripheral_aresetn] [get_bd_pins u_bfm/SYS_RST_N]
    connect_bd_net [get_bd_pins u_bfm/m_axi_aresetn] [get_bd_pins proc_sys_reset_0/peripheral_aresetn]
    
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

    connect_bd_net [get_bd_pins proc_sys_reset_0/peripheral_aresetn] [get_bd_pins axi_bram_ctrl_0/s_axi_aresetn]

    connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axi_interconnect_0/M01_AXI] [get_bd_intf_pins lenet_wrapper/s_axi_axilite]

    connect_bd_net [get_bd_pins lenet_wrapper/ap_rst_n] [get_bd_pins proc_sys_reset_0/peripheral_aresetn]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins proc_sys_reset_0/slowest_sync_clk]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins u_bfm/SYS_CLK]
    connect_bd_net [get_bd_pins u_bfm/m_axi_aclk] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins lenet_wrapper/ap_clk] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins axi_bram_ctrl_0/s_axi_aclk] [get_bd_pins clk_wiz_0/clk_out1]
	
    connect_bd_net [get_bd_ports BOARD_CLK_IN] [get_bd_pins clk_wiz_0/clk_in1]
    connect_bd_net [get_bd_ports BOARD_RST_SW] [get_bd_pins proc_sys_reset_0/ext_reset_in]

    connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axi_interconnect_0/ACLK]
    connect_bd_net [get_bd_pins axi_interconnect_0/S00_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins axi_interconnect_0/M00_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins axi_interconnect_0/M01_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins proc_sys_reset_0/interconnect_aresetn] [get_bd_pins axi_interconnect_0/ARESETN]
    connect_bd_net [get_bd_pins axi_interconnect_0/S00_ARESETN] [get_bd_pins proc_sys_reset_0/interconnect_aresetn]
    connect_bd_net [get_bd_pins axi_interconnect_0/M00_ARESETN] [get_bd_pins proc_sys_reset_0/interconnect_aresetn]
    connect_bd_net [get_bd_pins axi_interconnect_0/M01_ARESETN] [get_bd_pins proc_sys_reset_0/interconnect_aresetn]
    connect_bd_intf_net [get_bd_intf_pins u_bfm/m_axi] -boundary_type upper [get_bd_intf_pins axi_interconnect_0/S00_AXI]

    connect_bd_intf_net [get_bd_intf_pins lenet_wrapper/m_axi_memorybus] -boundary_type upper [get_bd_intf_pins axi_interconnect_1/S00_AXI]
    connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axi_interconnect_0/M00_AXI] [get_bd_intf_pins axi_interconnect_1/S01_AXI]
    connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axi_interconnect_1/M00_AXI] [get_bd_intf_pins axi_bram_ctrl_0/S_AXI]
    connect_bd_net [get_bd_pins clk_wiz_0/clk_out1] [get_bd_pins axi_interconnect_1/ACLK]
    connect_bd_net [get_bd_pins axi_interconnect_1/S00_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins axi_interconnect_1/M00_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins axi_interconnect_1/S01_ACLK] [get_bd_pins clk_wiz_0/clk_out1]
    connect_bd_net [get_bd_pins proc_sys_reset_0/interconnect_aresetn] [get_bd_pins axi_interconnect_1/ARESETN]
    connect_bd_net [get_bd_pins axi_interconnect_1/S00_ARESETN] [get_bd_pins proc_sys_reset_0/interconnect_aresetn]
    connect_bd_net [get_bd_pins axi_interconnect_1/M00_ARESETN] [get_bd_pins proc_sys_reset_0/interconnect_aresetn]
    connect_bd_net [get_bd_pins axi_interconnect_1/S01_ARESETN] [get_bd_pins proc_sys_reset_0/interconnect_aresetn]

    ### set address
    assign_bd_address
    set_property offset 0x00000000 [get_bd_addr_segs {lenet_wrapper/Data_m_axi_memorybus/SEG_axi_bram_ctrl_0_Mem0}]
    set_property offset 0x00000000 [get_bd_addr_segs {u_bfm/m_axi/SEG_axi_bram_ctrl_0_Mem0}]
    set_property offset 0xC0000000 [get_bd_addr_segs {u_bfm/m_axi/SEG_lenet_wrapper_Reg}]

    ### save block design 
    regenerate_bd_layout
    validate_bd_design
    save_bd_design

    ### Create top wrapper  
    make_wrapper -files [get_files ./$projName/$projName.srcs/sources_1/bd/zed_bd/zed_bd.bd] -top
    add_files -norecurse ./$projName/$projName.srcs/sources_1/bd/zed_bd/hdl/zed_bd_wrapper.v

    ### Synthesis   
    launch_runs synth_1 -jobs 8
    wait_on_run synth_1
    
    ### implementation and Bit file generation 
    launch_runs impl_1 -to_step write_bitstream -jobs 8
    wait_on_run impl_1
    open_run impl_1
    if { $::env(FIXED_POINT) == 0 } {
        write_bitstream -force zed_bd_wrapper.bit
    } else {
        write_bitstream -force zed_bd_wrapper_fixed.bit
    }
    
    ### copy hardware design files to sw directory  
    file mkdir ./$projName/$projName.sdk
    file copy -force ./$projName/$projName.runs/impl_1/zed_bd_wrapper.sysdef ./$projName/$projName.sdk/zed_bd_wrapper.hdf
    if { $::env(FIXED_POINT) == 0 } {
        file copy -force ./$projName/$projName.runs/impl_1/zed_bd_wrapper.bit ./$projName/$projName.sdk/zed_bd_wrapper.bit
    } else {
        file copy -force ./$projName/$projName.runs/impl_1/zed_bd_wrapper.bit ./$projName/$projName.sdk/zed_bd_wrapper_fixed.bit
    }
