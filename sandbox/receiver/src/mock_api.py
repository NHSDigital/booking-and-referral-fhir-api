from flask import Flask, request, Response
import os

app = Flask(__name__)


@app.route("/meta")
def meta():
    global expected_response
    env_name = os.environ["ENV_NAME"]

    if "response-type" in request.headers:
        expected_response = request.headers["response-type"]

    return Response(
        response_builder(expected_response, env_name),
        status=expected_response,
        mimetype="application/json",
    )


def response_builder(http_code_response, env_name):
    if http_code_response == "200":
        return (
            '{ "providerName": "%s", "resourceType": "CapabilityStatement", "meta": { "profile": [ '
            '"https://www.hl7.org/fhir/CapabilityStatement" ] }, "fhirVersion": "4.0.1", "status": "active" }'
            % env_name
        )
    elif http_code_response == "400":
        return (
            '{ "providerName": "%s", "resourceType": "OperationOutcome", "meta": { "profile": [ '
            '"http://hl7.org/fhir/STU3/operationoutcome" ] }, "issue": [ { "severity": "error", "code": "invalid", '
            '"details": { "coding": [ { "system": "https://fhir.nhs.uk/STU3/ValueSet/Spine-ErrorOrWarningCode-1", '
            '"code": "BAD_REQUEST" } ] }, "diagnostics": "Any further internal debug details i.e. stack trace '
            'details etc." } ] } ' % env_name
        )
    elif http_code_response == "401":
        return (
            '{ "providerName": "%s", "resourceType": "OperationOutcome", "meta": { "profile": [ '
            '"http://hl7.org/fhir/STU3/operationoutcome" ] }, "issue": [ { "severity": "error", "code": "invalid", '
            '"details": { "coding": [ { "system": "https://fhir.nhs.uk/STU3/ValueSet/Spine-ErrorOrWarningCode-1", '
            '"code": "BAD_REQUEST" } ] }, "diagnostics": "Any further internal debug details i.e. stack trace '
            'details etc." } ] } ' % env_name
        )
    elif http_code_response == "403":
        return (
            '{"providerName": "%s", "resourceType": "OperationOutcome", "meta": {"profile": [ '
            '"http://hl7.org/fhir/STU3/operationoutcome" ] }, "issue": [ { "severity": "error", "code": "invalid", '
            '"details": { "coding": [ { "system": "https://fhir.nhs.uk/STU3/ValueSet/Spine-ErrorOrWarningCode-1", '
            '"code": "BAD_REQUEST" } ] }, "diagnostics": "Any further internal debug details i.e. stack trace '
            'details etc." } ] } ' % env_name
        )
    elif http_code_response == "404":
        return (
            '{"providerName": "%s", "resourceType": "OperationOutcome", "meta": {"profile": [ '
            '"http://hl7.org/fhir/STU3/operationoutcome" ] }, "issue": [ { "severity": "error", "code": "invalid", '
            '"details": { "coding": [ { "system": "https://fhir.nhs.uk/STU3/ValueSet/Spine-ErrorOrWarningCode-1", '
            '"code": "BAD_REQUEST" } ] }, "diagnostics": "Any further internal debug details i.e. stack trace '
            'details etc." } ] } ' % env_name
        )
    elif http_code_response == "500":
        return (
            '{"providerName": "%s", "resourceType": "OperationOutcome", "meta": {"profile": [ '
            '"http://hl7.org/fhir/STU3/operationoutcome" ] }, "issue": [ { "severity": "error", "code": "invalid", '
            '"details": { "coding": [ { "system": "https://fhir.nhs.uk/STU3/ValueSet/Spine-ErrorOrWarningCode-1", '
            '"code": "BAD_REQUEST" } ] }, "diagnostics": "Any further internal debug details i.e. stack trace '
            'details etc." } ] } ' % env_name
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
