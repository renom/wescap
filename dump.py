#!/usr/bin/env python3

# This file is part of Wescap.
#
# Wescap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wescap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wescap.  If not, see <https://www.gnu.org/licenses/>.

# Usage:
# python dump.py [-t /usr/bin/tshark] [-i eth0] [-q] [-e] [-p 15000 14999] [-o dump.csv] [-H host:port]

import argparse, sys
from subprocess import Popen, PIPE, STDOUT
from capture import decoder

parser = argparse.ArgumentParser(description='Dump the Battle for Wesnoth data.')
parser.add_argument('-t', '--tshark', dest='tshark', default='/usr/bin/tshark', help='a path to the tshark binary')
parser.add_argument('-i', '--interface', dest='interface', default='lo', help='a network interface to monitor')
parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                    default=False, help='hide the output')
parser.add_argument('-e', '--expand', dest='expand', action='store_true',
                    default=False, help='expand the output')
parser.add_argument('-p', '--ports', dest='ports', default=[15000], type=int, nargs='+', help='server port(s) to capture')
parser.add_argument('-o', '--output', dest='output', help='a path to save dump')
parser.add_argument('-H', '--host', dest='host', help='the address to highlight as a host player')
args = parser.parse_args()

tshark = args.tshark
interface = args.interface
quiet = args.quiet
expand = args.expand
displayFilter = ' or '.join(['tcp.srcport == '+str(port)+' or tcp.dstport == '+str(port) for port in args.ports])
file = args.output
output = file is not None
replacements = {args.host: 'host'} if args.host is not None else {}

if quiet == True and not output:
    sys.exit("The quiet mode requires an output file.")

cmd = (tshark, '-l', '-E', 'separator=,', '-i', interface, '-T', 'fields',
        '-e', 'ip.src', '-e', 'tcp.srcport', '-e', 'ip.dst',
        '-e', 'tcp.dstport', '-e', 'data.data',
        '-Y', displayFilter)
p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True, bufsize=1)

if output:
    file = open(file, "w")
if not quiet:
    d = decoder.Decoder(replacements)
for line in iter(p.stdout.readline, ''):
    if not quiet:
        dump = d.decodeText(line)
        dump.print(expand)
    if output:
        file.write(line)
if output:
    file.close()
