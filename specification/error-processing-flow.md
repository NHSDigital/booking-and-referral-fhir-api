## General errors

```mermaid
stateDiagram-v2
    [*] --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> A6
    A6 --> A7 
    A7 --> A8
    A8 --> A9
    A9 --> A10
    A10 --> A11
    A11 --> A12
    A12 --> A13
    A13 --> A14
    A14 --> A15
    A15 --> A16
    A16 --> A17
    A17 --> A18
    A18 --> A19
    A19 --> A20
    A20 --> A21
    A21 --> A22
    A22 --> A23
    A23 --> A24
    A24 --> A25

    A1 --> 400_SEND_BAD_REQUEST: Required header not present (code - invalid)
    A2 --> 401_SEND_UNAUTHORIZED: Access Token is invalid/expired (code - security)
    A3 --> 401_SEND_UNAUTHORIZED2: Access Token not provided (code - unknown)
    A4 --> 403_SEND_FORBIDDEN: Access Token is valid but BaRS is not enabled (code - forbidden)
    A5 --> 429_SEND_TOO_MANY_REQUESTS: when rate limiting is applied (code - throttled)
    A6 --> 404_PROXY_NOT_FOUND: Endpoint on the API does not exist (code - not-found)
    A7 --> 405_SEND_METHOD_NOT_ALLOWED: using the wrong http verb (code - not-supported)
    A8 --> 406_SEND_NOT_ACCEPTABLE: The requested resource is capable of generating only content not acceptable according to the Accept headers sent in the request (code - processing)
    A9 --> 500_PROXY_SERVER_ERROR: Unexpected error (code - exception)
    A10 --> 400_PROXY_BAD_REQUEST: A structural issue in the content such as the Target identifier is malformed (code - structure)
    A11 --> 404_PROXY_NOT_FOUND2: The target endpoint does not exist in the Endpoint Catalogue (code - not-found)
    A12 --> 404_PROXY_NOT_FOUND3: The Target Identifier found two endpoints (code - multiple-matches)
    A13 --> 500_PROXY_SERVER_ERROR2: A sub-service encountered an unhandled exception (code - exception)
    A14 --> 503_PROXY_UNAVAILABLE: A sub-service was unavailble (code - transient)
    A15 --> 408_REC_TIMEOUT: The connection to the Receiver timed out (code - timeout)
    A16 --> 500_REC_SERVER_ERROR: 500 response received but no operation outcome (code - exception)
    A17 --> 503_REC_SERVICE_UNAVAILABLE: 503 response received but no operation outcome (code - transient)
    A18 --> 400_REC_NOT_FOUND: The payload was invalid, or malformed (code - invalid)
    A19 --> 401_REC_UNAUTHORIZED: Access Control (code - security)
    A20 --> 403_REC_FORBIDDEN: TLS-MA failure (code - forbidden)
    A21 --> 403_REC_FORBIDDEN2: TLS-MA failure (code - security)
    A22 --> 500_REC_SERVER_ERROR2: The start params in a slot request were two wide resulting in a large number of results (code - too-costly)
    A23 --> 500_REC_SERVER_ERROR2: unhandled exception (code - exception)
    A24 --> 500_REC_SERVER_ERROR3: internal data storage issue (code - no-store)
    A25 --> 501_REC_NOT_IMPLEMENTED: The receiver has not yet implemented that endpoint or functionality (code - not-supported)
```

```mermaid
stateDiagram-v2
    [*] --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> A6
    A6 --> A7
    A7 --> A8
    A8 --> A9
    A9 --> A10
    A10 --> A11
    A11 --> A12

    A1 --> 401_SEND_UNAUTHORIZED: token invalid/expired
    A2 --> 400_SEND_BAD_REQUEST: missing required param
    A3 --> 405_SEND_METHOD_NOT_ALLOWED: wrong http verb
    A4 --> 429_SEND_TOO_MANY_REQUESTS: rate limiting applied
    A5 --> 406_SEND_NOT_ACCEPTABLE: requested resource not acceptable
    A6 --> 500_PROXY_SERVER_ERROR/SERVER_ERROR : unexpected exception in proxy
    A7 --> 400_REC_BAD_REQUEST: invalid param
    A8 --> 400_REC_BAD_REQUEST2: feature not yet supported
    A9 --> 406_REC_NOT_ACCEPTABLE: requested resource not acceptable
    A10 --> 409_REC_TIMEOUT: receiver timed out (proxy triggering 504)
    A11 --> 500_REC_SERVER_ERROR: unexpected exception in receiver 
    A12 --> 501_REC_NOT_IMPLEMENTED: receiver not yet implemented endpoint
```

## General errors implemented so far

```mermaid
stateDiagram-v2
    [*] --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> A6
    A6 --> A7
    A7 --> A8


    A1 --> 401_REC_UNAUTHORIZED: proxy to receiver unauthorized, TLS-MA failure?
    A2 --> 403_REC_FORBIDDEN: TLS-MA faliure
    A3 --> 406_SEND_NOT_ACCEPTABLE: requested resource not acceptable
    A4 --> 409_REC_CONFLICT: no longer valid, should be REC_TIMEOUT receiver timed out (proxy triggering 504)
    A5 --> 422_REC_UNPROCESSABLE_ENTITY: The start time range requested is too wide (/Slot specific)
    A6 --> 500_REC_SERVER_ERROR: unexpected exception in receiver 
    A7 --> 501_REC_NOT_IMPLEMENTED : receiver not yet implemented endpoint
    A8 --> 503_REC_SERVICE_UNAVAILABLE: The service(s) is unavailable but is able to respond as such (endpoint specific?)
```

## Endpoint specific errors

### /Appointment/{id}
```mermaid
graph LR
    A[GET /Appointment/id] -->B{ID parameter correct format?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{GET request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F{Resource exist?}
    F --> |false| G[403 REC_NOT_FOUND]
    F --> |true| H[200 OK]
```
### /Appointment
```mermaid
graph LR
    A[GET /Appointment] -->B{required headers present?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{GET request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F[200 OK]
```
### /MessageDefinition
```mermaid
graph LR
    A[GET /MessageDefinition] -->B{required headers present?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{GET request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F[200 OK]
```
### /metadata
```mermaid
graph LR
    A[GET /metadata] -->B{required headers present?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{GET request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F[200 OK]
```
### /$process-message
```mermaid
graph LR
    A[POST /$process-message] -->B{required headers present?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{POST request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F[200 OK]
```
### /ServiceRequest
```mermaid
graph LR
    A[GET /ServiceRequest] -->B{required headers present?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{GET request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F[200 OK]
```
### /ServiceRequest/{id}
```mermaid
graph LR
    A[GET /ServiceRequest/id] -->B{required headers present?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{GET request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F[200 OK]
```
### /Slot
```mermaid
graph LR
    A[GET /Slot] -->B{required headers present?}
    B --> |false| C[400 REC_BAD_REQUEST]
    B --> |true| D{GET request?}
    D --> |false| E[405 REC_METHOD_NOT_ALLOWED]
    D --> |true| F[200 OK]
```