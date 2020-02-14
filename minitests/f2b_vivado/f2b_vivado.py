#!/usr/bin/env python3

import argparse
import subprocess

def main():

    parser = argparse.ArgumentParser(
            description='Runs an implemented design through fasm2bels and uses Vivado on the generated verilog'
            )

    parser.add_argument('--pcf', required=True, help="PCF file of the target device.")
    parser.add_argument('--xdc', required=True, help="XDC file constraining the design.")

    parser.add_argument('--sources_dir', help="Verilog design file to build")
    parser.add_argument('--top_verilog', help="Verilog design file to build")
    parser.add_argument('--fasm', help="FASM file of the implemented design.")
    parser.add_argument('--eblif', help="eblif file of the synthesized design.")

    args = parser.parse_args()

    fasm = args.fasm
    eblif = args.eblif
    sources_dir = args.sources_dir
    top_verilog = "{}/{}".format(sources_dir, args.top_verilog)

    pcf = args.pcf
    xdc = args.xdc

    if sources_dir is None or top_verilog is None:
        assert fasm and eblif, "Intermediate files necessary (FASM, bitstream and eblif)!"
    else:
        subprocess.check_call("./run_yosys_vivado.sh {} {} {}".format(xdc, top_verilog, sources_dir), shell=True)
        fasm = "build/top.fasm"
        eblif = "build/top.eblif"


    subprocess.check_call("./run_fasm2bels.sh {} {} {}".format(fasm, pcf, eblif), shell=True)
    subprocess.check_call("./run_vivado.sh {}".format(xdc), shell=True)




if __name__ == "__main__":
    main()
