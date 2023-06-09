# Copyright (c) 2020 ruundii. All rights reserved.

import asyncio
import socket
import os
import logging
from typing import List
from dasbus.connection import SystemMessageBus

OBJECT_MANAGER_INTERFACE = 'org.freedesktop.DBus.ObjectManager'
DEVICE_INTERFACE = 'org.bluez.Device1'
PROPERTIES_INTERFACE = 'org.freedesktop.DBus.Properties'
INPUT_DEVICE_INTERFACE = 'org.bluez.Input1'
INPUT_HOST_INTERFACE = 'org.bluez.InputHost1'

IGNORE_INPUT_DEVICES = True


class BluetoothDevice:
    def __init__(self,
                 bus: SystemMessageBus,
                 loop: asyncio.AbstractEventLoop,
                 device_registry,
                 object_path: str,
                 is_host: bool,
                 control_socket_path,
                 interrupt_socket_path):

        self.logger = logging.getLogger(__class__.__name__)
        self.device = bus.get_proxy(
            service_name="org.bluez", object_path=object_path, interface_name=DEVICE_INTERFACE)
        self.props = bus.get_proxy(
            service_name="org.bluez", object_path=object_path, interface_name=PROPERTIES_INTERFACE)
        self.props.PropertiesChanged.connect(
            self.device_connected_state_changed)

        self.bus = bus
        self.loop = loop
        self.device_registry = device_registry
        self.object_path = object_path
        self.is_host = is_host
        self.control_socket_path = control_socket_path
        self.control_socket = None
        self.interrupt_socket_path = interrupt_socket_path
        self.interrupt_socket = None
        self.sockets_connected = False

        self.logger.info(f"BT Device {object_path} created")
        asyncio.run_coroutine_threadsafe(
            self.reconcile_connected_state(1), loop=self.loop)

    async def reconcile_connected_state(self, delay):
        await asyncio.sleep(delay)
        try:
            if self.connected and not self.sockets_connected:
                await self.connect_sockets()
            elif not self.connected and self.sockets_connected:
                self.disconnect_sockets()
        except Exception as exc:
            self.logger.error(f"Possibly dbus error during reconcile_connected_state {exc}")

    async def connect_sockets(self):
        if self.sockets_connected or self.control_socket_path is None or self.interrupt_socket_path is None:
            return
        self.logger.info(f"Connecting sockets for {self.object_path}")
        if not self.connected:
            self.logger.info("BT Device is not connected. No point connecting sockets. Skipping.")
        try:
            self.control_socket = socket.socket(
                socket.AF_UNIX, socket.SOCK_SEQPACKET)
            self.control_socket.connect(self.control_socket_path)
            self.control_socket.setblocking(False)

            self.interrupt_socket = socket.socket(
                socket.AF_UNIX, socket.SOCK_SEQPACKET)
            self.interrupt_socket.connect(self.interrupt_socket_path)
            self.interrupt_socket.setblocking(False)
            self.sockets_connected = True
            if (self.is_host):
                self.device_registry.connected_hosts.append(self)
                addr = self.object_path[-17:].replace("_", ":")
                # asyncio.create_task(self.device_registry.switch_to_master(addr))
            else:
                self.device_registry.connected_devices.append(self)
            self.logger.info(f"Connected sockets for {self.object_path}")
            asyncio.run_coroutine_threadsafe(
                self.loop_of_fun(True), loop=self.loop)
            asyncio.run_coroutine_threadsafe(
                self.loop_of_fun(False), loop=self.loop)
        except Exception as err:
            self.logger.error(f"Error while connecting sockets for {self.object_path}. Will retry in a sec {err}")
            try:
                self.control_socket.close()
                self.interrupt_socket.close()
            except:
                pass
            await asyncio.sleep(1)
            asyncio.run_coroutine_threadsafe(
                self.connect_sockets(), loop=self.loop)

    def disconnect_sockets(self):
        if self.control_socket is not None:
            self.control_socket.close()
            self.control_socket = None
        if self.interrupt_socket is not None:
            self.interrupt_socket.close()
            self.interrupt_socket = None
        if (self.is_host and self in self.device_registry.connected_hosts):
            self.device_registry.connected_hosts.remove(self)
        elif self in self.device_registry.connected_devices:
            self.device_registry.connected_devices.remove(self)
        self.sockets_connected = False

        self.logger.info(f"Disconnected  sockets for {self.object_path}")

    async def loop_of_fun(self, is_ctrl):
        sock = self.control_socket if is_ctrl else self.interrupt_socket
        while sock is not None:
            try:
                msg = await self.loop.sock_recv(sock, 255)
            except Exception:
                self.logger.error(f"Cannot read data from socket. {self.object_path} Closing sockets")
                if self is not None:
                    try:
                        self.disconnect_sockets()
                    except:
                        self.logger.error("Error while disconnecting sockets")
                self.logger.error("Arranging reconnect")
                asyncio.run_coroutine_threadsafe(
                    self.reconcile_connected_state(1), loop=self.loop)
                break
            if msg is None or len(msg) == 0:
                continue
            self.device_registry.send_message(msg, not self.is_host, is_ctrl)
            sock = self.control_socket if is_ctrl else self.interrupt_socket

    @property
    def name(self):
        return self.device.Name

    @property
    def alias(self):
        return self.device.Alias

    @property
    def connected(self):
        return self.device.Connected

    def __eq__(self, other):
        return self.object_path == other.object_path

    def device_connected_state_changed(self, arg1, arg2, arg3):
        self.logger.debug("device_connected_state_changed")
        asyncio.run_coroutine_threadsafe(
            self.reconcile_connected_state(1), loop=self.loop)
        if self.device_registry.on_devices_changed_handler is not None:
            asyncio.run_coroutine_threadsafe(
                self.device_registry.on_devices_changed_handler(), loop=self.loop)

    def finalise(self):
        self.props.PropertiesChanged.disconnect(
            self.device_connected_state_changed)
        self.control_socket_path = None
        self.interrupt_socket_path = None
        # close sockets
        self.disconnect_sockets()
        self.logger.debug(f"BT Device {self.object_path} finalised")

    def __del__(self):
        self.logger.debug(f"BT Device {self.object_path} removed")


