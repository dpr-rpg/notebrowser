"""Configuration class."""

from dataclasses import asdict, dataclass
from pathlib import Path

import dacite
import yaml


@dataclass(frozen=True)
class Configuration:
    """Configuration class."""

    title: str = "Title"
    author: str = "Author"
    stylesheet: str = "style.css"

    def to_file(self, config_file: Path):
        """Write configuration to file."""
        with open(config_file, "w") as f:
            yaml.dump(asdict(self), f)


def load_configuration(config_file: Path) -> Configuration:
    """Read configuration file."""
    with open(config_file) as f:
        data = yaml.safe_load(f)
    return dacite.from_dict(data=data, data_class=Configuration)
