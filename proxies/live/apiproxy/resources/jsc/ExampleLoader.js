var fs = require("fs");
  
let rawdata = fs.readFileSync("../examples/metadata/BaRS_API_Capability_Statement .json");
let data = JSON.parse(rawdata);

context.setVariable("data", data);