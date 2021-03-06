# Copyright (C) 2017-2020  The Project X-Ray Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC
export XRAY_DATABASE="zynq7"
export XRAY_PART="xc7z020clg484-1"
export XRAY_ROI_FRAMES="0x00000000:0xffffffff"

# All CLB's in part, all BRAM's in part, all DSP's in part.
export XRAY_ROI_TILEGRID="SLICE_X0Y0:SLICE_X113Y149 RAMB18_X0Y0:RAMB18_X5Y59 RAMB36_X0Y0:RAMB36_X5Y29 DSP48_X0Y0:DSP48_X4Y59"

export XRAY_EXCLUDE_ROI_TILEGRID=""

export XRAY_IOI3_TILES="RIOI3_X73Y9 LIOI3_X0Y9"
export XRAY_PS7_INT="INT_L_X18Y100"

# These settings must remain in sync
export XRAY_ROI="SLICE_X0Y0:SLICE_X49Y49 RAMB18_X0Y0:RAMB18_X2Y19 RAMB36_X0Y0:RAMB36_X2Y9 IOB_X0Y0:IOB_X0Y49 DSP48_X0Y0:DSP48_X2Y19"

# Most of CMT X0Y2.
export XRAY_ROI_GRID_X1="0"
export XRAY_ROI_GRID_X2="86"
# Include VBRK / VTERM
export XRAY_ROI_GRID_Y1="105"
export XRAY_ROI_GRID_Y2="155"

source $(dirname ${BASH_SOURCE[0]})/../utils/environment.sh

eval $(python3 ${XRAY_UTILS_DIR}/create_environment.py)
