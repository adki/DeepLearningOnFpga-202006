// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
// Date        : Wed Jan  8 06:15:09 2020
// Host        : KS-PC running 64-bit Service Pack 1  (build 7601)
// Command     : write_verilog -force -mode synth_stub bfm_axi_stub.v
// Design      : bfm_axi
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7z045ffg900-2
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module bfm_axi(SYS_CLK_STABLE, SYS_CLK, SYS_RST_N, SL_RST_N, 
  SL_CS_N, SL_PCLK, SL_AD, SL_FLAGA, SL_FLAGB, SL_FLAGC, SL_FLAGD, SL_RD_N, SL_WR_N, SL_OE_N, 
  SL_PKTEND_N, SL_DT_I, SL_DT_O, SL_DT_T, SL_MODE, ARESETn, ACLK, MID, AWID, AWADDR, AWLEN, AWLOCK, AWSIZE, 
  AWBURST, AWCACHE, AWPROT, AWVALID, AWREADY, AWQOS, AWREGION, WID, WDATA, WSTRB, WLAST, WVALID, WREADY, BID, 
  BRESP, BVALID, BREADY, ARID, ARADDR, ARLEN, ARLOCK, ARSIZE, ARBURST, ARCACHE, ARPROT, ARVALID, ARREADY, 
  ARQOS, ARREGION, RID, RDATA, RRESP, RLAST, RVALID, RREADY, IRQ, FIQ, GPOUT, GPIN)
/* synthesis syn_black_box black_box_pad_pin="SYS_CLK_STABLE,SYS_CLK,SYS_RST_N,SL_RST_N,SL_CS_N,SL_PCLK,SL_AD[1:0],SL_FLAGA,SL_FLAGB,SL_FLAGC,SL_FLAGD,SL_RD_N,SL_WR_N,SL_OE_N,SL_PKTEND_N,SL_DT_I[31:0],SL_DT_O[31:0],SL_DT_T,SL_MODE[1:0],ARESETn,ACLK,MID[3:0],AWID[3:0],AWADDR[31:0],AWLEN[7:0],AWLOCK,AWSIZE[2:0],AWBURST[1:0],AWCACHE[3:0],AWPROT[2:0],AWVALID,AWREADY,AWQOS[3:0],AWREGION[3:0],WID[3:0],WDATA[31:0],WSTRB[3:0],WLAST,WVALID,WREADY,BID[3:0],BRESP[1:0],BVALID,BREADY,ARID[3:0],ARADDR[31:0],ARLEN[7:0],ARLOCK,ARSIZE[2:0],ARBURST[1:0],ARCACHE[3:0],ARPROT[2:0],ARVALID,ARREADY,ARQOS[3:0],ARREGION[3:0],RID[3:0],RDATA[31:0],RRESP[1:0],RLAST,RVALID,RREADY,IRQ,FIQ,GPOUT[15:0],GPIN[15:0]" */;
  input SYS_CLK_STABLE;
  input SYS_CLK;
  output SYS_RST_N;
  input SL_RST_N;
  output SL_CS_N;
  output SL_PCLK;
  output [1:0]SL_AD;
  input SL_FLAGA;
  input SL_FLAGB;
  input SL_FLAGC;
  input SL_FLAGD;
  output SL_RD_N;
  output SL_WR_N;
  output SL_OE_N;
  output SL_PKTEND_N;
  input [31:0]SL_DT_I;
  output [31:0]SL_DT_O;
  output SL_DT_T;
  input [1:0]SL_MODE;
  input ARESETn;
  input ACLK;
  input [3:0]MID;
  output [3:0]AWID;
  output [31:0]AWADDR;
  output [7:0]AWLEN;
  output AWLOCK;
  output [2:0]AWSIZE;
  output [1:0]AWBURST;
  output [3:0]AWCACHE;
  output [2:0]AWPROT;
  output AWVALID;
  input AWREADY;
  output [3:0]AWQOS;
  output [3:0]AWREGION;
  output [3:0]WID;
  output [31:0]WDATA;
  output [3:0]WSTRB;
  output WLAST;
  output WVALID;
  input WREADY;
  input [3:0]BID;
  input [1:0]BRESP;
  input BVALID;
  output BREADY;
  output [3:0]ARID;
  output [31:0]ARADDR;
  output [7:0]ARLEN;
  output ARLOCK;
  output [2:0]ARSIZE;
  output [1:0]ARBURST;
  output [3:0]ARCACHE;
  output [2:0]ARPROT;
  output ARVALID;
  input ARREADY;
  output [3:0]ARQOS;
  output [3:0]ARREGION;
  input [3:0]RID;
  input [31:0]RDATA;
  input [1:0]RRESP;
  input RLAST;
  input RVALID;
  output RREADY;
  input IRQ;
  input FIQ;
  output [15:0]GPOUT;
  input [15:0]GPIN;
endmodule
