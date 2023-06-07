from bitarray.util import ba2int
from bitarray import bitarray
from mouse_message_filter import MouseMessageFilter

m = MouseMessageFilter()

# generic mouse test
#  Button: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 | X:     -1 | Y:    -13 | Wheel:    0
print(m.filter_message_to_host(b'\x00\x00\xff\xff\xf3\xff\x00')
      == b'\xa1\x03\x00\x00\xff\xff\xf3\xff\x00')

#  Button: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 | X:      1 | Y:      5 | Wheel:    0
print(m.filter_message_to_host(b'\x00\x00\x01\x00\x05\x00\x00')
      == b'\xa1\x03\x00\x00\x01\x00\x05\x00\x00')

#  Button: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 | X:      0 | Y:      0 | Wheel:    1
print(m.filter_message_to_host(b'\x00\x00\x00\x00\x00\x00\x01')
      == b'\xa1\x03\x00\x00\x00\x00\x00\x00\x01')

#  Button: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 | X:      0 | Y:      0 | Wheel:   -1
print(m.filter_message_to_host(b'\x00\x00\x00\x00\x00\x00\xff')
      == b'\xa1\x03\x00\x00\x00\x00\x00\x00\xff')

#  Button: 1  0  1  0  0  0  0  0  0  0  0  0  0  0  0  0 | X:      0 | Y:      0 | Wheel:    0
print(m.filter_message_to_host(b'\x05\x00\x00\x00\x00\x00\x00')
      == b'\xa1\x03\x05\x00\x00\x00\x00\x00\x00')
