exports.handler = async function (event, context) {
  console.log('EVENT: \n' + JSON.stringify(event, null, 2))
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: 'Hello from mock-receiver',
    }),
  }
}
