function requiredHeaders(context) {
    const hasHeader = (name) => {
        const headers = context.getVariable("request.headers.name")
        return headers
            .map(header => header.toLowerCase())
            .some(header => header === name)
    }

    return hasHeader("x-request-id") && hasHeader("x-correlation-id")
}

function apiVersion(context) {
    const path = context.getVariable("proxy.pathsuffix")
    if (path.startsWith("/DocumentReference")) {
        const version = context.getVariable("versionNumber")
        return version === "1.1.0"
    }
}

function validate(context) {
    if (!requiredHeaders()) {
        return {
            name: "400InvalidHeaders",
            statusCode: 400

        }
    }
    if (!apiVersion(context)) {
        return {
            name: "406PageNotAcceptable",
            statusCode: 406
        }
    }

    return null
}

context.setVariable("validation.error", validate(context))
