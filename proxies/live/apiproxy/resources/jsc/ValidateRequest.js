function apiVersion(context) {
    const path = context.getVariable("proxy.pathsuffix")
    if (path.startsWith("/DocumentReference")) {
        const version = context.getVariable("versionNumber")
        return version === "1.1.0"
    }
}

function validate(context) {
    if (apiVersion(context)) {
        return "406PageNotAcceptable"
    }
}

context.setVariable("validationError", validate(context))
