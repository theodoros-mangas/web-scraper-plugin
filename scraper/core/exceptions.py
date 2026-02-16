class ScraperError(Exception):
    """Base class for all scraper exceptions."""
    pass

class PluginNotFound(ScraperError):
    """Raised when a specified plugin is not found."""
    pass

class FetchError(ScraperError):
    """Raised when there is an error fetching data from a source."""
    pass