# flake8: noqa
import pytest
import asyncio
import json
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

    is_internal_env = (
        ENVIRONMENT == "internal-dev"
        or ENVIRONMENT == "internal-dev-sandbox"
        or ENVIRONMENT == "internal-qa"
        or ENVIRONMENT == "internal-qa-sandbox"
    )
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
        # Product ratelimit
        product_ratelimit = {
            f"{config.PROXY_NAME}": {
                "quota": {
                    "limit": "300",
                    "enabled": True,
                    "interval": 1,
                    "timeunit": "minute",
                },
                "spikeArrest": {"ratelimit": "100ps", "enabled": True},
            }
        }
        await apigee_product.update_attributes({"ratelimiting": json.dumps(product_ratelimit)})

        await apigee_product.update_environments([config.ENVIRONMENT])

        apigee_app = ApigeeApiDeveloperApps()
        await apigee_app.create_new_app()

        # Set default JWT Testing resource url and app ratelimit
        app_ratelimit = {
            f"{config.PROXY_NAME}": {
                "quota": {
                    "limit": "300",
                    "enabled": True,
                    "interval": 1,
                    "timeunit": "minute",
                },
                "spikeArrest": {"ratelimit": "100ps", "enabled": True},
            }
        }
        await apigee_app.set_custom_attributes(
            {
                "jwks-resource-url": "https://raw.githubusercontent.com/NHSDigital/"
                "identity-service-jwks/main/jwks/internal-dev/"
                "9baed6f4-1361-4a8e-8531-1f8426e3aba8.json",
                "ratelimiting": json.dumps(app_ratelimit),
            }
        )

        await apigee_app.add_api_product(api_products=[apigee_product.name])

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
async def oauth_helper_document_reference():
    if ENVIRONMENT == "int" or ENVIRONMENT == "sandbox":
        oauth = OauthHelper(config.CLIENT_ID, config.CLIENT_SECRET, config.REDIRECT_URL)
        yield oauth

    is_internal_env = (
        ENVIRONMENT == "internal-dev"
        or ENVIRONMENT == "internal-dev-sandbox"
        or ENVIRONMENT == "internal-qa"
        or ENVIRONMENT == "internal-qa-sandbox"
    )
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
        # Product ratelimit
        product_ratelimit = {
            f"{config.PROXY_NAME}": {
                "quota": {
                    "limit": "300",
                    "enabled": True,
                    "interval": 1,
                    "timeunit": "minute",
                },
                "spikeArrest": {"ratelimit": "100ps", "enabled": True},
            }
        }
        await apigee_product.update_attributes({"ratelimiting": json.dumps(product_ratelimit)})

        await apigee_product.update_environments([config.ENVIRONMENT])

        apigee_app = ApigeeApiDeveloperApps()
        await apigee_app.create_new_app()

        # Set default JWT Testing resource url and app ratelimit
        app_ratelimit = {
            f"{config.PROXY_NAME}": {
                "quota": {
                    "limit": "300",
                    "enabled": True,
                    "interval": 1,
                    "timeunit": "minute",
                },
                "spikeArrest": {"ratelimit": "100ps", "enabled": True},
            }
        }
        await apigee_app.set_custom_attributes(
            {
                "jwks-resource-url": "https://raw.githubusercontent.com/NHSDigital/"
                "identity-service-jwks/main/jwks/internal-dev/"
                "9baed6f4-1361-4a8e-8531-1f8426e3aba8.json",
                "ratelimiting": json.dumps(app_ratelimit),
                "product-id": "P.GH7-4TY"
            }
        )

        await apigee_app.add_api_product(api_products=[apigee_product.name])

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
async def oauth_helper_wrong_app():
    is_internal_env = (
        ENVIRONMENT == "internal-dev"
        or ENVIRONMENT == "internal-dev-sandbox"
        or ENVIRONMENT == "internal-qa"
        or ENVIRONMENT == "internal-qa-sandbox"
    )
    if is_internal_env:
        print("\nCreating Default App and Product..")
        apigee_product = ApigeeApiProducts()
        await apigee_product.create_new_product()
        await apigee_product.update_proxies(
            [f"personal-demographics-{config.ENVIRONMENT}", f"identity-service-{config.ENVIRONMENT}"]
        )
        await apigee_product.update_scopes(
            ["urn:nhsd:apim:app:level3:personal-demographics-service"]
        )
        await apigee_product.update_environments([config.ENVIRONMENT])

        apigee_app = ApigeeApiDeveloperApps()
        await apigee_app.create_new_app()

        await apigee_app.set_custom_attributes(
            {
                "jwks-resource-url": "https://raw.githubusercontent.com/NHSDigital/"
                "identity-service-jwks/main/jwks/internal-dev/"
                "9baed6f4-1361-4a8e-8531-1f8426e3aba8.json",
            }
        )
        await apigee_app.add_api_product(api_products=[apigee_product.name])

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
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    jwt = default_oauth_helper.create_jwt(kid="test-1")
    token_resp = await default_oauth_helper.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]

@pytest.fixture()
async def get_token_client_credentials_wrong_app(oauth_helper_wrong_app):
    """Call identity server to get an access token"""
    if "sandbox" in ENVIRONMENT:
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    jwt = oauth_helper_wrong_app.create_jwt(kid="test-1")
    token_resp = await oauth_helper_wrong_app.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]

@pytest.fixture()
async def get_token_client_credentials_document_reference(oauth_helper_document_reference):
    """Call identity server to get an access token"""
    if "sandbox" in ENVIRONMENT:
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    jwt = oauth_helper_document_reference.create_jwt(kid="test-1")
    token_resp = await oauth_helper_document_reference.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    return token_resp["body"]

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    test_fn = item.obj
    docstring = getattr(test_fn, '__doc__')
    if docstring:
        report.nodeid = docstring
