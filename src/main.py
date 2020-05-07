#!/usr/bin/env python

import logging
import asyncio

from asyncua import ua, Server

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-20s  - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class MirrorHandler(object):

    def __init__(self, server, orig_data, copy_data):
        self.server = server
        self.orig_data = orig_data
        self.copy_data = copy_data
        self.sub = None

    async def start(self):
        self.sub = await self.server.create_subscription(100, self)
        await self.orig_data.set_writable()
        await self.sub.subscribe_data_change(self.orig_data)

    def datachange_notification(self, node, val, data):
        if self.orig_data == node:
            self.server.set_attribute_value(self.copy_data.nodeid, ua.DataValue(val))


async def toggle_data(data, refresh=1, init=False):
    value = init
    while True:
        await data.write_value(value)
        await asyncio.sleep(refresh)
        value = not value


async def periodic_data(data, refresh=1, init=0, increment=1):
    value = init
    while True:
        await data.write_value(value)
        await asyncio.sleep(refresh)
        value += increment


async def random_data(data, refresh=1, init=0, min=0, max=10):
    import random
    value = init
    while True:
        await data.write_value(value)
        await asyncio.sleep(refresh)
        value = round(random.uniform(min, max), 2)


async def cyclic_data(data, cycle_time=1, step=0.1, init=0, min=0, max=100):
    value = init
    interval = max - min
    spi = interval / step # steps per interval
    refresh = cycle_time / spi
    increasing = True
    while True:
        await data.write_value(value)
        await asyncio.sleep(refresh)
        if value >= max:
            increasing = False
        if value <= min:
            increasing = True
        value = value + step if increasing else value - step


async def main():
    server = Server()
    await server.init()
    await server.set_application_uri("urn:opcua:iom:server")
    server.set_endpoint('opc.tcp://0.0.0.0:4840/freeopcua/server/')
    server.set_server_name("IoM PLC Server Example")

    # Security
    await server.load_certificate("certificate.der")
    await server.load_private_key("key.pem")
    server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])

    # setup our own namespace, not really necessary but should as spec
    idx = await server.register_namespace("https://tknika.eus/opcua/demo/plc")
    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()
    # populating our address space
    plc_server = await objects.add_object(idx, 'PLC Server')
    bool_data = await plc_server.add_variable(idx, 'BooleanData', True)
    pos_data = await plc_server.add_variable(idx, 'PositiveTrendData', 0.0)
    neg_data = await plc_server.add_variable(idx, 'NegativeTrendData', 0.0)
    temp_data = await plc_server.add_variable(idx, 'TemperatureData', 18.5)
    cyc_data = await plc_server.add_variable(idx, 'CyclicData', 0)
    mirror_orig_data = await plc_server.add_variable(idx, 'MirrorDataOriginal', True)
    mirror_copy_data = await plc_server.add_variable(idx, 'MirrorDataCopy', True)

    logger.info('Starting OPC UA server!')

    bool_task = asyncio.Task(toggle_data(bool_data, refresh=2, init=True))
    pos_task = asyncio.Task(periodic_data(pos_data, refresh=0.2))
    neg_task = asyncio.Task(periodic_data(neg_data, increment=-2))
    temp_task = asyncio.Task(random_data(temp_data, refresh=1, init=18.5, min=15, max=22))
    cyclic_task = asyncio.Task(cyclic_data(cyc_data, cycle_time=10, step=0.2, init=0, min=-100, max=100))
    
    mirrorHandler = MirrorHandler(server, mirror_orig_data, mirror_copy_data)
    await mirrorHandler.start()

    async with server:
        await asyncio.gather(bool_task, pos_task, neg_task, temp_task, cyclic_task)


if __name__ == '__main__':
    logger.info('Starting application')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()