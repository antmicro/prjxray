#!/bin/bash

BUILD_DIR=build

export PYTHONPATH=${ARCH_DEFS_DIRECTORY}/third_party/prjxray:${ARCH_DEFS_DIRECTORY}/third_party/prjxray/third_party/fasm:${ARCH_DEFS_DIRECTORY}/xc7:${ARCH_DEFS_DIRECTORY}/utils
PYTHON=${ARCH_DEFS_DIRECTORY}/build/env/conda/bin/python3

${PYTHON} -mfasm2bels \
    --db_root ${ARCH_DEFS_DIRECTORY}/third_party/prjxray-db/artix7 \
    --bitread ${ARCH_DEFS_DIRECTORY}/build/third_party/prjxray/tools/bitread \
    --fasm_file ${1} \
    --iostandard LVCMOS33 \
    --drive 12 \
    --pcf ${2} \
    --eblif ${3} \
    --part ${XRAY_PART} \
    --connection_database ${ARCH_DEFS_DIRECTORY}/build/xc7/archs/artix7/devices/xc7a50t-virt/channels.db \
    build/top_bit.v \
    build/top_bit.v.tcl
