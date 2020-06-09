//------------------------------------------------------------------------------
// Copyright (c) 2018 by Future Design Systems Co., Ltd.
// All right reserved
// http://www.future-ds.com
//------------------------------------------------------------------------------
// fpga.v
//------------------------------------------------------------------------------
// VERSION: 2018.03.12.
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
module bfm_axi_if
(
     //-------------------------------------------------------------------------
       input   wire          SYS_CLK  
     , input   wire          SYS_RST_N  
     //-------------------------------------------------------------------------
     , input   wire          SL_RST_N      // synthesis xc_pullup = 1
     , output  wire          SL_CS_N
     , output  wire          SL_PCLK
     , input   wire          SL_FLAGA      // synthesis xc_pulldown = 1
     , input   wire          SL_FLAGB      // synthesis xc_pulldown = 1
     , input   wire          SL_FLAGC      // synthesis xc_pulldown = 1
     , input   wire          SL_FLAGD      // synthesis xc_pulldown = 1
     , output  wire          SL_RD_N       // IF_RD
     , output  wire          SL_WR_N       // IF_WR
     , output  wire          SL_OE_N       // IF_OE
     , output  wire          SL_PKTEND_N   // IF_PKTEND
     , output  wire  [ 1:0]  SL_AD         // IF_ADDR[1:0]
     , inout   wire  [31:0]  SL_DT         // IF_DATA[31:0]
     , input   wire  [ 1:0]  SL_MODE
     //-------------------------------------------------------------------------
     , input  wire                     m_axi_aclk
     , input  wire                     m_axi_aresetn
     //-------------------------------------------------------------------------
     , output wire [ 3:0]              m_axi_awid
     , output wire [31:0]              m_axi_awaddr
     , output wire [ 7:0]              m_axi_awlen
     , output wire                     m_axi_awlock
     , output wire [ 2:0]              m_axi_awsize
     , output wire [ 1:0]              m_axi_awburst
     , output wire [ 3:0]              m_axi_awcache
     , output wire [ 2:0]              m_axi_awprot
     , output wire                     m_axi_awvalid
     , input  wire                     m_axi_awready
     , output wire [ 3:0]              m_axi_awqos
     , output wire [ 3:0]              m_axi_awregion
     //-------------------------------------------------------------------------
     , output wire [ 3:0]              m_axi_wid
     , output wire [31:0]              m_axi_wdata
     , output wire [ 3:0]              m_axi_wstrb
     , output wire                     m_axi_wlast
     , output wire                     m_axi_wvalid
     , input  wire                     m_axi_wready
     //-------------------------------------------------------------------------
     , input  wire [ 3:0]              m_axi_bid
     , input  wire [ 1:0]              m_axi_bresp
     , input  wire                     m_axi_bvalid
     , output wire                     m_axi_bready
     //-------------------------------------------------------------------------
     , output wire [ 3:0]              m_axi_arid
     , output wire [31:0]              m_axi_araddr
     , output wire [ 7:0]              m_axi_arlen
     , output wire                     m_axi_arlock
     , output wire [ 2:0]              m_axi_arsize
     , output wire [ 1:0]              m_axi_arburst
     , output wire [ 3:0]              m_axi_arcache
     , output wire [ 2:0]              m_axi_arprot
     , output wire                     m_axi_arvalid
     , input  wire                     m_axi_arready
     , output wire [ 3:0]              m_axi_arqos
     , output wire [ 3:0]              m_axi_arregion
     //-------------------------------------------------------------------------
     , input  wire [ 3:0]              m_axi_rid
     , input  wire [31:0]              m_axi_rdata
     , input  wire [ 1:0]              m_axi_rresp
     , input  wire                     m_axi_rlast
     , input  wire                     m_axi_rvalid
     , output wire                     m_axi_rready
     //-------------------------------------------------------------------------
);
    //--------------------------------------------------------------------------
    // synthesis attribute IOB of SL_DT is "TRUE";
    wire [31:0]  SL_DT_I;
    wire [31:0]  SL_DT_O;
    wire         SL_DT_T;
    //assign SL_DT_I = SL_DT;
    //assign SL_DT   = (SL_DT_T==1'b0) ? SL_DT_O : 32'hZ;

    //--------------------------------------------------------------------------
    //wire [31:0]  m_axi_awaddr_int;
    //wire [31:0]  m_axi_araddr_int;
	//assign m_axi_awaddr = m_axi_awaddr_int;
	//assign m_axi_araddr = m_axi_araddr_int;
    //--------------------------------------------------------------------------
    generate
    genvar idx_usb;
    for (idx_usb=0; idx_usb<32; idx_usb=idx_usb+1) begin : IDX_SL_DT
         IOBUF IOPAD_SL_DT ( .IO( SL_DT   [idx_usb] ),
                             .T ( SL_DT_T           ),
                             .I ( SL_DT_O [idx_usb] ),
                             .O ( SL_DT_I [idx_usb] )
         );
    end
    endgenerate
    //--------------------------------------------------------------------------
    bfm_axi
    u_bfm_axi (
           .SYS_CLK_STABLE  ( SYS_RST_N      )
         , .SYS_CLK         ( SYS_CLK        )
         , .SYS_RST_N       ( )
         , .SL_RST_N        ( SL_RST_N       )
         , .SL_CS_N         ( SL_CS_N        )
         , .SL_PCLK         ( SL_PCLK        )
         , .SL_AD           ( SL_AD          )
         , .SL_FLAGA        ( SL_FLAGA       )
         , .SL_FLAGB        ( SL_FLAGB       )
         , .SL_FLAGC        ( SL_FLAGC       )
         , .SL_FLAGD        ( SL_FLAGD       )
         , .SL_RD_N         ( SL_RD_N        )
         , .SL_WR_N         ( SL_WR_N        )
         , .SL_OE_N         ( SL_OE_N        )
         , .SL_PKTEND_N     ( SL_PKTEND_N    )
         , .SL_DT_I         ( SL_DT_I        )
         , .SL_DT_O         ( SL_DT_O        )
         , .SL_DT_T         ( SL_DT_T        )
         , .SL_MODE         ( SL_MODE        )
         , .ARESETn  ( m_axi_aresetn  )
         , .ACLK     ( m_axi_aclk     )
         , .MID      ( 4'h1           )
         , .AWID     ( m_axi_awid     ) //[AXI_WIDTH_ID-1:0]
         , .AWADDR   ( m_axi_awaddr)
         , .AWLEN    ( m_axi_awlen    )
         , .AWLOCK   ( m_axi_awlock   )
         , .AWSIZE   ( m_axi_awsize   )
         , .AWBURST  ( m_axi_awburst  )
         , .AWCACHE  ( m_axi_awcache  )
         , .AWPROT   ( m_axi_awprot   )
         , .AWVALID  ( m_axi_awvalid  )
         , .AWREADY  ( m_axi_awready  )
         , .AWQOS    ( m_axi_awqos    )
         , .AWREGION ( m_axi_awregion )
         , .WID      ( m_axi_wid      ) //[AXI_WIDTH_ID-1:0]
         , .WDATA    ( m_axi_wdata    )
         , .WSTRB    ( m_axi_wstrb    )
         , .WLAST    ( m_axi_wlast    )
         , .WVALID   ( m_axi_wvalid   )
         , .WREADY   ( m_axi_wready   )
         , .BID      ( m_axi_bid      )
         , .BRESP    ( m_axi_bresp    )
         , .BVALID   ( m_axi_bvalid   )
         , .BREADY   ( m_axi_bready   )
         , .ARID     ( m_axi_arid     ) //[AXI_WIDTH_ID-1:0]
         , .ARADDR   ( m_axi_araddr)
         , .ARLEN    ( m_axi_arlen    )
         , .ARLOCK   ( m_axi_arlock   )
         , .ARSIZE   ( m_axi_arsize   )
         , .ARBURST  ( m_axi_arburst  )
         , .ARCACHE  ( m_axi_arcache  )
         , .ARPROT   ( m_axi_arprot   )
         , .ARVALID  ( m_axi_arvalid  )
         , .ARREADY  ( m_axi_arready  )
         , .ARQOS    ( m_axi_arqos    )
         , .ARREGION ( m_axi_arregion )
         , .RID      ( m_axi_rid      ) //[AXI_WIDTH_ID-1:0]
         , .RDATA    ( m_axi_rdata    )
         , .RRESP    ( m_axi_rresp    )
         , .RLAST    ( m_axi_rlast    )
         , .RVALID   ( m_axi_rvalid   )
         , .RREADY   ( m_axi_rready   )
         , .IRQ      ( 1'b0         )
         , .FIQ      ( 1'b0         )
         , .GPOUT    ( )
         , .GPIN     ( 15'h0 )
    );
    //--------------------------------------------------------------------------
endmodule
//------------------------------------------------------------------------------
// Revision history:
//
//------------------------------------------------------------------------------
