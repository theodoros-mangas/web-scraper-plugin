from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from scraper.core.exceptions import PluginNotFound
from scraper.plugins.base import ScraperPlugin


@dataclass
class PluginRegistry:
    _plugins: dict[str, Type[ScraperPlugin]]

    @classmethod
    def empty(cls) -> "PluginRegistry":
        return cls(_plugins={})

    def register(self, plugin_cls: Type[ScraperPlugin]) -> None:
        name = getattr(plugin_cls, "name", None)
        if not name or not isinstance(name, str):
            raise ValueError("Plugin class must define a string 'name' attribute.")
        self._plugins[name] = plugin_cls

    def create(self, name: str) -> ScraperPlugin:
        if name not in self._plugins:
            raise PluginNotFound(f"Plugin '{name}' not found. Available: {sorted(self._plugins.keys())}")
        return self._plugins[name]()

    def list_names(self) -> list[str]:
        return sorted(self._plugins.keys())
