var access_token;
// var cached_access_token = context.getVariable("cached_access_token");

// if (cached_access_token) {
//     access_token = cached_access_token;
// } else {
    var respContent=context.getVariable('nrlfTokenResponse.content');
    var respObject=JSON.parse(respContent)
    access_token = respObject["access_token"]
// }

context.setVariable("access_token", access_token)
context.setVariable("request.header.Authorization", "Bearer " + access_token);
