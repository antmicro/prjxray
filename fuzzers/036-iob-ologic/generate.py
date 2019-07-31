#!/usr/bin/env python3

from prjxray.segmaker import Segmaker
from prjxray import verilog
import json

# Set to true to enable additional tags useful for tracing bit toggles.
DEBUG_FUZZER = False


def bitfilter(frame, word):
    if frame < 30 or frame > 37:
        return False

    return True


def handle_data_width(segmk, d):
    if 'DATA_WIDTH' not in d:
        return

    if d['DATA_RATE_OQ'] == 'DDR':
        return

    for opt in [2, 3, 4, 5, 6, 7, 8, 10, 14]:
        segmk.add_site_tag(
            d['site'], 'OSERDESE.DATA_WIDTH.W{}'.format(opt),
            d['DATA_WIDTH'] == opt)


def main():
    print("Loading tags")
    segmk = Segmaker("design.bits")

    with open('params.jl', 'r') as f:
        design = json.load(f)

        for d in design:
            site = d['site']

            handle_data_width(segmk, d)

            segmk.add_site_tag(site, 'OSERDESE.IN_USE', d['use_oserdese2'])

            if d['use_oserdese2']:
                segmk.add_site_tag(site, 'OQUSED', 1)

                for opt in ['SDR', 'DDR']:
                    segmk.add_site_tag(
                        site, 'OSERDESE.DATA_RATE_OQ.{}'.format(opt),
                        verilog.unquote(d['DATA_RATE_OQ']) == opt)

                for opt in ['BUF', 'SDR', 'DDR']:
                    segmk.add_site_tag(
                        site, 'OSERDESE.DATA_RATE_TQ.{}'.format(opt),
                        verilog.unquote(d['DATA_RATE_TQ']) == opt)

                for opt in ['SRVAL_OQ', 'SRVAL_TQ', 'INIT_OQ', 'INIT_TQ']:
                    segmk.add_site_tag(site, opt, d[opt])
                    segmk.add_site_tag(site, 'Z' + opt, 1 ^ d[opt])

                for opt in ['CLK', 'CLKDIV']:
                    if d['{}_USED'.format(opt)]:
                        for clk in ['clk_0_0', 'clk_0_90', 'clk_1_0', 'clk_1_90', 'clk_2_0', 'clk_2_90']:
                            tag = '{}_{}'.format(opt, clk)
                            segmk.add_site_tag(site, 'OSERDESE.{}'.format(tag), tag in d)

                        k = 'IS_{}_INVERTED'.format(opt)
                        segmk.add_site_tag(site, k, d[k])
                        segmk.add_site_tag(
                            site, 'ZINV_{}'.format(opt), 1 ^ d[k])

                for idx in range(4):
                    k = 'IS_T{}_INVERTED'.format(idx + 1)
                    segmk.add_site_tag(site, k, d[k])
                    segmk.add_site_tag(
                        site, 'ZINV_T{}'.format(idx + 1), 1 ^ d[k])

                for idx in range(8):
                    k = 'IS_D{}_INVERTED'.format(idx + 1)
                    segmk.add_site_tag(site, k, d[k])
                    segmk.add_site_tag(
                        site, 'ZINV_D{}'.format(idx + 1), 1 ^ d[k])

                for tristate_width in [1, 4]:
                    segmk.add_site_tag(
                        site,
                        'OSERDES.TRISTATE_WIDTH.W{}'.format(tristate_width),
                        d['TRISTATE_WIDTH'] == tristate_width)

                for opt in ['MASTER', 'SLAVE']:
                    segmk.add_site_tag(
                        site, 'OSERDES.SERDES_MODE.{}'.format(opt),
                        opt == verilog.unquote(d['OSERDES_MODE']))

            if d['oddr_mux_config'] == 'direct' and d[
                    'tddr_mux_config'] == 'direct':
                for opt in ['OPPOSITE_EDGE', 'SAME_EDGE']:
                    segmk.add_site_tag(
                        site, 'ODDR.DDR_CLK_EDGE.{}'.format(opt),
                        verilog.unquote(d['ODDR_CLK_EDGE']) == opt)

                segmk.add_site_tag(
                    site, 'TDDR.DDR_CLK_EDGE.INV',
                    d['ODDR_CLK_EDGE'] != d['TDDR_CLK_EDGE'])
                segmk.add_site_tag(
                    site, 'TDDR.DDR_CLK_EDGE.ZINV',
                    d['ODDR_CLK_EDGE'] == d['TDDR_CLK_EDGE'])

                if 'SRTYPE' in d:
                    for opt in ['ASYNC', 'SYNC']:
                        segmk.add_site_tag(
                            site, 'OSERDESE.SRTYPE.{}'.format(opt),
                            verilog.unquote(d['SRTYPE']) == opt)

                for opt in ['ASYNC', 'SYNC']:
                    segmk.add_site_tag(
                        site, 'OSERDESE.TSRTYPE.{}'.format(opt),
                        verilog.unquote(d['TSRTYPE']) == opt)

            if not d['use_oserdese2']:
                if d['oddr_mux_config'] == 'lut':
                    segmk.add_site_tag(site, 'OMUX.D1', 1)
                    segmk.add_site_tag(site, 'OQUSED', 1)
                elif d['oddr_mux_config'] == 'direct':
                    segmk.add_site_tag(site, 'OMUX.D1', 0)
                elif d['oddr_mux_config'] == 'none' and not d['io']:
                    segmk.add_site_tag(site, 'OQUSED', 0)

            segmk.add_site_tag(site, 'TQUSED', d['io'])

            if DEBUG_FUZZER:
                for k in d:
                    segmk.add_site_tag(
                        site, 'param_' + k + '_' + str(d[k]).replace(
                            ' ', '').replace('\n', ''), 1)

    segmk.compile(bitfilter=bitfilter)
    segmk.write(allow_empty=True)


if __name__ == "__main__":
    main()
