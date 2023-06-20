import base64
import json

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestProcessMessage:
    target_id = config.TARGET_SYSTEM

    @pytest.mark.target_identifier
    @pytest.mark.broker
    @pytest.mark.sandbox
    def test_invalid_base64_encoded_identifier(self, get_token_client_credentials):
        """
          This test checks a request with an invalid encoded service identifier returns a 400 error.
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("invalid-base64.json")
        target_identifier_encoded = "this-is-not-base-64"

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

    @pytest.mark.target_identifier
    @pytest.mark.broker
    @pytest.mark.sandbox
    def test_invalid_nhsd_service_identifier_value(self, get_token_client_credentials):
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

    @pytest.mark.target_identifier
    @pytest.mark.broker
    @pytest.mark.sandbox
    def test_malformed_nhsd_service_identifier(self, get_token_client_credentials):
        """
          This test checks a request with a malformed service identifier returns a 400 error.
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("malformed-target-identifier.json")
        target_identifier = json.dumps({"system": "tests"})
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
