from .registry import PluginRegistry
from .quotes import QuotesToScrapePlugin


def build_registry() -> PluginRegistry:
    reg = PluginRegistry.empty()
    reg.register(QuotesToScrapePlugin)
    return reg
