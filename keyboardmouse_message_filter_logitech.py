# Copyright (c) 2020 ruundii. All rights reserved.
#
from hid_message_filter import HIDMessageFilter

# from the default sdp record

# Logitech Wireless Keyboard & Mouse combo
# 0x05, 0x01,                    // Usage Page (Generic Desktop)        0
# 0x09, 0x06,                    // Usage (Keyboard)                    2
# 0xa1, 0x01,                    // Collection (Application)            4
# 0x85, 0x01,                    //  Report ID (1)                      6
# 0x95, 0x08,                    //  Report Count (8)                   8
# 0x75, 0x01,                    //  Report Size (1)                    10
# 0x15, 0x00,                    //  Logical Minimum (0)                12
# 0x25, 0x01,                    //  Logical Maximum (1)                14
# 0x05, 0x07,                    //  Usage Page (Keyboard)              16
# 0x19, 0xe0,                    //  Usage Minimum (224)                18
# 0x29, 0xe7,                    //  Usage Maximum (231)                20
# 0x81, 0x02,                    //  Input (Data,Var,Abs)               22
# 0x95, 0x06,                    //  Report Count (6)                   24
# 0x75, 0x08,                    //  Report Size (8)                    26
# 0x15, 0x00,                    //  Logical Minimum (0)                28
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              30
# 0x05, 0x07,                    //  Usage Page (Keyboard)              33
# 0x19, 0x00,                    //  Usage Minimum (0)                  35
# 0x2a, 0xff, 0x00,              //  Usage Maximum (255)                37
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               40
# 0x85, 0x0e,                    //  Report ID (14)                     42
# 0x05, 0x08,                    //  Usage Page (LEDs)                  44
# 0x95, 0x05,                    //  Report Count (5)                   46
# 0x75, 0x01,                    //  Report Size (1)                    48
# 0x15, 0x00,                    //  Logical Minimum (0)                50
# 0x25, 0x01,                    //  Logical Maximum (1)                52
# 0x19, 0x01,                    //  Usage Minimum (1)                  54
# 0x29, 0x05,                    //  Usage Maximum (5)                  56
# 0x91, 0x02,                    //  Output (Data,Var,Abs)              58
# 0x95, 0x01,                    //  Report Count (1)                   60
# 0x75, 0x03,                    //  Report Size (3)                    62
# 0x91, 0x01,                    //  Output (Cnst,Arr,Abs)              64
# 0xc0,                          // End Collection                      66
# 0x05, 0x01,                    // Usage Page (Generic Desktop)        67
# 0x09, 0x02,                    // Usage (Mouse)                       69
# 0xa1, 0x01,                    // Collection (Application)            71
# 0x85, 0x02,                    //  Report ID (2)                      73
# 0x09, 0x01,                    //  Usage (Pointer)                    75
# 0xa1, 0x00,                    //  Collection (Physical)              77
# 0x05, 0x09,                    //   Usage Page (Button)               79
# 0x19, 0x01,                    //   Usage Minimum (1)                 81
# 0x29, 0x10,                    //   Usage Maximum (16)                83
# 0x15, 0x00,                    //   Logical Minimum (0)               85
# 0x25, 0x01,                    //   Logical Maximum (1)               87
# 0x95, 0x10,                    //   Report Count (16)                 89
# 0x75, 0x01,                    //   Report Size (1)                   91
# 0x81, 0x02,                    //   Input (Data,Var,Abs)              93
# 0x05, 0x01,                    //   Usage Page (Generic Desktop)      95
# 0x16, 0x01, 0xf8,              //   Logical Minimum (-2047)           97
# 0x26, 0xff, 0x07,              //   Logical Maximum (2047)            100
# 0x75, 0x0c,                    //   Report Size (12)                  103
# 0x95, 0x02,                    //   Report Count (2)                  105
# 0x09, 0x30,                    //   Usage (X)                         107
# 0x09, 0x31,                    //   Usage (Y)                         109
# 0x81, 0x06,                    //   Input (Data,Var,Rel)              111
# 0x15, 0x81,                    //   Logical Minimum (-127)            113
# 0x25, 0x7f,                    //   Logical Maximum (127)             115
# 0x75, 0x08,                    //   Report Size (8)                   117
# 0x95, 0x01,                    //   Report Count (1)                  119
# 0x09, 0x38,                    //   Usage (Wheel)                     121
# 0x81, 0x06,                    //   Input (Data,Var,Rel)              123
# 0x05, 0x0c,                    //   Usage Page (Consumer Devices)     125
# 0x0a, 0x38, 0x02,              //   Usage (AC Pan)                    127
# 0x95, 0x01,                    //   Report Count (1)                  130
# 0x81, 0x06,                    //   Input (Data,Var,Rel)              132
# 0xc0,                          //  End Collection                     134
# 0xc0,                          // End Collection                      135
# 0x05, 0x0c,                    // Usage Page (Consumer Devices)       136
# 0x09, 0x01,                    // Usage (Consumer Control)            138
# 0xa1, 0x01,                    // Collection (Application)            140
# 0x85, 0x03,                    //  Report ID (3)                      142
# 0x75, 0x10,                    //  Report Size (16)                   144
# 0x95, 0x02,                    //  Report Count (2)                   146
# 0x15, 0x01,                    //  Logical Minimum (1)                148
# 0x26, 0xff, 0x02,              //  Logical Maximum (767)              150
# 0x19, 0x01,                    //  Usage Minimum (1)                  153
# 0x2a, 0xff, 0x02,              //  Usage Maximum (767)                155
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               158
# 0xc0,                          // End Collection                      160
# 0x05, 0x01,                    // Usage Page (Generic Desktop)        161
# 0x09, 0x80,                    // Usage (System Control)              163
# 0xa1, 0x01,                    // Collection (Application)            165
# 0x85, 0x04,                    //  Report ID (4)                      167
# 0x75, 0x02,                    //  Report Size (2)                    169
# 0x95, 0x01,                    //  Report Count (1)                   171
# 0x15, 0x01,                    //  Logical Minimum (1)                173
# 0x25, 0x03,                    //  Logical Maximum (3)                175
# 0x09, 0x82,                    //  Usage (System Sleep)               177
# 0x09, 0x81,                    //  Usage (System Power Down)          179
# 0x09, 0x83,                    //  Usage (System Wake Up)             181
# 0x81, 0x60,                    //  Input (Data,Arr,Abs,NoPref,Null)   183
# 0x75, 0x06,                    //  Report Size (6)                    185
# 0x81, 0x03,                    //  Input (Cnst,Var,Abs)               187
# 0xc0,                          // End Collection                      189
# 0x06, 0x00, 0xff,              // Usage Page (Vendor Defined Page 1)  190
# 0x09, 0x01,                    // Usage (Vendor Usage 1)              193
# 0xa1, 0x01,                    // Collection (Application)            195
# 0x85, 0x10,                    //  Report ID (16)                     197
# 0x75, 0x08,                    //  Report Size (8)                    199
# 0x95, 0x06,                    //  Report Count (6)                   201
# 0x15, 0x00,                    //  Logical Minimum (0)                203
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              205
# 0x09, 0x01,                    //  Usage (Vendor Usage 1)             208
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               210
# 0x09, 0x01,                    //  Usage (Vendor Usage 1)             212
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              214
# 0xc0,                          // End Collection                      216
# 0x06, 0x00, 0xff,              // Usage Page (Vendor Defined Page 1)  217
# 0x09, 0x02,                    // Usage (Vendor Usage 2)              220
# 0xa1, 0x01,                    // Collection (Application)            222
# 0x85, 0x11,                    //  Report ID (17)                     224
# 0x75, 0x08,                    //  Report Size (8)                    226
# 0x95, 0x13,                    //  Report Count (19)                  228
# 0x15, 0x00,                    //  Logical Minimum (0)                230
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              232
# 0x09, 0x02,                    //  Usage (Vendor Usage 2)             235
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               237
# 0x09, 0x02,                    //  Usage (Vendor Usage 2)             239
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              241
# 0xc0,                          // End Collection                      243
# 0x06, 0x00, 0xff,              // Usage Page (Vendor Defined Page 1)  244
# 0x09, 0x04,                    // Usage (Vendor Usage 0x04)           247
# 0xa1, 0x01,                    // Collection (Application)            249
# 0x85, 0x20,                    //  Report ID (32)                     251
# 0x75, 0x08,                    //  Report Size (8)                    253
# 0x95, 0x0e,                    //  Report Count (14)                  255
# 0x15, 0x00,                    //  Logical Minimum (0)                257
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              259
# 0x09, 0x41,                    //  Usage (Vendor Usage 0x41)          262
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               264
# 0x09, 0x41,                    //  Usage (Vendor Usage 0x41)          266
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              268
# 0x85, 0x21,                    //  Report ID (33)                     270
# 0x95, 0x1f,                    //  Report Count (31)                  272
# 0x15, 0x00,                    //  Logical Minimum (0)                274
# 0x26, 0xff, 0x00,              //  Logical Maximum (255)              276
# 0x09, 0x42,                    //  Usage (Vendor Usage 0x42)          279
# 0x81, 0x00,                    //  Input (Data,Arr,Abs)               281
# 0x09, 0x42,                    //  Usage (Vendor Usage 0x42)          283
# 0x91, 0x00,                    //  Output (Data,Arr,Abs)              285
# 0xc0,                          // End Collection                      287


#There are 16 buttons, and each button's state is represented by 1 bit., so first 16 bits / 2 bytes for button state
# X and Y coordinates are represented by 12 bits each. so 24bits for XY Logical Minimum (-2047) and Logical Maximum (2047), 3 bytes
# The wheel position is represented by 8 bits. Logical Minimum (-127) and Logical Maximum (127)
# The AC Pan feature is represented by 1 bit.
#if you receive a report with the ID of 2, you would expect to find data for buttons, X and Y coordinates, and the wheel position in that report, each in the format specified by the descriptor.

class KeyboardMouseMessageFilterLogitech(HIDMessageFilter):
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
