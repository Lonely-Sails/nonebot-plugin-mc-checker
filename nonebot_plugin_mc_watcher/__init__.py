import asyncio
from nonebot import on_command, get_driver
from nonebot.plugin import PluginMetadata, get_plugin_config
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot

from .config import Config
from .timer import timer
from .minecraft import fetch_all_motd

__plugin_meta__ = PluginMetadata(
    name='MinecraftWatcher',
    description='一个基于 Motd 监视 Minecraft 多个服务器状态的 NoneBot 插件。',
    usage='可以通过命令 /mc 或 /minecraft 进行查询。',
    homepage='https://github.com/Lonely-Sails/nonebot-plugin-mc-watcher',
    type='application',
    config=Config,
    supported_adapters={'~onebot.v11'}
)

task = None
adapter = get_driver()
config = get_plugin_config(Config)
minecraft_matcher = on_command('minecraft', aliases={'mc'})


@adapter.on_startup
async def _():
    global task
    task = asyncio.create_task(timer(config))


@adapter.on_shutdown
async def _():
    task.cancel()


@minecraft_matcher.handle()
async def _(event: GroupMessageEvent):
    message_lines = ['服务器查询结果：']
    servers_motd = await fetch_all_motd(config.servers)
    for server_name, motd in servers_motd.items():
        if motd is not None:
            version = motd['version']['name']
            max_players = motd['players']['max']
            online_players = motd['players']['online']
            message_lines.append(F'  {server_name}：在线')
            message_lines.append(F'  - 在线玩家：{online_players}/{max_players}    版本：{version}')
            continue
        message_lines.append(F'  {server_name}：服务器已离线')
    await minecraft_matcher.send('\n'.join(message_lines), at_sender=True)
