`include "../src/data_generator.v"
`include "../src/iddr_wrapper.v"
`include "../src/oddr_wrapper.v"
`include "../src/ioddr_tester.v"

`default_nettype none
`timescale 1ns / 1ps

// ============================================================================

module tb;

// ============================================================================

reg CLK;
initial CLK <= 1'b0;
always #0.5 CLK <= !CLK;

reg [3:0] rst_sr;
initial rst_sr <= 4'hF;
always @(posedge CLK) rst_sr <= rst_sr >> 1;
wire RST;
assign RST = rst_sr[0];

// ============================================================================

initial begin
    $dumpfile("tb.vcd");
    $dumpvars;
end

integer cycle_cnt;
initial cycle_cnt <= 0;

always @(posedge CLK)
    if (!RST) cycle_cnt <= cycle_cnt + 1;

always @(posedge CLK)
    if (!RST && cycle_cnt >= 10000)
        $finish;

// ============================================================================

wire x;

ioddr_tester #(.DDR_CLK_EDGE("OPPOSITE_EDGE")) dut (
    .CLK    (CLK),
    .ERR    (),
    .Q      (x),
    .D      (x)
);

endmodule


