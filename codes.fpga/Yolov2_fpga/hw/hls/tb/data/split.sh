#!/bin/sh
split --bytes=20M weightsv2_comb.bin weightsv2_comb.bin.pices
split --bytes=20M weightsv2_comb_reorg_ap16.bin weightsv2_comb_reorg_ap16.bin.pices
split --bytes=20M weightsv2_comb_reorg.bin weightsv2_comb_reorg.bin.pices
