var accessToken;
var cachedAccessToken = context.getVariable("nrflCachedAccessToken");

if (cachedAccessToken) {
    access_token = cachedAccessToken;
} else {
    var respContent=context.getVariable('nrlfTokenResponse.content');
    var respObject=JSON.parse(respContent)
    accessToken = respObject["accessToken"]
}

context.setVariable("nrlfAccessToken", accessToken)
context.setVariable("request.header.Authorization", "Bearer " + accessToken);
