function validEndpoint(context) {
    const path = context.getVariable("proxy.pathsuffix")
    return path.startsWith("/$process-message") ||
        path.startsWith("/Slot") ||
        path.startsWith("/metadata") ||
        path.startsWith("/Appointment") ||
        path.startsWith("/ServiceRequest") ||
        path.startsWith("/registry") ||
        path.startsWith("/DocumentReference") ||
        path.startsWith("/MessageDefinition")
}

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
        const version = context.getVariable("versionNumber")
        return version === "1.1.0"
    }
    return true
}

function validate(context) {
    if (!validEndpoint(context)) {
        return {
            name: "404PageNotFound",
            statusCode: 404

        }
    }
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
