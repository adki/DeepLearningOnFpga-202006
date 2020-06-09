#!/bin/csh -f

if ( -e train.o           ) \rm -f train.o          
if ( -e test.o            ) \rm -f test.o           
if ( -e compile.log.train ) \rm -f compile.log.train
if ( -e compile.log.test  ) \rm -f compile.log.test 
if ( -e train             ) \rm -f train            
if ( -e test              ) \rm -f test             
if ( -e LeNet-model       ) \rm -f LeNet-model      
if ( -e LeNet-model-json  ) \rm -f LeNet-model-json
