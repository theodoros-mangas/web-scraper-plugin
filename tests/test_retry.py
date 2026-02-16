from scraper.core.retry import RetryPolicy

def test_retry_policy_has_defaults():
    rp = RetryPolicy()
    assert rp.max_retries >= 1
    assert rp.base_delay_seconds > 0
