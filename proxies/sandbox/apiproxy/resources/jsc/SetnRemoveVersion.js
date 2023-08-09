var acceptHeader = context.getVariable('request.header.Accept');
var acceptArray = acceptHeader.split(';');
var versionNumber = '1.0.0';

for (var i = 0; i < acceptArray.length; i++) {
    var acceptValue = acceptArray[i].trim();
    versionNumber = acceptValue.split('=')[1];  //Getting versionNumber after '=' sign
}

context.setVariable('versionNumber', versionNumber);
