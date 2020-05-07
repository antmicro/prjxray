create_project -force -name sim -part $::env(XRAY_PART)

read_verilog ../sim/tb.v

set_property top tb [get_filesets sim_1]

synth_design -top tb -verbose

set_property xsim.simulate.log_all_signals true [get_filesets sim_1]
set_property xsim.simulate.runtime 0 [get_filesets sim_1]

launch_simulation -verbose
restart

run -all
