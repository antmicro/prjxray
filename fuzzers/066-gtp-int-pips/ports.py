#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2020  The Project X-Ray Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC

ports = {
    "GTPE2_CHANNEL": [
        ("CFGRESET", 1),
        ("CLKRSVD0", 1),
        ("CLKRSVD1", 1),
        ("DMONFIFORESET", 1),
        ("DMONITORCLK", 1),
        ("DRPCLK", 1),
        ("DRPEN", 1),
        ("DRPWE", 1),
        ("EYESCANMODE", 1),
        ("EYESCANRESET", 1),
        ("EYESCANTRIGGER", 1),
        ("GTRESETSEL", 1),
        ("GTRXRESET", 1),
        ("GTTXRESET", 1),
        ("PMARSVDIN0", 1),
        ("PMARSVDIN1", 1),
        ("PMARSVDIN2", 1),
        ("PMARSVDIN3", 1),
        ("PMARSVDIN4", 1),
        ("RESETOVRD", 1),
        ("RX8B10BEN", 1),
        ("RXBUFRESET", 1),
        ("RXCDRFREQRESET", 1),
        ("RXCDRHOLD", 1),
        ("RXCDROVRDEN", 1),
        ("RXCDRRESET", 1),
        ("RXCDRRESETRSV", 1),
        ("RXCHBONDEN", 1),
        ("RXCHBONDMASTER", 1),
        ("RXCHBONDSLAVE", 1),
        ("RXCOMMADETEN", 1),
        ("RXDDIEN", 1),
        ("RXDFEXYDEN", 1),
        ("RXDLYBYPASS", 1),
        ("RXDLYEN", 1),
        ("RXDLYOVRDEN", 1),
        ("RXDLYSRESET", 1),
        ("RXGEARBOXSLIP", 1),
        ("RXLPMHFHOLD", 1),
        ("RXLPMHFOVRDEN", 1),
        ("RXLPMLFHOLD", 1),
        ("RXLPMLFOVRDEN", 1),
        ("RXLPMOSINTNTRLEN", 1),
        ("RXLPMRESET", 1),
        ("RXMCOMMAALIGNEN", 1),
        ("RXOOBRESET", 1),
        ("RXOSCALRESET", 1),
        ("RXOSHOLD", 1),
        ("RXOSINTEN", 1),
        ("RXOSINTHOLD", 1),
        ("RXOSINTNTRLEN", 1),
        ("RXOSINTOVRDEN", 1),
        ("RXOSINTPD", 1),
        ("RXOSINTSTROBE", 1),
        ("RXOSINTTESTOVRDEN", 1),
        ("RXOSOVRDEN", 1),
        ("RXPCOMMAALIGNEN", 1),
        ("RXPCSRESET", 1),
        ("RXPHALIGN", 1),
        ("RXPHALIGNEN", 1),
        ("RXPHDLYPD", 1),
        ("RXPHDLYRESET", 1),
        ("RXPHOVRDEN", 1),
        ("RXPMARESET", 1),
        ("RXPOLARITY", 1),
        ("RXPRBSCNTRESET", 1),
        ("RXRATEMODE", 1),
        ("RXSLIDE", 1),
        ("RXSYNCALLIN", 1),
        ("RXSYNCIN", 1),
        ("RXSYNCMODE", 1),
        ("RXUSERRDY", 1),
        ("RXUSRCLK2", 1),
        ("RXUSRCLK", 1),
        ("SETERRSTATUS", 1),
        ("SIGVALIDCLK", 1),
        ("TX8B10BEN", 1),
        ("TXCOMINIT", 1),
        ("TXCOMSAS", 1),
        ("TXCOMWAKE", 1),
        ("TXDEEMPH", 1),
        ("TXDETECTRX", 1),
        ("TXDIFFPD", 1),
        ("TXDLYBYPASS", 1),
        ("TXDLYEN", 1),
        ("TXDLYHOLD", 1),
        ("TXDLYOVRDEN", 1),
        ("TXDLYSRESET", 1),
        ("TXDLYUPDOWN", 1),
        ("TXELECIDLE", 1),
        ("TXINHIBIT", 1),
        ("TXPCSRESET", 1),
        ("TXPDELECIDLEMODE", 1),
        ("TXPHALIGN", 1),
        ("TXPHALIGNEN", 1),
        ("TXPHDLYPD", 1),
        ("TXPHDLYRESET", 1),
        ("TXPHDLYTSTCLK", 1),
        ("TXPHINIT", 1),
        ("TXPHOVRDEN", 1),
        ("TXPIPPMEN", 1),
        ("TXPIPPMOVRDEN", 1),
        ("TXPIPPMPD", 1),
        ("TXPIPPMSEL", 1),
        ("TXPISOPD", 1),
        ("TXPMARESET", 1),
        ("TXPOLARITY", 1),
        ("TXPOSTCURSORINV", 1),
        ("TXPRBSFORCEERR", 1),
        ("TXPRECURSORINV", 1),
        ("TXRATEMODE", 1),
        ("TXSTARTSEQ", 1),
        ("TXSWING", 1),
        ("TXSYNCALLIN", 1),
        ("TXSYNCIN", 1),
        ("TXSYNCMODE", 1),
        ("TXUSERRDY", 1),
        ("TXUSRCLK2", 1),
        ("TXUSRCLK", 1),
        ("RXADAPTSELTEST", 14),
        ("DRPDI", 16),
        ("GTRSVD", 16),
        ("PCSRSVDIN", 16),
        ("TSTIN", 20),
        ("RXELECIDLEMODE", 2),
        ("RXPD", 2),
        ("RXSYSCLKSEL", 2),
        ("TXPD", 2),
        ("TXSYSCLKSEL", 2),
        ("LOOPBACK", 3),
        ("RXCHBONDLEVEL", 3),
        ("RXOUTCLKSEL", 3),
        ("RXPRBSSEL", 3),
        ("RXRATE", 3),
        ("TXBUFDIFFCTRL", 3),
        ("TXHEADER", 3),
        ("TXMARGIN", 3),
        ("TXOUTCLKSEL", 3),
        ("TXPRBSSEL", 3),
        ("TXRATE", 3),
        ("TXDATA", 32),
        ("RXCHBONDI", 4),
        ("RXOSINTCFG", 4),
        ("RXOSINTID0", 4),
        ("TX8B10BBYPASS", 4),
        ("TXCHARDISPMODE", 4),
        ("TXCHARDISPVAL", 4),
        ("TXCHARISK", 4),
        ("TXDIFFCTRL", 4),
        ("TXPIPPMSTEPSIZE", 5),
        ("TXPOSTCURSOR", 5),
        ("TXPRECURSOR", 5),
        ("TXMAINCURSOR", 7),
        ("TXSEQUENCE", 7),
        ("DRPADDR", 9),
    ],
    "GTPE2_COMMON": [
        ("BGBYPASSB", 1),
        ("BGMONITORENB", 1),
        ("BGPDB", 1),
        ("BGRCALOVRDENB", 1),
        ("DRPCLK", 1),
        ("DRPEN", 1),
        ("DRPWE", 1),
        ("PLL0LOCKDETCLK", 1),
        ("PLL0LOCKEN", 1),
        ("PLL0PD", 1),
        ("PLL0RESET", 1),
        ("PLL1LOCKDETCLK", 1),
        ("PLL1LOCKEN", 1),
        ("PLL1PD", 1),
        ("PLL1RESET", 1),
        ("RCALENB", 1),
        ("DRPDI", 16),
        ("PLLRSVD1", 16),
        ("PLL0REFCLKSEL", 3),
        ("PLL1REFCLKSEL", 3),
        ("BGRCALOVRD", 5),
        ("PLLRSVD2", 5),
        ("DRPADDR", 8),
        ("PMARSVD", 8),
    ],
}
