import json
import asyncio
from time import time
from typing import Dict

from mcproto.buffer import Buffer
from mcproto.connection import TCPAsyncConnection
from mcproto.protocol.base_io import StructFormat


async def fetch_all_motd(servers: Dict[str, str]):
    tasks = {}
    for name, address in servers.items():
        address_info = address.split(':')
        if len(address_info) == 1:
            tasks[name] = asyncio.create_task(fetch_server_motd(address_info[0]))
            continue
        host, port = address_info
        tasks[name] = asyncio.create_task(fetch_server_motd(host, int(port)))
    return {name: await task for name, task in tasks.items()}


async def fetch_server_motd(host: str, port: int = 25565):
    try:
        start_time = round(time() * 1000)
        connection_context = await TCPAsyncConnection.make_client((host, port), 5)
        async with connection_context as connection:
            handshake = Buffer()
            handshake.write_varint(100)
            handshake.write_utf(host)
            handshake.write_value(StructFormat.USHORT, port)
            handshake.write_varint(1)
            packet = Buffer()
            packet.write_varint(0)
            packet.write(handshake)
            await connection.write_varint(len(packet))
            await connection.write(packet)
            packet = Buffer()
            packet.write_varint(0)
            await connection.write_varint(len(packet))
            await connection.write(packet)
            response_length = await connection.read_varint()
            response = Buffer(await connection.read(response_length))
            response.read_varint()
            now_time = round(time() * 1000)
            motd_data = json.loads(response.read_utf())
            motd_data.pop('favicon')
            motd_data.pop('description')
            motd_data.setdefault('ping', now_time - start_time)
            return motd_data
    except (ConnectionError, TimeoutError):
        return None


if __name__ == '__main__':
    # print(asyncio.run(fetch_server_motd('lemonfate.cn')))
    print(asyncio.run(fetch_server_motd('cn-qz-plc-1.ofalias.net', 56839)))
