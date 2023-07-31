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

