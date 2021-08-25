# Booking and Referral FHIR API


##This is a Mock receiver

This is a docker container that contains a Flask API with a single endpoint to simulate providers responses.
* `/meta` endpoint - the only one endpoint available requires an parameter `response-type`

###Parameter
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


### Install
Open the terminal in the project directory and run
```
$ docker build -t mock-api .
```
After build the docker container run it:
```
$ docker run -p 8080:5000 -e ENV_NAME=Internal mock-api
```


### Environment Variables
As you can have multiple docker container running this api you can use the `ENV_NAME` variable to identify each container.

### Testing
TBC
