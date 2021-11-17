import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example
from datetime import datetime


class TestSlots:
    currentTime = datetime.now()
    nhsd_token = "nhsd-token"

    @pytest.mark.slots
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_slots_happy_path(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("slots/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Token": self.nhsd_token,
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
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
                    "end": currentTime,
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 2: missing status query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "start ": currentTime,
                    "end": currentTime,
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 3: invalid status query
            (
                {
                    "status": ["invalid"],
                    "start ": currentTime,
                    "end": currentTime,
                    "_include": ["Schedule"],
                }
            ),
            # Scenario 4: missing start query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free"],
                    "end": currentTime,
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
                    "end": currentTime,
                }
            ),
            # Scenario 7: invalid _include query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free", "busy"],
                    "start ": currentTime,
                    "end": currentTime,
                    "_include": ["invalid"],
                }
            ),
        ],
    )
    def test_get_slots_bad_request(self, get_token_client_credentials, data):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("slots/GET-BadRequest.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Token": self.nhsd_token,
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
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        # expected_body = load_example("slots/GET-success.json")

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Token": self.nhsd_token,
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        # assert_that(expected_body).is_equal_to(response.json())