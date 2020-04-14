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

import csv
import gzip
import struct
from capture.packet import Packet
from capture.dump import Dump

class Decoder:
    def __init__(self, replacements={}):
        self.counter = 1
        self.replacements = replacements
        self.__buffer = {}
    
    def reset(self):
        self.__buffer = {}
    
    def replace(self, address, port):
        full_address = address + ':' + port
        
        if full_address in self.replacements:
            return self.replacements[full_address]
        
        if port == '15000':
            self.replacements[full_address] = 'server'
            return self.replacements[full_address]
        
        self.replacements[full_address] = 'player'+str(self.counter)
        self.counter += 1
        return self.replacements[full_address]
    
    def decodeFile(self, path):
        with open(path, newline='') as csvfile:
            return self.decode(csvfile)
    
    def decodeText(self, string):
        return self.decode(string.splitlines())
    
    def decode(self, csvData):
        packets = []
        reader = csv.reader(csvData)
        for row in reader:
            if len(row) != 5 or row[4] == '':
                continue
            
            src = self.replace(row[0], row[1])
            dst = self.replace(row[2], row[3])
            
            hasBuffer = self.hasBuffer(src, dst)
            buffer = ''
            if hasBuffer:
                buffer = self.buffer(src, dst) + row[4]
            else:
                buffer = row[4]
            
            size = Decoder.size(buffer)
            bufLength = int(len(buffer) / 2) - 4
            
            if size == bufLength:
                data = Decoder.decompress(buffer).strip()
                if len(data) > 0:
                    packets.append(Packet(src, dst, data))
                if hasBuffer:
                    self.clearBuffer()
            elif size < bufLength:
                data = Decoder.decompress(buffer[:(size+4)*2]).strip()
                packets.append(Packet(src, dst, data))
                self.updateBuffer(src, dst, buffer[(size+4)*2:])
            else:
                self.updateBuffer(src, dst, buffer)
                
        return Dump(packets)
    
    def buffer(self, src, dst):
        return self.__buffer[src + '_' + dst]
    
    def updateBuffer(self, src, dst, data):
        self.__buffer = data
    
    def clearBuffer(self, src, dst):
        self.__buffer.pop(src + '_' + dst, None)
    
    def hasBuffer(self, src, dst):
        return src + '_' + dst in self.__buffer
    
    @staticmethod
    def size(data):
        if len(data) < 8:
            return 0
        return struct.unpack('>I', Decoder.stringToBytes(data[:8]))[0]

    @staticmethod
    def decompress(string):
        return gzip.decompress(Decoder.stringToBytes(string[8:])).decode()
    
    @staticmethod
    def stringToBytes(string):
        result = bytearray()
        for i in range(0, len(string), 2):
            result.append(int(string[i:i+2], 16))
        return result
