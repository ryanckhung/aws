const AWS = require('aws-sdk');
AWS.config.update({region: 'ap-east-1'});

module.exports = {
    generatePresignedUrl: async function(bucketName, objectKey) {

        // Create an instance of the S3 client
        const s3 = new AWS.S3();

        // Generate the presigned URL
        const url = await s3.getSignedUrlPromise('putObject', {
            Bucket: bucketName,
            Key: objectKey,
            Expires: 60*3 // The URL will expire after 60 seconds *3
        });

        //console.log(url)
        return url;
    },

    objectExists: async function(bucketName, objectKey) {
        const s3 = new AWS.S3();
        try {
          await s3.headObject({ Bucket: bucketName, Key: objectKey }).promise();
          return true;
        } catch (error) {
          return false;
        }
    },

    getSignedUrl: async function (bucketName, objectKey) {
        const s3 = new AWS.S3();
        try {
            const url = await s3.getSignedUrlPromise('getObject', { Bucket: bucketName, Key: objectKey, Expires: 60*3 });
            return {"success": true, "data": url};        
        } catch (error) {
            console.log("error")
            return {"success": false, "data": ""};
        }
      }
}
