# Copyright (c) 2020 ruundii. All rights reserved.

import asyncio
import sys
from signal import SIGINT
import json
import logging
import logging.config
import asyncio_glib

from dasbus.connection import SystemMessageBus
from bluetooth_devices import BluetoothDeviceRegistry
from hid_devices import HIDDeviceRegistry
from web import Web, BluetoothAdapter

if __name__ == "__main__":
    server_config = json.load(open("logger_config.json", "r"))
    logging.config.dictConfig(server_config)
    root_logger = logging.getLogger()
    root_logger.info(f"Log level set to {logging.getLevelName(root_logger.getEffectiveLevel())}")
    #root_logger.info("Log level set to %s" % logging.getLevelName(root_logger.getEffectiveLevel()))

    asyncio.set_event_loop_policy(asyncio_glib.GLibEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(SIGINT, sys.exit)
    bus = SystemMessageBus()
    bluetooth_devices = BluetoothDeviceRegistry(bus, loop)
    hid_devices = HIDDeviceRegistry(loop)
    hid_devices.set_bluetooth_devices(bluetooth_devices)
    bluetooth_devices.set_hid_devices(hid_devices)
    adapter = BluetoothAdapter(bus, loop, bluetooth_devices, hid_devices)
    web = Web(loop, adapter, bluetooth_devices, hid_devices)
    loop.run_forever()
