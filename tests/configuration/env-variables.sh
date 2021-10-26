## SSO callback URL
export SSO_LOGIN_URL='https://login.apigee.com'
## target environment
export APIGEE_ENVIRONMENT='internal-dev'
## target environment
export BASE_URL='https://internal-dev.api.service.nhs.uk'
export SERVICE_BASE_PATH='booking-and-referral'
export FULLY_QUALIFIED_SERVICE_NAME='booking-and-referral-internal-dev'
export CLIENT_ID='Too5BdPayTQACdw1AJK1rD4nKUD0Ag7J' #int env
export CLIENT_SECRET='wi7sCuFSgQg34ZWO' #int env
export REDIRECT_URL='https://nhsd-apim-testing-internal-dev.herokuapp.com/callback' #int env
export APIGEE_API_TOKEN=`./get_token -u andre.silva2@nhs.net`
export SSO_LOGIN_URL=https://login.apigee.com
export JWT_PRIVATE_KEY_ABSOLUTE_PATH="/Users/Andre.c.silva/internal-dev-jwt.key"
export OAUTH_BASE_URI="https://$APIGEE_ENVIRONMENT.api.service.nhs.uk"
export OAUTH_PROXY="oauth2"
export JWT_PRIVATE_KEY_ABSOLUTE_PATH='/Users/Andre.c.silva/IW/APIM/utils-snippets/key.txt'
export ID_TOKEN_NHS_LOGIN_PRIVATE_KEY_ABSOLUTE_PATH='/Users/Andre.c.silva/IW/APIM/utils-snippets/nhsLoginTestRS512.key'
export ID_TOKEN_PRIVATE_KEY_ABSOLUTE_PATH='/Users/Andre.c.silva/IW/APIM/utils-snippets/idTokenKey.txt'

