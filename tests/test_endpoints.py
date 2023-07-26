import base64
import json

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestEndpoints:
    target_id = json.dumps({"value": "NHS0001", "system": config.TARGET_SYSTEM})
    target_id_encoded = base64.b64encode(bytes(target_id, "utf-8"))

    @pytest.mark.auth
    @pytest.mark.debug
    def test_invalid_access_token(self):
        """
          test for /metadata..  to check it with an invalid access token
          must return 401 forbiddden
        """
        expected_status_code = 401
        expected_body = load_example("OperationOutcome/SEND/401-SEND_UNAUTHORIZED-security.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": "Bearer invalid_token",
                "NHSD-Target-Identifier": self.target_id_encoded,
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.auth
    def test_missing_access_token(self):
        """
          test for /metadata..  to check it making a request without an access token
          must return 401 unauthorized
        """
        expected_status_code = 401
        expected_body = load_example("OperationOutcome/SEND/401-SEND_UNAUTHORIZED-unknown.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": "",
                "NHSD-Target-Identifier": self.target_id_encoded,
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.auth
    @pytest.mark.skipif(config.ENVIRONMENT in ["int", "sandbox"], reason="We don't create an apigee product/app per test in this environment.")
    def test_invalid_product_access_token(self, get_token_client_credentials_wrong_app):
        """
          Test that a request made with a valid access token returns a 403 forbidden response when BaRS is not available
        """
        token = get_token_client_credentials_wrong_app["access_token"]

        expected_status_code = 403
        expected_body = load_example("OperationOutcome/SEND/403-SEND_FORBIDDEN-forbidden.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_endpoint_not_found(self, get_token_client_credentials):
        """
          test for /invalid..  to check it making a request to an unexisting endpoint
          must return 500 server error.
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404
        expected_body = load_example("OperationOutcome/PROXY-NONE/404-NOT_FOUND-not-found.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/invalid",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.asyncio
    @pytest.mark.broker
    @pytest.mark.parametrize(
        "path_suffix",
        ("Appointment", "Appointment/some-id", "Appointment/some-id?param=value"),
    )
    async def test_proxy_routing(
        self, get_token_client_credentials, debug, path_suffix
    ):
        # Given
        token = get_token_client_credentials["access_token"]
        if "pr" in config.TARGET_SYSTEM:
            expected_target = f"https://internal-dev-pr.bars.dev.api.platform.nhs.uk/{path_suffix}"
        else:
            expected_target = f"https://internal-dev.bars.dev.api.platform.nhs.uk/{path_suffix}"

        await debug.start_trace()

        # When
        requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{path_suffix}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
        )

        target = await debug.get_apigee_variable_from_trace(name="target.url")

        # Then
        assert_that(target).is_equal_to(expected_target)

    def test_missing_headers_returns_bad_request(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("OperationOutcome/PROXY-NONE/400-BAD_REQUEST-invalid.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
