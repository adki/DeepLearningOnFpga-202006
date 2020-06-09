#ifndef TRX_AXI_API_H
#define TRX_AXI_API_H
//------------------------------------------------------------------------------
// Copyright (c) 2018-2019 Future Design Systems
//
// http://www.future-ds.com
//------------------------------------------------------------------------------
// trx_axi_api.h
//------------------------------------------------------------------------------
// VERSION = 2019.04.15.
//------------------------------------------------------------------------------
// Note that "data" carries justified data.
#include "conapi.h"

#if defined(_MSC_VER)
   #define CONFMC_BFM_API
#else
#if (defined(_WIN32)||defined(_WIN64))
   #ifdef BUILDING_DLL
      #define CONFMC_BFM_API __declspec(dllexport)
   #else
      #ifdef BUILDING_STATIC
         #define CONFMC_BFM_API
      #else
         #define CONFMC_BFM_API __declspec(dllimport)
      #endif
   #endif
#else
   #define CONFMC_BFM_API
#endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

CONFMC_BFM_API int BfmWrite( con_Handle_t handle
                           , unsigned int  addr
                           , unsigned int *data
                           , unsigned int  size
                           , unsigned int  length);
CONFMC_BFM_API int BfmRead ( con_Handle_t handle
                           , unsigned int  addr
                           , unsigned int *data
                           , unsigned int  size
                           , unsigned int  length);
CONFMC_BFM_API int BfmWriteFix( con_Handle_t handle
                              , unsigned int  addr
                              , unsigned int *data
                              , unsigned int  size
                              , unsigned int  length);
CONFMC_BFM_API int BfmReadFix ( con_Handle_t handle
                              , unsigned int  addr
                              , unsigned int *data
                              , unsigned int  size
                              , unsigned int  length);
CONFMC_BFM_API int BfmGpout( con_Handle_t handle
                           , unsigned int Value );
CONFMC_BFM_API int BfmGpin ( con_Handle_t handle
                           , unsigned int *pValue );
CONFMC_BFM_API int BfmSetAmbaAxi4( con_Handle_t handle );
#ifdef __cplusplus
}
#endif
//------------------------------------------------------------------------------
// Revision History
//
// 2019.04.15: BfmWrite()/BfmRead()/BfmWriteFix()/BfmReadFix() returns non-Void
// 2019.02.07: Each API has new argument, con_Handle_t handle
// 2018.06.12: BfmWriteFix/BfmReadFix added
// 2018.05.01: Start by Ando Ki (adki@future-ds.com)
//------------------------------------------------------------------------------
#endif
