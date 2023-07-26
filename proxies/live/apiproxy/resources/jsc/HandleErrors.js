const makeError = (id, profile, severity, code, system, systemCode, diagnostics) => {
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
        id = "d7aaf12e-7b94-4ef6-b047-d2d92981b1cd",
        profile = "https://simplifier.net/guide/UKCoreDevelopment2/ProfileUKCore-OperationOutcome",
        severity = "error",
        code = "security",
        system = "https://fhir.nhs.uk/Codesystem/http-error-codes",
        systemCode = "SEND_UNAUTHORIZED",
        diagnostics = "The user or system was not able to be authenticated, either the access token was invalid, or not provided."
    )
}

const pickError = (context) => {
    if (context.getVariable("oauthV2.OauthV2.VerifyAccessToken.failed")) {
        return errorRepository["401UnauthorizedSecurity"]
    }
}

pickError(context)
