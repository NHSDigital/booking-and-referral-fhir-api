function hasRequiredHeaders(context) {
    const headers = context.getVariable("request.headers.names").toArray()

    const hasHeader = (name) => {
        for (var i = 0; i < headers.length; i++) {
            if (String(headers[i]).toLowerCase().trim() === name.toLowerCase().trim()) return true
        }
        return false
    }
    return hasHeader("x-request-id") && hasHeader("x-correlation-id")
}

function isVersionValid(context) {
    const path = context.getVariable("proxy.pathsuffix")
    if (path.startsWith("/DocumentReference")) {
        const version = context.getVariable("versionNumberNumeric")
        return version >= 10100
    }
    return true
}

function validate(context) {
    if (!hasRequiredHeaders(context)) {
        return {
            name: "400InvalidHeaders",
            statusCode: 400

        }
    }
    if (!isVersionValid(context)) {
        return {
            name: "406PageNotAcceptable",
            statusCode: 406
        }
    }

    return null
}

context.setVariable("validation.error", validate(context))
