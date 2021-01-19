# Copyright (C) 2017-2020  The Project X-Ray Authors
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC
create_project -force -name $env(PROJECT_NAME) -part $env(PART)

read_edif ../$env(PROJECT_NAME).edif

link_design -part $env(PART)
source ../build/nexys_video/gateware/nexys_video.xdc

set_property SEVERITY {Warning} [get_drc_checks UCIO-1]
set_property SEVERITY {Warning} [get_drc_checks NSTD-1]
set_property SEVERITY {Warning} [get_drc_checks REQP-1936]

place_design
route_design

write_checkpoint -force ../$env(PROJECT_NAME).dcp

write_bitstream -force ../$env(PROJECT_NAME).bit
