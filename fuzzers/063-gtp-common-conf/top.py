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

import json
import os
import random
from collections import namedtuple

random.seed(int(os.getenv("SEED"), 16))
from prjxray import util
from prjxray import verilog
from prjxray.db import Database

INT = "INT"
BIN = "BIN"


def gen_sites():
    db = Database(util.get_db_root(), util.get_part())
    grid = db.grid()
    for tile_name in sorted(grid.tiles()):
        loc = grid.loc_of_tilename(tile_name)
        gridinfo = grid.gridinfo_at_loc(loc)

        if gridinfo.tile_type not in [
                "GTP_COMMON",
                "GTP_COMMON_MID_RIGHT",
                "GTP_COMMON_MID_RIGHT",
        ]:
            continue

        for site_name, site_type in gridinfo.sites.items():
            if site_type != "GTPE2_COMMON":
                continue

            return site_name, site_type


def main():
    print('''
module top();
''')

    site_name, site_type = gen_sites()

    params = dict()
    params['site'] = site_name

    verilog_attr = ""

    verilog_attr = "#("

    fuz_dir = os.getenv("FUZDIR", None)
    assert fuz_dir
    with open(os.path.join(fuz_dir, "attrs.json"), "r") as attrs_file:
        attrs = json.load(attrs_file)

    for param, param_info in attrs.items():
        param_type = param_info["type"]
        param_values = param_info["values"]
        param_digits = param_info["digits"]

        if param_type == INT:
            value = random.choice(param_values)
            value_str = value
        else:
            assert param_type == BIN
            value = random.randint(0, param_values[0])
            value_str = "{digits}'b{value:0{digits}b}".format(
                value=value, digits=param_digits)

        params[param] = value

        verilog_attr += """
    .{}({}),""".format(param, value_str)

    verilog_attr = verilog_attr.rstrip(",")
    verilog_attr += "\n)"

    print("(* KEEP, DONT_TOUCH *)")
    print("GTPE2_COMMON {} gtp_common ();".format(verilog_attr))
    print("endmodule")

    with open('params.json', 'w') as f:
        json.dump(params, f, indent=2)


if __name__ == '__main__':
    main()
