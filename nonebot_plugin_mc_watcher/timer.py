import asyncio
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot

from . import globals
from .config import Config
from .minecraft import fetch_all_motd


async def timer(bot: Bot, config: Config):
    globals.servers_motd = await fetch_all_motd(config.minecraft_servers)
    while True:
        logger.debug('正在定时抓取所有服务器信息……')
        for server_name, server_motd in await fetch_all_motd(config.minecraft_servers):
            logger.debug(F'服务器 {server_name} 的信息为：{server_motd}')

        await asyncio.sleep(config.interval)
