set part [lindex $argv 0]
set xdc [lindex $argv 1]
set verilog [lindex $argv 2]

create_project -force -name top -part $part
set_msg_config -id {Common 17-55} -new_severity {Warning}

read_verilog $verilog
read_xdc ../$xdc

synth_design -directive default -top top -part $part
opt_design -directive default
place_design -directive default
phys_opt_design -directive default
route_design -directive default
write_checkpoint -force top_f2b_route.dcp

set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property IS_ENABLED 0 [get_drc_checks {LUTLP-1}]

write_bitstream -force top_f2b.bit

write_cfgmem -force -format bin -interface spix4 -size 16 -loadbit "up 0x0 top.bit" -file top.bin
