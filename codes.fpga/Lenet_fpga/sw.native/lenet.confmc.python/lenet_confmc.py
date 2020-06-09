#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains Python version of XFFT with CON-FMC AMBA AXI BFM.
"""
__author__     = "Ando Ki"
__copyright__  = "Copyright 2020, Future Design Systems"
__credits__    = ["none", "some"]
__license__    = "FUTURE DESIGN SYSTEMS SOFTWARE END-USER LICENSE AGREEMENT FOR CON-FMC."
__version__    = "1"
__revision__   = "0"
__maintainer__ = "Ando Ki"
__email__      = "contact@future-ds.com"
__status__     = "Development"
__date__       = "2020.06.06"
__description__= "LeNet-5 with CON-FMC AMBA AXI BFM"

#-------------------------------------------------------------------------------
import sys
import cv2
import ctypes
import numpy as np
import confmc.pyconfmc as confmc
import confmc.pyconbfmaxi as axi

#-------------------------------------------------------------------------------
# constants
CONST_NUM_ROWS   = 32; # IMG_DMNIN
CONST_NUM_COLS   = 32; # IMG_DMNIN
CONST_SIZE_IMG   =(CONST_NUM_ROWS*CONST_NUM_COLS); # num of pixels
CONST_NUM_CLASSES= 10; # SFMX_SIZE

CONST_ADDR_CSR   = 0xC0000000
CONST_ADDR_IMG   = 0x00000000; # address for image data
CONST_ADDR_RESULT= (CONST_ADDR_IMG+4*CONST_SIZE_IMG); # address for result

#-------------------------------------------------------------------------------
# cast 32-bit float to unsigned int without modifying bit-pattern
def cast_float_to_uint(fvalue):
    uvalue = []
    for f in fvalue:
        uvalue.append(ctypes.cast(ctypes.pointer(ctypes.c_float(f)),
                                  ctypes.POINTER(ctypes.c_uint32)).contents.value)
    return uvalue

#-------------------------------------------------------------------------------
# cast 32-bit unsigned int to float without modifying bit-pattern
def cast_uint_to_float(uvalue):
    fvalue = []
    for u in uvalue:
        fvalue.append(ctypes.cast(ctypes.pointer(ctypes.c_uint32(u)),
                                  ctypes.POINTER(ctypes.c_float)).contents.value)
    return fvalue

#-------------------------------------------------------------------------------
def wait_for_ready(hdl):
    ap_addr = CONST_ADDR_CSR
    ap_idle = [0x0]
    while True:
        axi.BfmRead(hdl, addr=ap_addr, data=ap_idle, size=4, length=1, rigor=1)
        if ((ap_idle[0]>>2)&0x1): break; # 'ap_idle' high means the IP is waiting for start.

#-------------------------------------------------------------------------------
def go_and_wait_for_done (hdl):
    ap_addr = CONST_ADDR_CSR
    ap_data = [0x1]
    ap_done = [0x0]
    axi.BfmWrite(hdl, addr=ap_addr, data=ap_data, size=4, length=1, rigor=1)
    while True:
        axi.BfmRead(hdl, addr=ap_addr, data=ap_done, size=4, length=1, rigor=1)
        if ((ap_done[0]>>1)&0x1): break

#-------------------------------------------------------------------------------
# 1. read image file and convert to greay scale
# 2. make 32-bit float data
# 3. make sure 32x32 size
# 4. make background black if required
# 5. make normaized
# 6. make 1D array
# 7. return image data
def get_image_data(imageFile, normalize=1, revert=0, verbose=0):
    img = cv2.imread(imageFile, cv2.IMREAD_GRAYSCALE); # makes grey scale
    img = np.float32(img); # make it 32-bit float version
    if img.shape != [32, 32]:
        img = cv2.resize(img, (32, 32))
    if normalize: # normaize it to 0-1
        scale_min = -0.3635
        scale_max = 3.2558
        img = (img/255.0)*(scale_max-scale_min)+scale_min;
    if revert: img = 1-img; # revert the image, i.e., make black background
    img = img.flatten()
    if verbose:
        print(img.dtype)
        print(img.shape)
        cv2.imshow(imageFile, img)
        cv2.waitKey(0)
    return img

#-------------------------------------------------------------------------------
def lenet_test(hdl, imageFile, verbose=0):
    # 1: get grey-scale image data in 1D array
    fdata = get_image_data(imageFile, verbose=verbose)
    # 2: cast float to unsigned int (presever bit-pattern)
    udata = cast_float_to_uint(fdata)
    # 3: wait for IP ready 
    wait_for_ready(hdl)
    # 4: push image data
    axi.BfmWrite(hdl, addr=CONST_ADDR_IMG, data=udata, size=4, length=CONST_SIZE_IMG, rigor=1)
    # 5: let IP run and wait for completion
    go_and_wait_for_done(hdl)
    # 6: get results
    uresults = [0]*CONST_NUM_CLASSES
    axi.BfmRead(hdl, addr=CONST_ADDR_RESULT, data=uresults, size=4, length=CONST_NUM_CLASSES, rigor=1)
    # 7: cast unsigned int to float while keeping bit-pattern
    fresults = cast_uint_to_float(uresults)
    return fresults

#-------------------------------------------------------------------------------
def help(prog):
    print(prog+' [-c <card_id>] -i <image_file>')

#-------------------------------------------------------------------------------
def main(prog, argv):
    import getopt
    cid=0
    verbose=0
    imageFile=""
    try: opts, args = getopt.getopt(argv, "hc:i:v",['help','cid=','input=','verbose'])
    except getopt.GetoptError:
           print("conInit getopterror.")
           help(prog)
           sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
           help(prog)
           sys.exit()
        elif opt in ("-c", "--cid"):
             cid = int(arg)
        elif opt in ("-i", "--input"):
             imageFile = str(arg)
        elif opt in ("-v", "--verbose"):
             verbose = 1
        else:
             print("unknown options: "+str(opt))
             sys.exit(1)
    if not imageFile:
       help(prog)
       sys.exit(1)

    hdl=confmc.conInit()
    if not hdl:
       print("conInit returns error; check CID.")
       help(prog)
       sys.exit(1)
    cid=confmc.conGetCid(hdl)
    if cid<0:
       print("CON-FMC: CID"+str(cid)+" not found.")
       sys.exit(1)

    if verbose: print("CON-FMC: CID"+str(cid)+" found.")

    results = lenet_test(hdl, imageFile, verbose)
    maxVAL = 0.0
    maxID = 0;
    for i in range(len(results)):
        if (maxVAL<results[i]) : maxVAL = results[i]; maxID = i;
    for i in range(len(results)): print("[%d] = %f %s" %(i, results[i], ((i==maxID) and '*' or '')))

    confmc.conRelease(hdl)

if __name__ == '__main__':
   main(sys.argv[0],sys.argv[1:])

#===============================================================================
# Revision history:
#
# 2020.06.06: Started by Ando Ki (adki@future-ds.com)
#             - Not finished nor complete yet
#===============================================================================
