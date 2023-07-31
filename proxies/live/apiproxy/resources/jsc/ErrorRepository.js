function makeError(id, profile, severity, code, system, systemCode, diagnostics) {
    return {
        "resourceType": "OperationOutcome",
        "id": id,
        "meta": {
            "profile": [
                profile,
            ]
        },
        "issue": [
            {
                "severity": severity,
                "code": code,
                "details": {
                    "coding": [
                        {
                            "system": system,
                            "code": systemCode
                        }
                    ]
                },
                "diagnostics": diagnostics
            }
        ]
    }
}

const errorRepository = {
    "401UnauthorizedSecurity": makeError(
        id = "d7aaf12e-7b94-4ef6-b047-d2d92981b1cd",
        profile = "https://simplifier.net/guide/UKCoreDevelopment2/ProfileUKCore-OperationOutcome",
        severity = "error",
        code = "security",
        system = "https://fhir.nhs.uk/Codesystem/http-error-codes",
        systemCode = "SEND_UNAUTHORIZED",
        diagnostics = "The user or system was not able to be authenticated, either the access token was invalid, or not provided."
    ),
    "401UnauthorizedUnknown": makeError(
        id = "e1112dbd-7aaf-412e-9b94-ef6e047d2d92",
        profile = "https://simplifier.net/guide/UKCoreDevelopment2/ProfileUKCore-OperationOutcome",
        severity = "error",
        code = "unknown",
        system = "https://fhir.nhs.uk/Codesystem/http-error-codes",
        systemCode = "SEND_UNAUTHORIZED",
        diagnostics = "No Access token was provided."
    ),
    "403ProxyNotEnabled": makeError(
        id = "3ce474db-cbc8-4682-a5ab-ca2a4eda1dae",
        profile = "https://simplifier.net/guide/UKCoreDevelopment2/ProfileUKCore-OperationOutcome",
        severity = "error",
        code = "forbidden",
        system = "https://fhir.nhs.uk/Codesystem/http-error-codes",
        systemCode = "SEND_FORBIDDEN",
        diagnostics = "The access token was provided, but BaRS is not enabled."
    ),

    // FIXME: id is not provided.
    "400InvalidBase64Encoding": makeError(
        id = "",
        profile = "https://fhir.hl7.org.uk/StructureDefinition/UKCore-OperationOutcome",
        severity = "error",
        code = "400",
        system = "http://hl7.org/fhir/ValueSet/operation-outcome",
        systemCode = "PROXY_BAD_REQUEST",
        diagnostics = "The base64 decoding of the NHSD-Target-Identifier header failed."
    )
}

