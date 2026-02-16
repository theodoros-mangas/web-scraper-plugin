from scraper.plugins import build_registry

def test_registry_lists_plugins():
    reg = build_registry()
    assert "quotes" in reg.list_names()
