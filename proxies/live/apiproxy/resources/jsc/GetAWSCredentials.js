const AWS = require('aws-sdk');
// Configure AWS Region (Replace with your region)
AWS.config.update({ region: 'eu-west-2' });
// IAM Role to assume 
const roleArn = 'arn:aws:iam::790083933819:role/bars_s3_user_role';
// Session name 
const roleSessionName = 'ApigeeSession'; 
const sts = new AWS.STS();
const params = {
 RoleArn: roleArn,
 RoleSessionName: roleSessionName
};
sts.assumeRole(params, (err, data) => {
 if (err) {
   context.setVariable('error', err.message);
 } else {
   const credentials = data.Credentials;
   context.setVariable('aws_access_key_id', credentials.AccessKeyId);
   context.setVariable('aws_secret_access_key', credentials.SecretAccessKey);
   context.setVariable('aws_session_token', credentials.SessionToken);
 }
});

// Create S3 object with temporary credentials
const s3 = new AWS.S3({
    accessKeyId: context.getVariable('aws_access_key_id'),
    secretAccessKey: context.getVariable('aws_secret_access_key'),
    sessionToken: context.getVariable('aws_session_token')
   });
   // S3 bucket and object key (Replace with your values)
   const bucketName = 'booking-and-referral-targets-int';
   const objectKey = 'targets.json';
   // Get object from S3
   s3.getObject({ Bucket: bucketName, Key: objectKey }, function(err, data) {
    if (err) {
      context.setVariable('error', err.message);
    } else {
      context.setVariable('s3_object_content', data.Body.toString('utf-8')); // Assuming text content
    }
   });