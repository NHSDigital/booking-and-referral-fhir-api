import requests
from assertpy import assert_that
from .configuration import config


class TestEndpoints:

    # This tests are only asserting status codes since we still do not have 'mock-recievers' in place
    # Lets dont forget to add assertions fot the response body whenever is possible :)

    def test_happy_path(self, get_token_client_credentials):
        # This test should be parametrized using all the valid endpoints whenever the finish the OAS spec.
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slots",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    def test_invalid_nhsd_service_identifier(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slots",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "invalid",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    def test_invalid_path(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/invalid",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
