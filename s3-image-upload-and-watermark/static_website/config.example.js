const awsIdentityPool = '<cognito-identity-pool-id>' // AWS Cognito ID, to claim Role to access S3 Buckets
const awsRegion = '<your-region>'; // Region of your S3 Buckets
const bucketNamePriv = '<private-s3-bucket>'; // Private S3 Bucket that holds original images (upload)
const bucketNamePub = '<public-s3-bucket>'; // Public S3 Bucket that shows watermarked images (website)
const folderPub = '<public-s3-folder>'; // The S3 Folder where the images are stored