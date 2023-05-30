import pytest
import requests
from assertpy import assert_that
import time
import random
import json
from .configuration import config


class TestDocumentReference:
    end_user_ods = "V4T0L"
    end_user_nhs_number = "4409815415"

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.debug
    def test_get_document_reference(self, get_token_client_credentials):
        """
           Test for the GET /DocumentReference endpoint. This operation will call the Consumer NRL API.
        """
        subject_identifier = "https://fhir.nhs.uk/Id/nhs-number|"+self.end_user_nhs_number
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference",
            params={"subject:identifier": subject_identifier},
            headers={
                "Accept": "application/fhir+json;version=1",
                "Authorization": f"Bearer {token}",
                "NHSD-End-User-Organisation-ODS": self.end_user_ods,
                "X-Request-Id": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
                "X-Correlation-Id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.debug
    def test_get_document_reference_by_id(self, get_token_client_credentials):
        """
           Test for the GET /DocumentReference/{id} endpoint. This operation will call the Producer NRL API.
        """
        document_id = "V4T0L-"
        timestamp = int(time.time())
        random.seed(timestamp)
        random_integer = random.randint(0, 1000)
        document_id += str(random_integer)
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404
        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{document_id}",
            headers={
                "Accept": "application/fhir+json;version=1",
                "Authorization": f"Bearer {token}",
                "NHSD-End-User-Organisation-ODS": self.end_user_ods,
                "X-Request-Id": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
                "X-Correlation-Id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    @pytest.mark.debug
    def test_post_delete_put_document_reference(self, get_token_client_credentials):
        """
           Test for the POST, Delete and PUT /DocumentReference endpoint. This operation will call the Producer NRL API.
        """
        document_id = "V4T0L-"
        timestamp = int(time.time())
        random.seed(timestamp)
        random_integer = random.randint(0, 1000)
        document_id += str(random_integer)
        # Given
        token = get_token_client_credentials["access_token"]
        expected_post_status_code = 201
        expected_delete_status_code = 200
        expected_put_status_code = 404
        request_payload = {
                        "resourceType": "DocumentReference",
                        "id": document_id,
                        "type": {
                                "coding": [
                                  {
                                   "system": "https://snomed.info/ict",
                                   "code": "3457005",
                                   "display": "Royal College of Physicians NEWS2 (National Early Warning Score 2) chart"
                                  }
                                ]
                                },
                        "subject": {
                                   "identifier":
                                   {
                                     "system": "https://fhir.nhs.uk/Id/nhs-number",
                                     "value": self.end_user_nhs_number
                                   }
                                   },
                        "status": "active",
                        "content": [
                         {
                          "attachment":
                          {
                            "language": "en-UK",
                            "url": "http://fhir.nhs.uk/Id/dos-service-id%7C111111111",
                            "size": 0,
                            "title": "Physical",
                            "creation": "2005-12-24T09:35:00+11:00"
                          }
                         }
                        ],
                        "custodian": {
                          "identifier": {
                                        "system": "https://fhir.nhs.uk/Id/ods-organization-code",
                                        "value": self.end_user_ods
                                        }
                                     }
                          }
        json_payload = json.dumps(request_payload)
        # When
        post_response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference",
            headers={
                "Accept": "application/fhir+json;version=1",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "NHSD-End-User-Organisation-ODS": self.end_user_ods,
                "X-Request-Id": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
                "X-Correlation-Id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
            },
            data=json_payload
        )

        delete_response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{document_id}",
            headers={
                "Accept": "application/fhir+json;version=1",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "NHSD-End-User-Organisation-ODS": self.end_user_ods,
                "X-Request-Id": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
                "X-Correlation-Id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
            }
        )

        put_response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{document_id}",
            headers={
                "Accept": "application/fhir+json;version=1",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "NHSD-End-User-Organisation-ODS": self.end_user_ods,
                "X-Request-Id": "60E0B220-8136-4CA5-AE46-1D97EF59D068",
                "X-Correlation-Id": "11C46F5F-CDEF-4865-94B2-0EE0EDCC26DA",
            },
            data=json_payload
        )

        # Then
        assert_that(expected_post_status_code).is_equal_to(post_response.status_code)
        assert_that(expected_delete_status_code).is_equal_to(delete_response.status_code)
        assert_that(expected_put_status_code).is_equal_to(put_response.status_code)
