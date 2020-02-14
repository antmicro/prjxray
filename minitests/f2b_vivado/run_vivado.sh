#!/bin/bash

XDC=${1}

sed -i 's/.*(\*.*\*)//g' build/top_bit.v

python3 replace_bufhce.py --in_file build/top_bit.v

cd build


${XRAY_VIVADO} -mode batch -source ../top_vivado.tcl -tclargs ${XRAY_PART} ${XDC} top_bit.v
${XRAY_BIT2FASM} --part ${XRAY_PART} top_f2b.bit > top_f2b.fasm
cd ..
