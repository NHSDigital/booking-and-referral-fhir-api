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

    A1 --> 400_SEND_BAD_REQUEST: missing required param
    A2 --> 400_REC_BAD_REQUEST: invalid param
    A3 --> 400_REC_BAD_REQUEST2: feature not yet supported
    A4 --> 401_SEND_UNAUTHORIZED: token invalid/expired
    A5 --> 405_SEND_METHOD_NOT_ALLOWED: wrong http verb
    A6 --> 406_SEND_NOT_ACCEPTABLE: requested resource not acceptable
    A7 --> 406_REC_NOT_ACCEPTABLE: requested resource not acceptable
    A8 --> 429_SEND_TOO_MANY_REQUESTS: rate limiting applied
    A9 --> 409_REC_TIMEOUT: receiver timed out (proxy triggering 504)
    A10 --> 500_REC_SERVER_ERROR: unexpected exception in receiver 
    A11 --> 500_PROXY_SERVER_ERROR/SERVER_ERROR : unexpected exception in proxy
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