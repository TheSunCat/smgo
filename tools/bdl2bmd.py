import sys
import struct

#====================================================================================================

class MDL3entry:
  def __init__(self,fn,n):
    f = open(fn,'rb')
    while( f.read(4) != b'MDL3' ): f.read(12)
    base = f.tell() - 4
    f.read(4)
    if ( n >= struct.unpack('>h',f.read(2))[0] ): raise Exception('MDL3 entry index to high')
    f.read(2)
    ss1_offset = struct.unpack('>L',f.read(4))[0]
    ss2_offset = struct.unpack('>L',f.read(4))[0]
    ss3_offset = struct.unpack('>L',f.read(4))[0]
    ss4_offset = struct.unpack('>L',f.read(4))[0]

    f.seek(base + ss1_offset + 8*n)
    ss1_data_offset = struct.unpack('>L',f.read(4))[0]
    ss1_data_size = struct.unpack('>L',f.read(4))[0]
    f.seek(f.tell() - 8 + ss1_data_offset)
    self.subsection1 = f.read(ss1_data_size)

    f.seek(base + ss2_offset + 16*n)
    self.subsection2 = f.read(16)

    f.seek(base + ss3_offset + 8*n)
    self.subsection3 = f.read(8)

    f.seek(base + ss4_offset + n)
    self.subsection4 = f.read(1)

#====================================================================================================

class StringTable:
  def __init__(self,f):
    self.num_entries = struct.unpack('>h',f.read(2))[0]
    f.read(2)
    self.unknown1 = []
    self.unknown2 = []
    self.offset = []
    for i in range(self.num_entries):
      self.unknown1.append(f.read(1))
      self.unknown2.append(f.read(1))
      self.offset.append(struct.unpack('>h',f.read(2))[0])

    self.string = []
    for i in range(self.num_entries):
      self.string.append('')
      while ( 1 ):
        b = f.read(1)
        if ( b == b'\x00' ): break
        self.string[i] += b.decode('ascii')

#====================================================================================================

def align(n,l):
  return n + (l - n % l) % l

#====================================================================================================

fi = open(sys.argv[1],'rb')
fo = open(sys.argv[2],'wb')

#----------------------------------------------------------------------------------------------------

fi.seek(32)
while ( fi.read(4) != b'MDL3' ):
  fi.seek(fi.tell() + struct.unpack('>L',fi.read(4))[0] - 4)
MDL3base = fi.tell() - 4
MDL3size = struct.unpack('>L',fi.read(4))[0]
fi.seek(0)

#----------------------------------------------------------------------------------------------------

fi.read(8)
fo.write(b'J3D2bmd3')
fo.write(struct.pack('>L',struct.unpack('>L',fi.read(4))[0] - MDL3size))
fi.read(4)
fo.write(struct.pack('>L',8))

fo.write(fi.read(MDL3base - 16))
fi.seek(MDL3base + MDL3size)

#----------------------------------------------------------------------------------------------------

fo.write(fi.read(4))
TEX1size = struct.unpack('>L',fi.read(4))[0]
fo.write(struct.pack('>L',TEX1size))
fo.write(fi.read(TEX1size - 8))

#____________________________________________________________________________________________________
