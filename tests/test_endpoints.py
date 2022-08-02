import asyncio
import base64
import json

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestEndpoints:
    target_id = "NHS0001"

    @pytest.mark.auth
    def test_invalid_access_token(self):
        """
          test for /metadata..  to check it with an invalid access token
          must return 403 forbiddden
        """
        expected_status_code = 403
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": "Bearer invalid_token",
                "NHSD-Target-Identifier": target_identifier_encoded,
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.auth
    def test_missing_access_token(self):
        """
          test for /metadata..  to check it making a request without an access token
          must return 401 unauthorized
        """
        expected_status_code = 401
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": "",
                "NHSD-Target-Identifier": target_identifier_encoded,
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.auth
    def test_invalid_access_token_auth_code(self, default_oauth_helper):
        """
          This test checks that when trying to authenticate using auth_code flow
          an exemption is raised.
        """

        with pytest.raises(Exception):
            assert asyncio.run(
                default_oauth_helper.get_token_response(grant_type="authorization_code")
            )

    @pytest.mark.broker
    def test_invalid_nhsd_service_identifier(self, get_token_client_credentials):
        """
          This test checks a request with an invalid service identifier returns a 404 error.
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404
        expected_body = load_example("proxy-not-found.json")
        target_identifier = json.dumps({"value": "invalid", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
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
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/invalid",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

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
        expected_target = f"https://dev.bars.dev.api.platform.nhs.uk/{path_suffix}"
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        await debug.start_trace()

        # When
        requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{path_suffix}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
        )

        target = await debug.get_apigee_variable_from_trace(name="target.url")

        # Then
        assert_that(target).is_equal_to(expected_target)
