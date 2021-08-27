# flake8: noqa
import pytest
import asyncio
from uuid import uuid4
from time import time
from api_test_utils.api_test_session_config import APITestSessionConfig
from api_test_utils.apigee_api_products import ApigeeApiProducts
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps
from api_test_utils.oauth_helper import OauthHelper
from .configuration import config

@pytest.fixture(scope='session')
def api_test_config() -> APITestSessionConfig:
    """
        this imports a 'standard' test session config,
        which builds the proxy uri
    """
    return APITestSessionConfig()

@pytest.fixture(scope="class")
async def default_app():
    """This fixture is automatically called once when used inside a class.
    The default app created here should not be modified by your tests.
    The default app has a default product associated.
    If your test requires specific app config then please create your own"""

    print("\nCreating Default App and Product..")
    apigee_product = ApigeeApiProducts()
    await apigee_product.create_new_product()
    await apigee_product.update_proxies(
        [config.BASE_PATH, "identity-service-internal-dev"]
    )
    await apigee_product.update_scopes(
        ["urn:nhsd:apim:app:level3:booking-and-referral"]
    )

    apigee_app = ApigeeApiDeveloperApps()
    await apigee_app.create_new_app()

    # Set default JWT Testing resource url
    await apigee_app.set_custom_attributes(
        {
            "jwks-resource-url": "https://raw.githubusercontent.com/NHSDigital/"
            "identity-service-jwks/main/jwks/internal-dev/"
            "9baed6f4-1361-4a8e-8531-1f8426e3aba8.json"
        }
    )

    await apigee_app.add_api_product(api_products=[apigee_product.name])

    [
        await product.update_ratelimits(
            quota=60000,
            quota_interval="1",
            quota_time_unit="minute",
            rate_limit="1000ps",
        )
        for product in [apigee_product]
    ]

    yield apigee_app

    # Teardown
    print("\nDestroying Default App and Product..")
    await apigee_app.destroy_app()
    await apigee_product.destroy_product()


@pytest.yield_fixture(scope="class")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def get_token_client_credentials(default_app):
    """Call identity server to get an access token"""
    test_app = default_app
    oauth = OauthHelper(
        client_id=test_app.client_id,
        client_secret=test_app.client_secret,
        redirect_uri=test_app.callback_url,
    )
    jwt = oauth.create_jwt(kid="test-1")
    token_resp = await oauth.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]
