#!/bin/bash

YOSYS=${XRAY_DIR}/third_party/yosys/yosys

XDC=${1}
TOP_VERILOG=${2}
SOURCES_DIR=${3}

BUILD_DIR=`pwd`/build

MEM_INIT_FILES=$(find "${SOURCES_DIR}" -name *.init)

for FILE in ${MEM_INIT_FILES}
do
    ln -s $FILE
done

export BUILD_DIR=${BUILD_DIR}
export VERILOG_FILE=${TOP_VERILOG}

${YOSYS} -p "tcl synth.tcl" -l yosys.log

source /opt/Xilinx/Vivado/2017.2/settings64.sh

cd build
vivado -mode batch -source ../top_yosys.tcl -nojournal -tclargs ${XRAY_PART} ${XDC} top.edif
cd ..

