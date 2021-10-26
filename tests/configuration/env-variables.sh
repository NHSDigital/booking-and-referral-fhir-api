## SSO callback URL
export SSO_LOGIN_URL='https://login.apigee.com'

## Target environment name
export APIGEE_ENVIRONMENT='sandbox'

export BASE_URL='https://'$APIGEE_ENVIRONMENT'.api.service.nhs.uk'
export SERVICE_BASE_PATH='booking-and-referral'
export FULLY_QUALIFIED_SERVICE_NAME='booking-and-referral-'$APIGEE_ENVIRONMENT

## Just used to run Integration tests
## Stored on AWS secret manager
export CLIENT_ID='{PLACEHOLDER}' #int env
export CLIENT_SECRET='{PLACEHOLDER}' #int env

export REDIRECT_URL='https://nhsd-apim-testing-internal-dev.herokuapp.com/callback' #int env
export APIGEE_API_TOKEN=`./get_token -u andre.silva2@nhs.net`
export SSO_LOGIN_URL=https://login.apigee.com
export JWT_PRIVATE_KEY_ABSOLUTE_PATH="{PLACEHOLDER}"
export OAUTH_BASE_URI="https://$APIGEE_ENVIRONMENT.api.service.nhs.uk"
export OAUTH_PROXY="oauth2"

#Stored on AWS secret managet
export JWT_PRIVATE_KEY_ABSOLUTE_PATH='{PLACEHOLDER}'
export ID_TOKEN_NHS_LOGIN_PRIVATE_KEY_ABSOLUTE_PATH='{PLACEHOLDER}'
export ID_TOKEN_PRIVATE_KEY_ABSOLUTE_PATH='{PLACEHOLDER}'
