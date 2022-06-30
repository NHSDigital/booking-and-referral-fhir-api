import base64
import json
from datetime import datetime

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestSlots:
    currentTime = datetime.now()
    nhsd_token = "nhsd-token"
    target_id = "NHS0001"

    @pytest.mark.slots
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_slots_happy_path(self, get_token_client_credentials):
        """
          test for /Slot..  to get slots for the target identifier
          must return a slot entity
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("slots/GET-success.json")
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "Schedule.actor:HealthcareService": "918999198999",
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.slots
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.parametrize(
        "data",
        [
            # Scenario 1: missing healthcareService query
            (
                {
                    "status": ["free"],
                    "start ": currentTime,
                    "Schedule.actor:HealthcareService": "918999198999",
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 2: missing status query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "start ": currentTime,
                    "Schedule.actor:HealthcareService": "918999198999",
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 3: invalid status query
            (
                {
                    "status": ["invalid"],
                    "start ": currentTime,
                    "Schedule.actor:HealthcareService": "918999198999",
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 4: missing start query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free"],
                    "Schedule.actor:HealthcareService": "918999198999",
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 5: missing end query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free"],
                    "start ": currentTime,
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 6: missing _include query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free"],
                    "start ": currentTime,
                    "Schedule.actor:HealthcareService": "918999198999",
                }
            ),
            # Scenario 7: invalid _include query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free", "busy"],
                    "start ": currentTime,
                    "Schedule.actor:HealthcareService": "918999198999",
                    "_include": ["invalid"],
                }
            ),
        ],
    )
    def test_get_slots_bad_request(self, get_token_client_credentials, data):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
            params=data,
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.slots
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_slots_method_not_allowed(self, get_token_client_credentials):
        """
          test for /Slot..  to post slot for the target identifier
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
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "Schedule.actor:HealthcareService": "918999198999",
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
