import os
import time

import pytest
import requests

from .configuration import config

# Proxy base URL and the commit id we expect to be deployed. The pipeline exports
# SOURCE_COMMIT_ID; the _ping / _status endpoints echo it back as "commitId".
BASE_URI = f"{config.BASE_URL}/{config.BASE_PATH}"
COMMIT_ID = os.environ.get("SOURCE_COMMIT_ID")


def _poll_until(make_request, until, timeout=120, interval=5):
    """Call make_request() until until(response) is truthy or the timeout elapses."""
    deadline = time.monotonic() + timeout
    response = make_request()
    while not until(response):
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Condition not met within {timeout}s; last status {response.status_code}"
            )
        time.sleep(interval)
        response = make_request()
    return response


def _is_deployed(response):
    if response.status_code != 200:
        return False
    return response.json().get("commitId") == COMMIT_ID


def _is_401(response):
    return response.status_code == 401


@pytest.mark.smoketest
def test_output_test_config():
    print(f"base_uri={BASE_URI} commit_id={COMMIT_ID}")


@pytest.mark.smoketest
@pytest.mark.ping
def test_wait_for_ping():
    """
        test for _ping .. polls until the correct SOURCE_COMMIT_ID (from env var) is deployed
    """
    _poll_until(lambda: requests.get(f"{BASE_URI}/_ping"), until=_is_deployed)


@pytest.mark.smoketest
@pytest.mark.sandbox
@pytest.mark.status
def test_check_status_is_secured():
    _poll_until(lambda: requests.get(f"{BASE_URI}/_status"), until=_is_401)


@pytest.mark.smoketest
@pytest.mark.sandbox
@pytest.mark.status
def test_wait_for_status():
    """
        test for _status .. polls until the correct SOURCE_COMMIT_ID (from env var) is deployed
    """
    api_key = os.environ["STATUS_ENDPOINT_API_KEY"]
    _poll_until(
        lambda: requests.get(f"{BASE_URI}/_status", headers={"apikey": api_key}),
        until=_is_deployed,
    )
