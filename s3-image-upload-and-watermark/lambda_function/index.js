'use strict';

console.log('Loading function...');

// Require packages
const AWS = require('aws-sdk');
var watermark = require('image-watermark'); // Image Tool (https://www.npmjs.com/package/image-watermark)
var fs = require('fs'); // Filesystem Tools

// Initial Setup
AWS.config.region = process.env.AWS_REGION;
const s3 = new AWS.S3({ apiVersion: '2006-03-01' });
const watermarkTxt = 'S3 Picture Upload';

// The main Handler for the functions
exports.handler = (event, context, callback) => {
    console.log("Starting handler...");

    // Get Event variables
    const privBucket = event.Records[0].s3.bucket.name;
    const privKey = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
    const s3PrivParams = {
        Bucket: privBucket,
        Key: privKey,
    };

    // Download the S3 Object
    getObject(s3PrivParams);
};

// Downloads the S3 Object to local disk
function getObject(s3PrivParams) {
    var file = fs.createWriteStream('/tmp/'+s3PrivParams.Key);
    // Dowloads the object and writes to disk
    s3.getObject(s3PrivParams).createReadStream().on('error', function(err){
        console.log(err);
    }).pipe(file);
    // Creates the watermark
    file.on('close', function(){
        console.log('Finished writing picture to disk');
        watermarkImage(s3PrivParams.Key, watermarkTxt); 
    });
}

// Create a watermark
function watermarkImage(img, txt) {
    var options = {
        'text': txt,
        'color':  '#FFFFFF',
        'dstPath': '/tmp/edited.jpg',
        'override-image': true,
        'resize' : '70%'
    };

    watermark.embedWatermarkWithCb('/tmp/'+img, options, function(err) {
        if (!err) {
            console.log('Succefully embeded watermark');
            uploadImage(img); // Uploads the image back to S3
        }
    });
}

// Uploads an image from disk to S3
function uploadImage(img) {
    console.log('Trying to read image: '+img);
    // Get Environment variables
    const pubBucket = process.env.S3_BUCKET_PUBLIC;
    const folderPub = process.env.BUCKET_FOLDER_PUBLIC;

    // Read all files from /tmp (just to show, that multiple can exist)
    fs.readdir('/tmp', function(err, files) {
        if(err) {
            console.log(err);
        }else{
            console.log("Files in /tmp:");
            console.log(files);
        }
    });

    // Read image from disk
    fs.readFile('/tmp/'+img, function (err, data) {
        if (err) { 
            console.log(err);
        }else{
            // Create a binary from image
            var base64data = new Buffer(data, 'binary');
            const s3PubParams = {
                Body: base64data, 
                Bucket: pubBucket,
                Key: folderPub+'/'+img,
                ACL: 'public-read',
                ContentType: 'image/jpeg'
            };

            console.log('Now uploading image: '+img);
            // Uploads image to S3
            s3.putObject(s3PubParams, function (resp) {
                console.log('Successfully uploaded image.');
            });
        }
    });
}