var acceptHeader = context.getVariable('request.header.Accept');
var acceptArray = acceptHeader.split(';');
var versionNumber = '1.0.0';
var modifiedAcceptHeader ='';

for (var i = 0; i < acceptArray.length; i++) {
    var acceptValue = acceptArray[i].trim();
     if (acceptValue.startsWith('version=')) {
            versionNumber = acceptValue.split('=')[1];  //Getting versionNumber after '=' sign
            versionNumber = versionNumber.split('-')[0];  //Removing beta/aplha from end
    }
    else if (acceptValue.startsWith('application'))
    {
        modifiedAcceptHeader=acceptValue
    }
}

context.setVariable('versionNumber', versionNumber);
