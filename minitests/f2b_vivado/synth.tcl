yosys -import

read_verilog $::env(VERILOG_FILE)
synth_xilinx -edif $::env(BUILD_DIR)/top.edif
write_blif $::env(BUILD_DIR)/top.eblif
