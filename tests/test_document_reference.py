import json
import base64
import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestDocumentReference:
    target_id = "NHS0001"

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_document_reference(self, get_token_client_credentials):
        """
           Test for the /DocumentReference endpoint. This operation will call the Consumer NRL API.
        """
        subject_identifier = "https://fhir.nhs.uk/Id/nhs-number|4409815415"
        end_user_ods = "Y05868"
        target_identifier = json.dumps({"value": self.target_id, "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("document_reference/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference",
            params={"subject:identifier": subject_identifier},
            headers={
                "Accept": "application/fhir+json;version=1",
                "Authorization": f"Bearer {token}",
                "NHSD-End-User-Organisation-ODS": end_user_ods,
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
                "X-Correlation-Id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
