# flake8: noqa
import pytest
import asyncio
import json
from api_test_utils.apigee_api_products import ApigeeApiProducts
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps
from api_test_utils.oauth_helper import OauthHelper
from api_test_utils.apigee_api_trace import ApigeeApiTraceDebug
from .configuration.cmd_options import options, create_cmd_options

def pytest_addoption(parser):
    for option in options:
        parser.addoption(
            option["name"],
            required=option.get("required", False),
            action=option.get("action", "store"),
            help=option.get("help", ""),
            default=option.get("default")
        )


@pytest.fixture(scope='session', autouse=True)
def cmd_options(request) -> dict:
    return create_cmd_options(request.config.getoption)

@pytest.fixture(scope="session")
async def default_oauth_helper(cmd_options: dict):
    """This fixture is automatically called once when used inside a class.
    The default app created here should not be modified by your tests.
    The default app has a default product associated.
    If your test requires specific app config then please create your own"""

    ENVIRONMENT = cmd_options['--apigee-environment']
    client_id = cmd_options["--default-client-id"]
    client_secret = cmd_options["--default-client-secret"]
    redirect_url=cmd_options["--default-callback-url"]
    proxy_name = cmd_options["--service-name"]  #Todo



    if ENVIRONMENT == "int" or ENVIRONMENT == "sandbox":
        oauth = OauthHelper(client_id, client_secret, redirect_url)
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
            [proxy_name, f"identity-service-{ENVIRONMENT}"]
        )
        await apigee_product.update_scopes(
            ["urn:nhsd:apim:app:level3:booking-and-referral"]
        )
        # Product ratelimit
        product_ratelimit = {
            f"{proxy_name}": {
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

        await apigee_product.update_environments([ENVIRONMENT])

        apigee_app = ApigeeApiDeveloperApps()
        await apigee_app.create_new_app()

        # Set default JWT Testing resource url and app ratelimit
        app_ratelimit = {
            f"{proxy_name}": {
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
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def debug(cmd_options):
    """
    Import the test utils module to be able to:
        - Use the trace tool and get context variables after making a request to Apigee
    """
    return ApigeeApiTraceDebug(proxy=cmd_options["--service-name"])


@pytest.fixture()
async def get_token_client_credentials(default_oauth_helper, cmd_options: dict):
    """Call identity server to get an access token"""
    ENVIRONMENT = cmd_options['--apigee-environment']
    if "sandbox" in ENVIRONMENT:
        # Sandbox environments don't need access_token. Return fake one
        return {"access_token": "not_needed"}

    jwt = default_oauth_helper.create_jwt(kid="test-1")
    token_resp = await default_oauth_helper.get_token_response(
        grant_type="client_credentials", _jwt=jwt
    )
    print(token_resp)
    return token_resp["body"]

@pytest.fixture()
def base_url_path(cmd_options) -> str:
    return f"{cmd_options['--oauth-base-uri']}/{cmd_options['--proxy-base-path']}"