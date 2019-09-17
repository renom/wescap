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
# python decode.py dump.csv [-e] [-H host:port]

import argparse
from capture import decoder

parser = argparse.ArgumentParser(description='Decode the existing dump.')
parser.add_argument('file', metavar='FILE',
                    help='a dump file to parse')
parser.add_argument('-e', '--expand', dest='expand', action='store_true',
                    default=False, help='expand the output')
parser.add_argument('-H', '--host', dest='host', help='the address to highlight as a host player')
args = parser.parse_args()

# Get the path of the dump and other parameters (if latter are provided)
path = args.file
expand = args.expand
replacements = {args.host: 'host'} if args.host is not None else {}

d = decoder.Decoder(replacements)
dump = d.decodeFile(path)
dump.print(expand)
