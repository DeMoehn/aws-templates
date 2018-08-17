# S3 Image Upload and Watermark

- Uses AWS Lambda and an S3 Trigger to convert original images to resized, watermarkt images.
- Also includes a simple static HTML/JS website to upload and display images

## How to use

### Setup the Lambda

- Start a new Terminal at folder: *lambda_function* & Run `npm install` to install the dependencies
- Package all contents of *lambda_function/* to a .zip file: `zip -r -X lambda.zip *` <small>(only the contents! Not the folder itself)</small>
- (Use `aws configure` if you haven't used your AWS CLI before)
- Upload the Archive to AWS Lambda (512MB, 30s)