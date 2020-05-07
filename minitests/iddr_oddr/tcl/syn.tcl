create_project -force -name $::env(PROJECT_NAME) -part $::env(XRAY_PART)

read_verilog ../$::env(PROJECT_NAME).v

synth_design -top top
write_edif -force ../$::env(PROJECT_NAME).edif
