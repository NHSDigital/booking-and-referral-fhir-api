const fs = require("fs");

var rawdata = fs.readFileSync("../examples/metadata/BaRS_API_Capability_Statement .json");
var data = JSON.parse(rawdata);

context.setVariable("data", data);