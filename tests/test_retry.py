from scraper.core.retry import RetryPolicy


def test_retry_policy_has_defaults():
    rp = RetryPolicy()
    assert rp.max_retries >= 1
    assert rp.base_delay_seconds > 0


def test_retry_policy_backoff_grows_and_caps():
    rp = RetryPolicy(base_delay_seconds=0.5, max_delay_seconds=1.0, jitter_factor=0.0)

    assert rp.backoff_delay(1) == 0.5
    assert rp.backoff_delay(2) == 1.0
    assert rp.backoff_delay(3) == 1.0
