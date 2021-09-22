# flake8: noqa
import pytest
import asyncio
from api_test_utils.apigee_api_products import ApigeeApiProducts
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps
from api_test_utils.oauth_helper import OauthHelper
from api_test_utils.apigee_api_trace import ApigeeApiTraceDebug
from .configuration import config
from .configuration.config import ENVIRONMENT


@pytest.fixture(scope="session")
async def default_oauth_helper():
    """This fixture is automatically called once when used inside a class.
    The default app created here should not be modified by your tests.
    The default app has a default product associated.
    If your test requires specific app config then please create your own"""

    if ENVIRONMENT == "int" or ENVIRONMENT == "sandbox":
        oauth = OauthHelper(config.CLIENT_ID, config.CLIENT_SECRET, config.REDIRECT_URL)
        yield oauth

    is_internal_env = ENVIRONMENT == "internal-dev" or ENVIRONMENT == "internal-dev-sandbox" or \
                      ENVIRONMENT == "internal-qa" or ENVIRONMENT == "internal-qa-sandbox"
    if is_internal_env:
        print("\nCreating Default App and Product..")
        apigee_product = ApigeeApiProducts()
        await apigee_product.create_new_product()
        await apigee_product.update_proxies(
            [config.PROXY_NAME, f"identity-service-{config.ENVIRONMENT}"]
        )
        await apigee_product.update_scopes(
            ["urn:nhsd:apim:app:level3:booking-and-referral"]
        )
        await apigee_product.update_environments([config.ENVIRONMENT])

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

        oauth = OauthHelper(
            client_id=apigee_app.client_id,
            client_secret=apigee_app.client_secret,
            redirect_uri=apigee_app.callback_url,
        )

        yield oauth

        # Teardown
        print("\nDestroying Default App and Product..")
        await apigee_app.destroy_app()
        await apigee_product.destroy_product()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def debug():
    """
    Import the test utils module to be able to:
        - Use the trace tool and get context variables after making a request to Apigee
    """
    return ApigeeApiTraceDebug(proxy=config.PROXY_NAME)


@pytest.fixture()
async def get_token_client_credentials(default_oauth_helper):
    """Call identity server to get an access token"""
    if "sandbox" in ENVIRONMENT:
        # Sandbox environments doesn't need access_token. Fake one
        return {"access_token": "not_needed"}

    jwt = default_oauth_helper.create_jwt(kid="test-1")
    token_resp = await default_oauth_helper.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]
