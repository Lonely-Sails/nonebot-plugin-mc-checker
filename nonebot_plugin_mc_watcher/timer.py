import asyncio
from nonebot import get_bots
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot

from . import globals
from .config import Config
from .minecraft import fetch_all_motd


async def timer(config: Config):
    globals.servers_motd = await fetch_all_motd(config.minecraft_servers)
    while True:
        await asyncio.sleep(config.interval)
        logger.debug('正在执行定时任务……')
        await task(config)


async def task(config: Config):
    bot = None
    bots = get_bots()
    for one_bot in bots.values():
        if isinstance(one_bot, Bot):
            bot = one_bot
            break
    if not bot and not config.minecraft_broadcast_server:
        logger.warning('未找到可用机器人，无法进行服务器广播！')
    for server_name, server_motd in await fetch_all_motd(config.minecraft_servers):
        logger.debug(F'服务器 {server_name} 的信息为：{server_motd}')
        memory_motd = globals.servers_motd.get(server_name)
        if server_motd is None and memory_motd:
            logger.info(F'检测到服务器 {server_name} 已下线！')
            if config.minecraft_broadcast_server:
                for group in config.minecraft_broadcast_groups:
                    await bot.send_group_msg(group_id=group, message=F'服务器 [{server_name}] 已下线！')
        elif server_motd and memory_motd is None:
            logger.info(F'检测到服务器 {server_name} 已上线！')
            if config.minecraft_broadcast_server:
                for group in config.minecraft_broadcast_groups:
                    await bot.send_group_msg(group_id=group, message=F'服务器 [{server_name}] 已上线！')
        elif server_motd != memory_motd:
            message = F'服务器 [{server_name}] 信息已更新！'
            logger.info(F'检测到服务器 {server_name} 信息已更新！')
            player_count = memory_motd['players']['online']
            max_player_count = server_motd['players']['max']
            current_player_count = server_motd['players']['online']
            if player_count < current_player_count:
                message = F'服务器 [{server_name}] 有玩家退出！当前共有 {current_player_count}/{max_player_count} 人。'
                logger.info(F'检测到服务器 {server_name} 有新玩家加入！')
            elif player_count > current_player_count:
                message = F'服务器 [{server_name}] 有玩家加入！当前共有 {current_player_count}/{max_player_count} 人。'
                logger.info(F'检测到服务器 {server_name} 有玩家退出！')
            if config.minecraft_broadcast_player:
                for group in config.minecraft_broadcast_groups:
                    await bot.send_group_msg(group_id=group, message=message)
        globals.servers_motd[server_name] = server_motd
