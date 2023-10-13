var responseBody = response.body.asJson;

if (responseBody && responseBody.targets) {
    var extractedTarget = responseBody.targets;

    context.setVariable("myExtractedURL", extractedTarget);
}