class BluetoothDeviceRegistry:
    def __init__(self, bus: SystemMessageBus, loop: asyncio.AbstractEventLoop):
        self.logger = logging.getLogger(__class__.__name__)
        self.bus = bus
        self.loop = loop
        self.all = {}
        self.connected_hosts = []
        self.connected_devices = []
        self.on_devices_changed_handler = None
        self.hid_devices = None
        self.current_host_index = 0

    def set_hid_devices(self, hid_devices):
        self.hid_devices = hid_devices

    def set_on_devices_changed_handler(self, handler):
        self.on_devices_changed_handler = handler

    def add_devices(self):
        self.logger.debug("Adding all BT devices")
        om = self.bus.get_proxy(
            service_name="org.bluez", object_path="/", interface_name=OBJECT_MANAGER_INTERFACE)
        objs = om.GetManagedObjects()

        for obj in list(objs):
            if INPUT_HOST_INTERFACE in objs[obj]:
                self.add_device(obj, True)

            elif INPUT_DEVICE_INTERFACE in objs[obj]:
                self.add_device(obj, False)

    def add_device(self, device_object_path: str, is_host: bool):
        if (IGNORE_INPUT_DEVICES and not is_host):
            return

        if device_object_path in self.all:
            self.logger.warning(f"Device {device_object_path} already exist. Cannot add. Skipping.")
            return
        # ensure master role for this connection, otherwise latency of sending packets to hosts may get pretty bad
        # asyncio.ensure_future(self.switch_to_master(device_object_path[-17:].replace("_",":")))
        p = self.bus.get_proxy(service_name="org.bluez", object_path=device_object_path,
                               interface_name=INPUT_HOST_INTERFACE if is_host else INPUT_DEVICE_INTERFACE)
        device = BluetoothDevice(
            self.bus, self.loop, self, device_object_path, is_host, p.SocketPathCtrl, p.SocketPathIntr)
        self.all[device_object_path] = device

    async def switch_to_master(self, device_address):
        self.logger.debug(f"switch to master called for {device_address}")
        while self.is_slave(device_address):
            try:
                success = os.system("sudo hcitool sr " +
                                    device_address + " MASTER") == 0
                self.logger.debug(f"hcitool {device_address} success: {success}")
            except Exception as exc:
                self.logger.error(f"hcitool {device_address} exception: {exc}")
            await asyncio.sleep(5)

    def is_slave(self, device_address):
        with os.popen('sudo hcitool con') as stream:
            for line in stream.readlines():
                if line.find(device_address) >= 0:
                    if line.find("SLAVE") >= 0:
                        return True
        return False

    def remove_devices(self):
        self.logger.debug("Removing all BT devices")
        while len(self.all) > 0:
            self.remove_device(list(self.all)[0])

    def remove_device(self, device_object_path):
        if device_object_path not in self.all:
            return  # no such device
        device = self.all[device_object_path]
        del self.all[device_object_path]
        list = self.connected_hosts if device.is_host else self.connected_devices
        if device in list:
            list.remove(device)
        device.finalise()
        del device

    def switch_host(self):
        self.current_host_index = (
            self.current_host_index + 1) % len(self.connected_hosts)

    def __get_current_host_as_list(self):
        if len(self.connected_hosts) <= self.current_host_index:
            return []
        return [self.connected_hosts[self.current_host_index]]

    def send_message(self, msg, send_to_hosts, is_control_channel):
        if IGNORE_INPUT_DEVICES and not send_to_hosts and not is_control_channel and self.hid_devices is not None:
            asyncio.run_coroutine_threadsafe(
                self.hid_devices.send_message_to_devices(msg), loop=self.loop)
            return
        targets: List[BluetoothDevice] = self.__get_current_host_as_list(
        ) if send_to_hosts else self.connected_devices
        for target in list(targets):
            try:
                socket = target.control_socket if is_control_channel else target.interrupt_socket
                socket.sendall(msg)
            except Exception:
                self.logger.error("Cannot send data to socket of ",
                      target.object_path, ". Closing")
                if target is not None:
                    try:
                        target.disconnect_sockets()
                    except:
                        self.logger.error("Error while trying to disconnect sockets")
                asyncio.run_coroutine_threadsafe(
                    target.reconcile_connected_state(1), loop=self.loop)
