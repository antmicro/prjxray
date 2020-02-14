set part [lindex $argv 0]
set xdc [lindex $argv 1]
set edif [lindex $argv 2]

create_project -force -name top -part $part
set_msg_config -id {Common 17-55} -new_severity {Warning}

read_edif $edif
link_design -top top -part $part
read_xdc ../$xdc

opt_design -directive default
place_design -directive default
phys_opt_design -directive default
route_design -directive default
write_checkpoint -force top_route.dcp

set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property IS_ENABLED 0 [get_drc_checks {LUTLP-1}]

write_bitstream -force top.bit

write_cfgmem -force -format bin -interface spix4 -size 16 -loadbit "up 0x0 top.bit" -file top.bin
