function makeResponse(errorObject, statusCode) {
    return {
        content: JSON.stringify(errorObject),
        statusCode: statusCode
    }
}

function handleError(context) {
    // PROXY flow

    if (context.getVariable("raisefault.RaiseFault.QuotaPerApp.failed")) {
        return makeResponse(errorRepository["429RateLimiting"], 429)
    }
    // Authorization
    const tokenFaultName = context.getVariable("oauthV2.OauthV2.VerifyAccessToken.fault.name")

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

    // Target flow
    // Request Validation
    if (context.getVariable("script.Python.DecodeBase64.failed")) {
        return makeResponse(errorRepository["400InvalidBase64Encoding"], 400)
    }
    if (context.getVariable("idMalformed")) {
        return makeResponse(errorRepository["400InvalidTargetIdentifierValue"], 400)
    }

    // Response error handling
    const errorStatusCode = context.getVariable("error.status.code")

    if (errorStatusCode === 503) {
        return makeResponse(errorRepository["503ServiceUnavailable"], 503)
    }
    if (errorStatusCode === 500 ) {
        if (context.getVariable("operation-outcome.code") === "no-store") {
            return makeResponse(errorRepository["500ServerErrorNoStore"], 500)
        } 
        else if (context.getVariable("operation-outcome.code") === null) {
            return makeResponse(errorRepository["500ServerErrorException"], 500)
        }
    }
    if (errorStatusCode === 504) {
        return makeResponse(errorRepository["408TimeoutError"], 408)
    }

    if (context.getVariable("isError")) {
        return makeResponse(errorRepository["404ProxyNotFound"], 404)
    }
    
    if (errorStatusCode === 406) {
        return makeResponse(errorRepository["406SendNotAcceptable"], 406)
    }

    const responseStatusCode = context.getVariable("response.status.code")
    if (responseStatusCode === 403) {
        return makeResponse(errorRepository["403ReceiverMtls"], 403)
    }
}

var errorResponse = null;

const validationError = context.getVariable("validation.error")
if (validationError) {
    errorResponse  = makeResponse(errorRepository[validationError.name], validationError.statusCode)
} else {
    errorResponse = handleError(context)
}

context.setVariable("errorContent", errorResponse.content)
context.setVariable("errorStatusCode", errorResponse.statusCode)

