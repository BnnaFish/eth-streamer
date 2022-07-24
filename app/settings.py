from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

import marshmallow_dataclass
from pyhocon import ConfigFactory

from app.schema import BaseSchema


@dataclass
class NodeConfig:
    """
    Creds to use blockchain parsers
    """

    api_key: str
    url: str


node_config_schema = marshmallow_dataclass.class_schema(NodeConfig, base_schema=BaseSchema)()


def config_factory(folder: str = "settings", section: str = None) -> dict[str, Any]:
    """
    parsing hocon config from the given folder for the given section in file
    """
    package_dir = Path(folder)
    env = os.getenv("ENV", "default")
    conf_path = package_dir / f"{env}.conf"
    fallback_conf_path = package_dir / "default.conf"
    factory = ConfigFactory.parse_file(conf_path)
    factory = factory.with_fallback(fallback_conf_path)
    return factory.get_config(section or "config")


node_config = node_config_schema.load(config_factory(folder="settings", section="node"))
