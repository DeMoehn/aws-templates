'use strict';

console.log('Loading function...');
var AWS = require('aws-sdk'); 
var zlib = require('zlib');

AWS.config.region = process.env.AWS_REGION;
var s3 = new AWS.S3();
var sns = new AWS.SNS();

exports.getELBlogs = function(event, context) {  
    console.log("Loading handler...");
    var objBucket = event.Records[0].s3.bucket.name;
    var objPath = event.Records[0].s3.object.key;
    var getParams = {
      Bucket: objBucket,
      Key: objPath
    };
    s3.getObject(getParams, function (err, data) {
      if (err) {
        console.log(err);
      } else {
        zlib.gunzip(data.Body, function(err, dezipped) {
          if(err) {
            console.log(err);
          }else{
            publishSNS(dezipped.toString());
          }
        });
      }
    });

    function publishSNS(dezContent) {

      var objContent = dezContent;
      var message = 'ELB Log created in:\n';
      message += 'Bucket: '+objBucket+'\n';
      message += 'Path: '+objPath+'\n';
      message += 'LogContent: '+objContent;

      var snsContent = {Message: message, TopicArn: process.env.SNS_TOPIC};
      sns.publish(snsContent,
        function(err, data) {
          if (err) {
            console.log(err.stack);
            return;
          }
          console.log('push sent');
          console.log(data);
          context.done(null, 'Function Finished!');  
      });
    }   
};

