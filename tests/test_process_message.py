import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example
import base64
import json


class TestProcessMessage:
    nhsd_token = "nhsd-token"

    @pytest.mark.process_message
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_create_process_message(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("process_message/POST-success.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/$process-message",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.process_message
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_process_message_method_not_allowed(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/$process-message",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
