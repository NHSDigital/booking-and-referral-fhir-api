import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example


class TestMetadata:
    @pytest.mark.metadata
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_metadata(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("metadata/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
