from typing import Dict, List
from socket import gethostbyname
from pydantic import BaseModel, field_validator


def verify_address_name(address: str):
    try: gethostbyname(address)
    except OSError: return False
    return True


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
            if ':' in address:
                host, port = address.split(':')
                if not host or not port.isdigit():
                    raise ValueError(f'Invalid port in MINECRAFT_SERVERS: {name}={address}.')
                if not verify_address_name(host):
                    raise ValueError(f'Invalid server address MINECRAFT_SERVERS: {name}={address}.')
            elif not verify_address_name(address):
                raise ValueError(f'Invalid server address MINECRAFT_SERVERS: {name}={address}.')
        return value
