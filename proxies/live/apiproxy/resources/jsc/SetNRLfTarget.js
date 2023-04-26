// Override target url
context.setVariable(
    "target.url",
    "https://sandbox.api.service.nhs.uk/record-locator/consumer/FHIR/R4/DocumentReference?subject:identifier=" + context.getVariable("query_params.subjectIdentifier")
)
