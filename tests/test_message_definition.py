import base64
import json

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestMessageDefinition:
    target_id = config.TARGET_ID

    @pytest.mark.message_definition
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_message_definition(self, get_token_client_credentials):
        """
           test to get message definition for the target identifier
        """

        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("message_definition/MessageDefinition_ServiceRequest-request_CaseTransfer.json")
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/MessageDefinition",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={"context": "2000099999"}
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.message_definition
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_message_definition_method_not_allowed(self, get_token_client_credentials):
        """
          test to posting message definition for the target identifier
          must return method not allowed
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/MessageDefinition",
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
