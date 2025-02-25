# Booking and Referral FHIR API


## This is a Mock receiver

This is a docker container that contains an API with endpoints to simulate providers responses.
* `/meta` endpoint - this endpoint requires a parameter `response-type`

### Parameter
`response-type` parameter must be one of the values bellow and you must expect the same code as a response.

* 200 - Success
* 400 - Bad Request
* 401 - Unauthorized
* 403 - Forbidden
* 404 - Not Found
* 500 - Internal server error


## Development

### Requirements
* python
* docker

**Note**

use the Dockerfile in the root to run this locally.

also if the dockerfile is removed from the sandbox folder this seems to break the automated build process, I dont currently have enough information as to how to fix this, so leave be for now.

### Install
Open the terminal in the project directory and run
```
$ docker build -t mock-api .
```
After build the docker container run it:
```
$ docker run -p 8080:5000 -e ENV_NAME=Internal mock-api
```
then use curl to send requests to http://localhost:8080/Appointment etc.

### Environment Variables
As you can have multiple docker container running this api you can use the `ENV_NAME` variable to identify each container.

### Testing
TBC
