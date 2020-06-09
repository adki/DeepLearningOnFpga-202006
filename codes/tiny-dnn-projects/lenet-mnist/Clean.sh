#!/bin/sh

if [ -f train.o           ]; then \rm -f train.o          ; fi
if [ -f test.o            ]; then \rm -f test.o           ; fi
if [ -f compile.log.train ]; then \rm -f compile.log.train; fi
if [ -f compile.log.test  ]; then \rm -f compile.log.test ; fi
if [ -f train             ]; then \rm -f train            ; fi
if [ -f "test"            ]; then \rm -f test             ; fi
if [ -f LeNet-mdoel       ]; then \rm -f LeNet-mdoel      ; fi
if [ -f LeNet-mdoel-json  ]; then \rm -f LeNet-mdoel-json ; fi
