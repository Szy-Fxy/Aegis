"""Aegis Toolchain 配置模型"""

from pydantic import BaseModel, Field


class AegisConfig(BaseModel):
    """aegis-toolchain 自身配置"""
    project_name: str = ""
    rules_path: str = Field(default="Aegis/rules")
    specs_path: str = Field(default="Aegis_Specs")
    devlogs_path: str = Field(default="Aegis/rules/DevLogs")
    state_path: str = Field(default="Aegis/state/state.json")
