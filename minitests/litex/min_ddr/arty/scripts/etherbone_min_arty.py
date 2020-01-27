#!/usr/bin/env python3

# This file is Copyright (c) 2015-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# License: BSD

import argparse

from migen import *

from litex.boards.platforms import arty
from litex.build.xilinx.vivado import vivado_build_args, vivado_build_argdict

from litex.soc.cores.clock import *
from litex.soc.integration.soc_sdram import *
from litex.soc.integration.builder import *

from litedram.modules import MT41K128M16
from litedram.phy import s7ddrphy
from litex.soc.cores.uart import UARTWishboneBridge

# CRG ----------------------------------------------------------------------------------------------


class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_sys4x = ClockDomain(reset_less=True)
        self.clock_domains.cd_sys4x_dqs = ClockDomain(reset_less=True)
        self.clock_domains.cd_clk200 = ClockDomain()
        self.clock_domains.cd_eth = ClockDomain()

        # # #
        pll_clkin = Signal()
        self.specials += Instance(
            "BUFG", i_I=platform.request("clk100"), o_O=pll_clkin)
        self.submodules.pll = pll = S7PLL(speedgrade=-1)
        self.comb += pll.reset.eq(~platform.request("cpu_reset"))
        pll.register_clkin(pll_clkin, 100e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)
        pll.create_clkout(self.cd_sys4x, 4 * sys_clk_freq)
        pll.create_clkout(self.cd_sys4x_dqs, 4 * sys_clk_freq, phase=90)
        pll.create_clkout(self.cd_clk200, 200e6)
        self.submodules.idelayctrl = S7IDELAYCTRL(self.cd_clk200)


# BaseSoC ------------------------------------------------------------------------------------------


class EtherboneMinSoC(SoCSDRAM):
    def __init__(
            self, sys_clk_freq=int(100e6), integrated_rom_size=0x8000,
            **kwargs):
        platform = arty.Platform()

        # SoCSDRAM ---------------------------------------------------------------------------------
        SoCSDRAM.__init__(
            self,
            platform,
            with_uart = False,
            clk_freq=sys_clk_freq,
            cpu_type=None,
            **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)
        # UART Bridge
        self.submodules.bridge = UARTWishboneBridge(platform.request("serial", 0), sys_clk_freq, baudrate=115200)
        self.add_wb_master(self.bridge.wishbone)

        # DDR3 SDRAM -------------------------------------------------------------------------------
        self.submodules.ddrphy = s7ddrphy.A7DDRPHY(
            platform.request("ddram"),
            memtype="DDR3",
            nphases=4,
            sys_clk_freq=sys_clk_freq)
        self.add_csr("ddrphy", 5)
        sdram_module = MT41K128M16(sys_clk_freq, "1:4")
        self.register_sdram(
            self.ddrphy,
            geom_settings=sdram_module.geom_settings,
            timing_settings=sdram_module.timing_settings)


# Build --------------------------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on Arty")
    builder_args(parser)
    soc_sdram_args(parser)
    vivado_build_args(parser)
    args = parser.parse_args()

    cls = EtherboneMinSoC
    soc = cls(**soc_sdram_argdict(args))
    builder = Builder(soc, **builder_argdict(args))
    builder.build(**vivado_build_argdict(args))


if __name__ == "__main__":
    main()
