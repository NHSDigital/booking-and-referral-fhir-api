import base64
import json

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestMetadata:
    target_id = json.dumps({"value": "NHS0001", "system": config.TARGET_SYSTEM})
    target_id_encoded = base64.b64encode(bytes(target_id, "utf-8"))

    @pytest.mark.metadata
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_metadata_method_not_allowed(self, get_token_client_credentials):
        """
          test to posting metadata for the target identifier
          must return method not allowed
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.metadata
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_metadata_capability_statement(self, get_token_client_credentials):
        """
          test to get metadata capability statement
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("metadata/BaRS_API_Capability_Statement.json")
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
