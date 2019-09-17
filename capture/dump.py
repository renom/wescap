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

class Dump:
    def __init__(self, data=[]):
        self.data = data
        
    def print(self, expand):
        for v in self.data:
            print('=== ' + v.src + ' -> ' + v.dst + ' (' + str(len(v.data)) + ') ===')
            
            if expand or v.data.count('\n') <= 10:
                print(v.data, end='\n\n')
            else:
                print('\n'.join(v.data.split('\n')[:10]), end='\n...\n\n')
