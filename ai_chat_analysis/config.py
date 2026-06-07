from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).parent.parent / "config.yml"


@dataclass
class Config:
    claude_chat_r2_raw_prefix: str
    claude_chat_r2_output_prefix: str
    claude_chat_local_tmp_dir: Path

    claude_code_r2_projects_prefix: str
    claude_code_r2_output_key: str
    claude_code_local_tmp_dir: Path


def load(path: Path = CONFIG_PATH) -> Config:
    raw = yaml.safe_load(path.read_text())
    return Config(
        claude_chat_r2_raw_prefix=raw["claude_chat_r2_raw_prefix"],
        claude_chat_r2_output_prefix=raw["claude_chat_r2_output_prefix"],
        claude_chat_local_tmp_dir=Path(raw["claude_chat_local_tmp_dir"]),
        claude_code_r2_projects_prefix=raw["claude_code_r2_projects_prefix"],
        claude_code_r2_output_key=raw["claude_code_r2_output_key"],
        claude_code_local_tmp_dir=Path(raw["claude_code_local_tmp_dir"]),
    )
