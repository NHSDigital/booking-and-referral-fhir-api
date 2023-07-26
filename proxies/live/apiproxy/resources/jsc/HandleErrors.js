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
    )
}

function makeResponse(errorObject, statusCode) {
    return {
        content: JSON.stringify(errorObject),
        statusCode: statusCode
    }
}

function handleError(context) {
    const tokenFaultName = context.getVariable("oauthV2.OauthV2.VerifyAccessToken.fault.name")
    print("here")
    print(tokenFaultName)

    if (tokenFaultName === "keymanagement.service.invalid_access_token") {
        return makeResponse(errorRepository["401UnauthorizedSecurity"], 401)
    }
    if (tokenFaultName === "oauth.v2.InvalidAccessToken") {
        return makeResponse(errorRepository["401UnauthorizedUnknown"], 401)
    }
    if (tokenFaultName === "keymanagement.service.InvalidAPICallAsNoApiProductMatchFound") {
        return makeResponse(errorRepository["403ProxyNotEnabled"], 403)
    }
    if (context.getVariable("oauthV2.OauthV2.VerifyAccessToken.failed")) {
        return makeResponse(errorRepository["401UnauthorizedSecurity"], 401)
    }
}

const errorResponse = handleError(context)
context.setVariable("errorContent", errorResponse.content)
context.setVariable("errorStatusCode", errorResponse.statusCode)

