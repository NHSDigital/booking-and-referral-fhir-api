import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example


class TestServiceRequest:
    @pytest.mark.slots
    @pytest.mark.integration
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
                "NHSD-ServiceIdentifier": "NHS0001",
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free", "busy"],
                "start ": "2020-03-31T14:00:00",
                "end": "2020-03-31T16:00:00",
                "_include": ["Schedule", "Schedule:actor:Practitioner", "Schedule:actor:PractitionerRole", "Schedule:actor:HealthcareService", "HealthcareService.providedBy", "HealthcareService.location"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.slots
    @pytest.mark.integration
    @pytest.mark.parametrize(
        "data",
        [
            # Scenario 1: missing healthcareService query
            (
                {
                    "status": ["free", "busy"],
                    "start ": "2020-03-31T14:00:00",
                    "end": "2020-03-31T16:00:00",
                    "_include": ["Schedule", "Schedule:actor:Practitioner", "Schedule:actor:PractitionerRole", "Schedule:actor:HealthcareService", "HealthcareService.providedBy", "HealthcareService.location"],
                }
            ),
            # Scenario 2: missing status query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "start ": "2020-03-31T14:00:00",
                    "end": "2020-03-31T16:00:00",
                    "_include": ["Schedule", "Schedule:actor:Practitioner", "Schedule:actor:PractitionerRole", "Schedule:actor:HealthcareService", "HealthcareService.providedBy", "HealthcareService.location"],
                }
            ),
            # Scenario 3: invalid status query
            (
                {
                    "status": "",
                    "start ": "2020-03-31T14:00:00",
                    "end": "2020-03-31T16:00:00",
                    "_include": ["Schedule", "Schedule:actor:Practitioner", "Schedule:actor:PractitionerRole", "Schedule:actor:HealthcareService", "HealthcareService.providedBy", "HealthcareService.location"],
                }
            ),
            # Scenario 4: missing start query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free", "busy"],
                    "end": "2020-03-31T16:00:00",
                    "_include": ["Schedule", "Schedule:actor:Practitioner", "Schedule:actor:PractitionerRole", "Schedule:actor:HealthcareService", "HealthcareService.providedBy", "HealthcareService.location"],
                }
            ),
            # Scenario 5: missing end query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free", "busy"],
                    "start ": "2020-03-31T14:00:00",
                    "_include": ["Schedule", "Schedule:actor:Practitioner", "Schedule:actor:PractitionerRole", "Schedule:actor:HealthcareService", "HealthcareService.providedBy", "HealthcareService.location"],
                }
            ),
            # Scenario 6: missing _include query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free", "busy"],
                    "start ": "2020-03-31T14:00:00",
                    "end": "2020-03-31T16:00:00",
                }
            ),
            # Scenario 7: invalid _include query
            (
                {
                    "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                    "status": ["free", "busy"],
                    "start ": "2020-03-31T14:00:00",
                    "end": "2020-03-31T16:00:00",
                    "_include": "",
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
                "NHSD-ServiceIdentifier": "NHS0001",
            },
            params=data,
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
