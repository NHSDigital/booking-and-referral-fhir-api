ALLOWED_METHODS = ["GET", "POST", "DELETE", "PUT"]


def basic_lambda_handler(event, context):
    return found(event, context)


def found(event, context):

    response = {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
        },
    }
    return response
