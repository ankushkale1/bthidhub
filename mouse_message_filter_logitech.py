# Copyright (c) 2020 ruundii. All rights reserved.
#
from hid_message_filter import HIDMessageFilter

# default mouse filter

# first 16 bits are flags for buttons. 01 is left button, 02 is right, 04 is scroll
# second 16 bits are X -32767 to 32767
# third 16 bits are Y -32767 to 32767
# then 8 bits of wheel -127 to 127

# from the default sdp record

# Logitech Wireless Mouse
# 0x05, 0x01,                    // Usage Page (Generic Desktop)        0
# 0x09, 0x02,                    // Usage (Mouse)                       2
# 0xa1, 0x01,                    // Collection (Application)            4
# 0x85, 0x02,                    //  Report ID (2)                      6
# 0x09, 0x01,                    //  Usage (Pointer)                    8
# 0xa1, 0x00,                    //  Collection (Physical)              10
# 0x05, 0x09,                    //   Usage Page (Button)               12
# 0x19, 0x01,                    //   Usage Minimum (1)                 14
# 0x29, 0x10,                    //   Usage Maximum (16)                16
# 0x15, 0x00,                    //   Logical Minimum (0)               18
# 0x25, 0x01,                    //   Logical Maximum (1)               20
# 0x95, 0x10,                    //   Report Count (16)                 22
# 0x75, 0x01,                    //   Report Size (1)                   24
# 0x81, 0x02,                    //   Input (Data,Var,Abs)              26
# 0x05, 0x01,                    //   Usage Page (Generic Desktop)      28
# 0x16, 0x01, 0xf8,              //   Logical Minimum (-2047)           30
# 0x26, 0xff, 0x07,              //   Logical Maximum (2047)            33
# 0x75, 0x0c,                    //   Report Size (12)                  36
# 0x95, 0x02,                    //   Report Count (2)                  38
# 0x09, 0x30,                    //   Usage (X)                         40
# 0x09, 0x31,                    //   Usage (Y)                         42
# 0x81, 0x06,                    //   Input (Data,Var,Rel)              44
# 0x15, 0x81,                    //   Logical Minimum (-127)            46
# 0x25, 0x7f,                    //   Logical Maximum (127)             48
# 0x75, 0x08,                    //   Report Size (8)                   50
# 0x95, 0x01,                    //   Report Count (1)                  52
# 0x09, 0x38,                    //   Usage (Wheel)                     54
# 0x81, 0x06,                    //   Input (Data,Var,Rel)              56
# 0x05, 0x0c,                    //   Usage Page (Consumer Devices)     58
# 0x0a, 0x38, 0x02,              //   Usage (AC Pan)                    60
# 0x95, 0x01,                    //   Report Count (1)                  63
# 0x81, 0x06,                    //   Input (Data,Var,Rel)              65
# 0xc0,                          //  End Collection                     67
# 0xc0,                          // End Collection                      68

# 0x06, 0x00, 0xff,              // Usage Page (Vendor Defined Page 1)  69
# 0x09, 0x01,                    // Usage (Vendor Usage 1)              72

# 0xa1, 0x01,                    // Collection (Application)            74
# 0x85, 0x10,                    //  Report ID (16)                     76
# 0x75, 0x08,                    //  Report Size (8)                    78
# 0x95, 0x06,                    //  Report Count (6)                   80
# 0x15, 0x00,                    //  Logical Minimum (0)                82
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              84
# 0x09, 0x01,                    //  Usage (Vendor Usage 1)             87
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               89
# 0x09, 0x01,                    //  Usage (Vendor Usage 1)             91
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              93
# 0xc0,                          // End Collection                      95

# 0x06, 0x00, 0xff,              // Usage Page (Vendor Defined Page 1)  96
# 0x09, 0x02,                    // Usage (Vendor Usage 2)              99

