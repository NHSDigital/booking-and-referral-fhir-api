# flake8: noqa
import os

import pytest

from .configuration.config import ENVIRONMENT

# The API name as declared in manifest_template.yml (meta.api.name). pytest-nhsd-apim
# uses it to build the OAuth product scope.
API_NAME = "booking-and-referral"


def pytest_configure(config):
    """Bridge the Azure pipeline's environment variables to the config keys that
    pytest-nhsd-apim expects.

    The plugin reads ``--apigee-access-token`` / ``--proxy-name`` / ``--api-name``
    from CLI options, falling back to the matching UPPER_SNAKE env var. Our pipeline
    already exports these values, but under different names, so map them here before
    any plugin fixture runs. ``--proxy-name`` / ``--api-name`` default to ``""``
    (falsy but not ``None``), which stops the plugin from consulting the environment,
    so we populate the parsed options directly.
    """
    if not os.environ.get("APIGEE_ACCESS_TOKEN") and os.environ.get("APIGEE_API_TOKEN"):
        os.environ["APIGEE_ACCESS_TOKEN"] = os.environ["APIGEE_API_TOKEN"]

    if not getattr(config.option, "PROXY_NAME", ""):
        config.option.PROXY_NAME = os.environ.get("FULLY_QUALIFIED_SERVICE_NAME", "")
    if not getattr(config.option, "API_NAME", ""):
        config.option.API_NAME = os.environ.get("API_NAME") or API_NAME


@pytest.fixture()
def get_token_client_credentials(request):
    """Application-restricted access token (signed-JWT client-credentials flow).

    Returns the token payload as a dict (e.g. ``{"access_token": ...}``), matching
    the shape the test suite already consumes. Sandbox environments don't require a
    real token, so a placeholder is returned without contacting Apigee.
    """
    if "sandbox" in ENVIRONMENT:
        return {"access_token": "not_needed"}

    from pytest_nhsd_apim.auth_journey import get_access_token_via_signed_jwt_flow

    credentials = request.getfixturevalue("_test_app_credentials")
    # identity_service_base_url is derived from the environment inside
    # ClientCredentialsConfig, so the argument here is ignored - pass None to avoid
    # resolving the (marker-dependent) identity-service fixture chain.
    return get_access_token_via_signed_jwt_flow(
        None,
        credentials["consumerKey"],
        request.getfixturevalue("jwt_private_key_pem"),
        request.getfixturevalue("jwt_public_key_id"),
        request.getfixturevalue("apigee_environment"),
    )


@pytest.fixture()
def get_token_client_credentials_wrong_app():
    """Token from an app NOT subscribed to the BaRS product (used to assert 403).

    pytest-nhsd-apim's high-level fixtures always subscribe the test app to the
    proxy-under-test's product, so reproducing a "wrong app" token needs a bespoke
    app/product setup. Deferred to the test_endpoints.py migration.
    """
    pytest.skip("Pending pytest-nhsd-apim port: needs an app subscribed to a non-BaRS product.")


@pytest.fixture()
def debug():
    """Apigee trace helper (formerly api_test_utils.ApigeeApiTraceDebug).

    pytest-nhsd-apim 3.0.1 does not expose an Apigee trace/debug API, so the
    trace-based routing assertion in test_endpoints.py is deferred to that file's
    migration.
    """
    pytest.skip("Pending pytest-nhsd-apim port: Apigee trace debugging is not provided by pytest-nhsd-apim 3.0.1.")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    test_fn = item.obj
    docstring = getattr(test_fn, "__doc__")
    if docstring:
        report.nodeid = docstring
