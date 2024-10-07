from typing import Dict, List
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    minecraft_servers: Dict[str, str]
    minecraft_update_interval: int = 30
    minecraft_broadcast_server: bool = True
    minecraft_broadcast_player: bool = False
    minecraft_broadcast_groups: List[int] = []

    @field_validator('minecraft_servers')
    @classmethod
    def check_servers(cls, value: Dict[str, str]):
        if not value:
            raise ValueError('MINECRAFT_SERVERS cannot be empty!')
        for name, address in value.items():
            host, port = address.split(':')
            if not host or not port.isdigit():
                raise ValueError(f'Invalid server address MINECRAFT_SERVERS: {name}={address}.')
        return value