# 0xa1, 0x01,                    // Collection (Application)            101
# 0x85, 0x11,                    //  Report ID (17)                     103
# 0x75, 0x08,                    //  Report Size (8)                    105
# 0x95, 0x13,                    //  Report Count (19)                  107
# 0x15, 0x00,                    //  Logical Minimum (0)                109
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              111
# 0x09, 0x02,                    //  Usage (Vendor Usage 2)             114
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               116
# 0x09, 0x02,                    //  Usage (Vendor Usage 2)             118
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              120
# 0xc0,                          // End Collection                      122

# 0x06, 0x00, 0xff,              // Usage Page (Vendor Defined Page 1)  123
# 0x09, 0x04,                    // Usage (Vendor Usage 0x04)           126

# 0xa1, 0x01,                    // Collection (Application)            128
# 0x85, 0x20,                    //  Report ID (32)                     130
# 0x75, 0x08,                    //  Report Size (8)                    132
# 0x95, 0x0e,                    //  Report Count (14)                  134
# 0x15, 0x00,                    //  Logical Minimum (0)                136
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              138
# 0x09, 0x41,                    //  Usage (Vendor Usage 0x41)          141
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               143
# 0x09, 0x41,                    //  Usage (Vendor Usage 0x41)          145
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              147
# 0x85, 0x21,                    //  Report ID (33)                     149
# 0x95, 0x1f,                    //  Report Count (31)                  151
# 0x15, 0x00,                    //  Logical Minimum (0)                153
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              155
# 0x09, 0x42,                    //  Usage (Vendor Usage 0x42)          158
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               160
# 0x09, 0x42,                    //  Usage (Vendor Usage 0x42)          162
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              164
# 0xc0,                          // End Collection                      166

#There are 16 buttons, and each button's state is represented by 1 bit., so first 16 bits / 2 bytes for button state
# X and Y coordinates are represented by 12 bits each. so 24bits for XY Logical Minimum (-2047) and Logical Maximum (2047), 3 bytes
# The wheel position is represented by 8 bits. Logical Minimum (-127) and Logical Maximum (127)
# The AC Pan feature is represented by 1 bit.
#if you receive a report with the ID of 2, you would expect to find data for buttons, X and Y coordinates, and the wheel position in that report, each in the format specified by the descriptor.

class MouseMessageFilterLogitech(HIDMessageFilter):
    def __init__(self):
        self.message_size = 7

    def filter_message_to_host(self, msg):
        # if len(msg) != self.message_size:
        #     return None
        try:
            hex_string = ' '.join([f'{byte:02X}' for byte in msg])
            print("Raw Text: " + hex_string)
            #msg = b'\xa1\x02' + \
            #    self.get_buttons_flags(msg) + self.get_xy(msg) + self.get_wheel(msg) + self.get_acFlag(msg)
            msg = b'\xa1' + msg
            #hex_string = ' '.join([f'{byte:02X}' for byte in msg])
            #print("Parsed Text: " + hex_string)
        except Exception as e:
            print(f"An error occurred: {e}")
        return msg

    def get_buttons_flags(self, msg):
        #print("Buttons: "+msg[1:3])
        return msg[1:3]

    # def get_x(self, msg):
    #     # Extract the first 12 bits (X)
    #     x = ((msg[4] << 4) | (msg[5] >> 4)) & 0xFFF
    #     print("X: "+x)
    #     return x
    #
    # def get_y(self, msg):
    #     # Extract the next 12 bits (Y)
    #     y = (((msg[5] & 0xF) << 8) | msg[6]) & 0xFFF
    #     print("Y: "+y)
    #     return y

    def get_xy(self, msg):
        #print("XY: "+msg[3:6])
        return msg[3:6]

    def get_wheel(self, msg):
        #print("Wheel: "+msg[6:7])
        return msg[6:7]

    def get_acFlag(self, msg):
        #print("Wheel: "+msg[6:7])
        return msg[7:8]

    def filter_message_from_host(self, msg):
        return None
