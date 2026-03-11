import pytest

from scraper.core.exceptions import PluginNotFound
from scraper.plugins import build_registry
from scraper.plugins.base import ScraperPlugin
from scraper.plugins.registry import PluginRegistry


def test_registry_lists_plugins():
    reg = build_registry()
    assert "quotes" in reg.list_names()


class DuplicatePlugin(ScraperPlugin):
    name = "duplicate"

    def start_urls(self) -> list[str]:
        return []

    def parse(self, ctx, html: str):
        return []


def test_registry_rejects_duplicate_names():
    reg = PluginRegistry.empty()
    reg.register(DuplicatePlugin)

    with pytest.raises(ValueError, match="already registered"):
        reg.register(DuplicatePlugin)


def test_registry_create_raises_for_unknown_plugin():
    reg = build_registry()

    with pytest.raises(PluginNotFound, match="Plugin 'missing' not found"):
        reg.create("missing")
