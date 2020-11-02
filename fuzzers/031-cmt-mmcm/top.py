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
import os
import random
random.seed(int(os.getenv("SEED"), 16))
from prjxray import util
from prjxray import verilog
from prjxray.db import Database
import json


def gen_sites():
    db = Database(util.get_db_root(), util.get_part())
    grid = db.grid()
    for tile_name in sorted(grid.tiles()):
        loc = grid.loc_of_tilename(tile_name)
        gridinfo = grid.gridinfo_at_loc(loc)

        tile_type = tile_name.rsplit("_", 1)[0]

        for site_name, site_type in gridinfo.sites.items():
            if site_type in ['MMCME2_ADV']:
                yield tile_name, tile_type, site_name


def main():
    sites = sorted(list(gen_sites()))
    max_sites = len(sites)

    f = open('params.jl', 'w')
    f.write('module,loc,params\n')

    routes_file = open('routes.txt', 'w')

    def gen_true_false(p):
        if random.random() <= p:
            return verilog.quote("TRUE")
        else:
            return verilog.quote("FALSE")

    print(
        """
module top(
    input [{N}:0] clkin1,
    input [{N}:0] clkin2,
    input [{N}:0] clkfb,
    input [{N}:0] dclk
);

    (* KEEP, DONT_TOUCH *)
    LUT1 dummy();
""".format(N=max_sites - 1))

    for i, (
            tile_name,
            tile_type,
            site,
    ) in enumerate(sorted(gen_sites())):
        params = {
            "site":
            site,
            'active':
            random.random() > .2,
            "clkin1_conn":
            random.choice(
                ("clkfbout_mult_BUFG_" + site, "clkin1[{}]".format(i), "")),
            "clkin2_conn":
            random.choice(
                ("clkfbout_mult_BUFG_" + site, "clkin2[{}]".format(i), "")),
            "dclk_conn":
            random.choice((
                "0",
                "dclk[{}]".format(i),
            )),
            "dwe_conn":
            random.choice((
                "",
                "1",
                "0",
                "dwe_" + site,
                "den_" + site,
            )),
            "den_conn":
            random.choice((
                "",
                "1",
                "0",
                "den_" + site,
            )),
            "daddr4_conn":
            random.choice((
                "0",
                "dwe_" + site,
            )),
            "IS_RST_INVERTED":
            random.randint(0, 1),
            "IS_PWRDWN_INVERTED":
            random.randint(0, 1),
            "IS_CLKINSEL_INVERTED":
            random.randint(0, 1),
            "CLKFBOUT_MULT_F":
            random.randint(2, 4),
            "CLKOUT0_DIVIDE_F":
            random.randint(1, 128),
            "CLKOUT1_DIVIDE":
            random.randint(1, 128),
            "CLKOUT2_DIVIDE":
            random.randint(1, 128),
            "CLKOUT3_DIVIDE":
            random.randint(1, 128),
            "CLKOUT4_DIVIDE":
            random.randint(1, 128),
            "CLKOUT5_DIVIDE":
            random.randint(1, 128),
            "CLKOUT6_DIVIDE":
            random.randint(1, 128),
            "DIVCLK_DIVIDE":
            random.randint(1, 5),
            "CLKOUT0_DUTY_CYCLE":
            "0.500",
            "STARTUP_WAIT":
            verilog.quote('TRUE' if random.randint(0, 1) else 'FALSE'),
            "COMPENSATION":
            verilog.quote(
                random.choice((
                    'ZHOLD',
                    'BUF_IN',
                    'EXTERNAL',
                    'INTERNAL',
                ))),
            "BANDWIDTH":
            verilog.quote(random.choice((
                'OPTIMIZED',
                'HIGH',
                'LOW',
            ))),
            "CLKFBOUT_USE_FINE_PS":
            gen_true_false(0.50),
            "CLKOUT0_USE_FINE_PS":
            gen_true_false(0.50),
            "CLKOUT1_USE_FINE_PS":
            gen_true_false(0.50),
            "CLKOUT2_USE_FINE_PS":
            gen_true_false(0.50),
            "CLKOUT3_USE_FINE_PS":
            gen_true_false(0.50),
            "CLKOUT4_USE_FINE_PS":
            gen_true_false(0.50),
            "CLKOUT5_USE_FINE_PS":
            gen_true_false(0.50),
            "CLKOUT6_USE_FINE_PS":
            gen_true_false(0.50),
            "SS_EN":
            gen_true_false(0.15),
            "SS_MODE":
            verilog.quote(random.choice([
                "DOWN_LOW",
                "DOWN_HIGH",
                "CENTER_LOW",
                "CENTER_HIGH"
            ])),
            "SS_MOD_PERIOD":
            random.randint(4000, 40000),
            "CLKOUT4_CASCADE": # FIXME: Sometime makes Vivado segfault
            verilog.quote("FALSE"), #gen_true_false(0.15),
        }

        # SS_EN requires BANDWIDTH to be LOW
        if verilog.unquote(params["SS_EN"]) == "TRUE":
            params["BANDWIDTH"] = verilog.quote("LOW")

        if verilog.unquote(params['COMPENSATION']) == 'ZHOLD':
            params['clkfbin_conn'] = random.choice(
                (
                    "",
                    "clkfbout_mult_BUFG_" + site,
                ))
        elif verilog.unquote(params['COMPENSATION']) == 'INTERNAL':
            params['clkfbin_conn'] = random.choice(
                (
                    "",
                    "clkfbout_mult_" + site,
                ))
        else:
            params['clkfbin_conn'] = random.choice(
                ("", "clkfb[{}]".format(i), "clkfbout_mult_BUFG_" + site))

        params['clkin1_route'] = random.choice(
            (
                "{}_CLKIN1",
                "{}_FREQ_BB0",
                "{}_FREQ_BB1",
                "{}_FREQ_BB2",
                "{}_FREQ_BB3",
                "{}_MMCME2_CLK_IN1_INT",
            )).format(tile_type)

        params['clkin2_route'] = random.choice(
            (
                "{}_CLKIN2",
                "{}_FREQ_BB0",
                "{}_FREQ_BB1",
                "{}_FREQ_BB2",
                "{}_FREQ_BB3",
                "{}_MMCME2_CLK_IN2_INT",
            )).format(tile_type)

        params['clkfbin_route'] = random.choice(
            (
                "{}_CLKFBOUT2IN",
                "{}_UPPER_T_FREQ_BB0",
                "{}_UPPER_T_FREQ_BB1",
                "{}_UPPER_T_FREQ_BB2",
                "{}_UPPER_T_FREQ_BB3",
                "{}_UPPER_T_MMCME2_CLK_FB_INT",
            )).format(tile_type.replace("_UPPER_T", ""))

        f.write('%s\n' % (json.dumps(params)))

        def make_ibuf_net(net):
            p = net.find('[')
            return net[:p] + '_IBUF' + net[p:]

        if params['clkin1_conn'] != "":
            net = make_ibuf_net(params['clkin1_conn'])
            wire = '{}/{}'.format(tile_name, params['clkin1_route'])
            routes_file.write('{} {}\n'.format(net, wire))

        if params['clkin2_conn'] != "":
            net = make_ibuf_net(params['clkin2_conn'])
            wire = '{}/{}'.format(tile_name, params['clkin2_route'])
            routes_file.write('{} {}\n'.format(net, wire))

        if params['clkfbin_conn'] != "" and\
           params['clkfbin_conn'] != ("clkfbout_mult_BUFG_" + site):
            net = params['clkfbin_conn']
            if "[" in net and "]" in net:
                net = make_ibuf_net(net)
            wire = '{}/{}'.format(tile_name, params['clkfbin_route'])
            routes_file.write('{} {}\n'.format(net, wire))

        if not params['active']:
            continue

        print(
            """

    wire den_{site};
    wire dwe_{site};

    wire psclk_{site};
    wire psen_{site};
    wire psincdec_{site};

    (* KEEP, DONT_TOUCH *)
    LUT1 den_lut_{site} (
        .O(den_{site})
    );

    (* KEEP, DONT_TOUCH *)
    LUT1 dwe_lut_{site} (
        .O(dwe_{site})
    );

    (* KEEP, DONT_TOUCH *)
    LUT1 psclk_lut_{site} (
        .O(psckl_{site})
    );

    (* KEEP, DONT_TOUCH *)
    LUT1 psen_lut_{site} (
        .O(psen_{site})
    );

    (* KEEP, DONT_TOUCH *)
    LUT1 psincdec_lut_{site} (
        .O(psincdec_{site})
    );

    wire clkfbout_mult_{site};
    wire clkfbout_mult_BUFG_{site};
    wire clkout0_{site};
    wire clkout1_{site};
    wire clkout2_{site};
    wire clkout3_{site};
    wire clkout4_{site};
    wire clkout5_{site};
    wire clkout6_{site};
    (* KEEP, DONT_TOUCH, LOC = "{site}" *)
    MMCME2_ADV #(
            .IS_RST_INVERTED({IS_RST_INVERTED}),
            .IS_PWRDWN_INVERTED({IS_PWRDWN_INVERTED}),
            .IS_CLKINSEL_INVERTED({IS_CLKINSEL_INVERTED}),
            .CLKOUT0_DIVIDE_F({CLKOUT0_DIVIDE_F}),
            .CLKOUT1_DIVIDE({CLKOUT1_DIVIDE}),
            .CLKOUT2_DIVIDE({CLKOUT2_DIVIDE}),
            .CLKOUT3_DIVIDE({CLKOUT3_DIVIDE}),
            .CLKOUT4_DIVIDE({CLKOUT4_DIVIDE}),
            .CLKOUT5_DIVIDE({CLKOUT5_DIVIDE}),
            .CLKOUT6_DIVIDE({CLKOUT6_DIVIDE}),
            .CLKFBOUT_MULT_F({CLKFBOUT_MULT_F}),
            .DIVCLK_DIVIDE({DIVCLK_DIVIDE}),
            .STARTUP_WAIT({STARTUP_WAIT}),
            .CLKOUT0_DUTY_CYCLE({CLKOUT0_DUTY_CYCLE}),
            .COMPENSATION({COMPENSATION}),
            .BANDWIDTH({BANDWIDTH}),
            .CLKFBOUT_USE_FINE_PS({CLKFBOUT_USE_FINE_PS}),
            .CLKOUT0_USE_FINE_PS({CLKOUT0_USE_FINE_PS}),
            .CLKOUT1_USE_FINE_PS({CLKOUT1_USE_FINE_PS}),
            .CLKOUT2_USE_FINE_PS({CLKOUT2_USE_FINE_PS}),
            .CLKOUT3_USE_FINE_PS({CLKOUT3_USE_FINE_PS}),
            .CLKOUT4_USE_FINE_PS({CLKOUT4_USE_FINE_PS}),
            .CLKOUT5_USE_FINE_PS({CLKOUT5_USE_FINE_PS}),
            .CLKOUT6_USE_FINE_PS({CLKOUT6_USE_FINE_PS}),
            .CLKOUT4_CASCADE({CLKOUT4_CASCADE}),
            .SS_EN({SS_EN}),
            .SS_MODE({SS_MODE}),
            .SS_MOD_PERIOD({SS_MOD_PERIOD}),
            .CLKIN1_PERIOD(10.0),
            .CLKIN2_PERIOD(10.0)
    ) mmcm_{site} (
            .CLKFBOUT(clkfbout_mult_{site}),
            .CLKOUT0(clkout0_{site}),
            .CLKOUT1(clkout1_{site}),
            .CLKOUT2(clkout2_{site}),
            .CLKOUT3(clkout3_{site}),
            .CLKOUT4(clkout4_{site}),
            .CLKOUT5(clkout5_{site}),
            .CLKOUT6(clkout6_{site}),
            .PSCLK(psclk_{site}),
            .PSEN(psen_{site}),
            .PSINCDEC(psincdec_{site}),
            .DRDY(),
            .LOCKED(),
            .DO(),
            .CLKFBIN({clkfbin_conn}),
            .CLKIN1({clkin1_conn}),
            .CLKIN2({clkin2_conn}),
            .CLKINSEL(),
            .DCLK({dclk_conn}),
            .DEN({den_conn}),
            .DWE({dwe_conn}),
            .PWRDWN(),
            .RST(),
            .DI(),
            .DADDR({{7{{ {daddr4_conn} }} }}));

    (* KEEP, DONT_TOUCH *)
    BUFG bufg_{site} (
        .I(clkfbout_mult_{site}),
        .O(clkfbout_mult_BUFG_{site})
    );

    (* KEEP, DONT_TOUCH *)
    FDRE reg_clkfbout_mult_{site} (
        .C(clkfbout_mult_{site})
    );
            """.format(**params))

        disabled_clkout = random.randint(0, 7)
        for clk in range(0, 7):
            if clk == disabled_clkout:
                continue

            print(
                """
            (* KEEP, DONT_TOUCH *)
            FDRE reg_clkout{clk}_{site} (
                .C(clkout{clk}_{site})
            );
            """.format(clk=clk, site=params['site']))

    print('endmodule')

    f.close()


if __name__ == "__main__":
    main()
