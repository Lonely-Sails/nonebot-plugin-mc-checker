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
    homepage='https://github.com/LonelySail/nonebot_plugin_mc_watcher',
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


@minecraft_matcher.handle()
async def _(event: GroupMessageEvent, bot: Bot):
    pass
