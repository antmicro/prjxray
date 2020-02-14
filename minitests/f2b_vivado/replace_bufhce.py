#!/usr/bin/env python3


import argparse
import re

PORT_RE = re.compile('.*\((.*)\).*')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--in_file', required=True)

    args = parser.parse_args()

    with open(args.in_file, 'r') as f:
        data = f.readlines()

    is_bufhce = False

    bufhce_wire = None
    bufgctrl_wire = None

    new_data = []
    for line in data:
        if 'BUFHCE #' in line or is_bufhce:
            is_bufhce = True

            m = PORT_RE.match(line)

            if line.startswith('.I'):
                if m:
                    bufgctrl_wire = m.groups(1)[0]
            if line.startswith('.O'):
                if m:
                    bufhce_wire = m.groups(1)[0]

            if ');' in line:
                is_bufhce = False

                new_line = 'assign {} = {};'.format(bufhce_wire, bufgctrl_wire)
                bufhce_wire = None
                bufgctrl_wire = None

                new_data.append(new_line)
        else:
            new_data.append(line)

    with open(args.in_file, 'w') as f:
        for line in new_data:
            f.write(line)



if __name__ == "__main__":
    main()
