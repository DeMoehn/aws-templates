// Cognito Configuration
AWS.config.region = awsRegion;
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: awsIdentityPool
});

// S3 Configuration
var bucketPriv = new AWS.S3({params: {Bucket: bucketNamePriv}});
var bucketPub = new AWS.S3({params: {Bucket: bucketNamePub}});

// DOM Configuration
var fileChooser = document.getElementById('file-chooser');
var filePreview = document.getElementById('file-preview');
var button = document.getElementById('upload-button');
var hint = document.getElementById('hint');
var resultsInfo = document.getElementById('results-info');
var results = document.getElementById('results');

// Variables Configuration
var prevPicLength = 0; // Length of the picture array from last search
var previewImg = filePreview.src;

// File Chooser Event
fileChooser.addEventListener('change', function() {
    hint.innerHTML = 'File choosen';
    
    // Show preview image before upload
    var reader = new FileReader();
    reader.onload = function (e) {
        filePreview.src = e.target.result;
        filePreview.height = 100;
    };
    reader.readAsDataURL(fileChooser.files[0]);
});

// Button Event
button.addEventListener('click', function() {
    hint.innerHTML = 'Uploading file';

    var file = fileChooser.files[0];
    if (file) {
        var objKey = file.name;
        var params = {
            Key: objKey,
            ContentType: file.type,
            Body: file,
            ACL:'public-read'
        };

        // Creates object in S3
        var request = bucketPriv.putObject(params, function(err, data) {
            if (err) {
                hint.innerHTML = 'Error - ' + err;
            } else {
                hint.innerHTML = 'File successfully uploaded';
                fileChooser.value = '';
                filePreview.src = previewImg;
            }
        });
        request.on('httpUploadProgress', function (progress) { // Tracks status
            uploadProgress = ((progress.loaded/progress.total)*100);
            hint.innerHTML = 'Uploading file ('+uploadProgress.toFixed(0)+'%)';
        });
        request.send();
    } else {
        hint.innerHTML = 'Nothing to upload';
    }
}, false);

function listObjs() {
    resultsInfo.innerHTML = 'Looking for new pictures...';
    var prefix = folderPub+'/';

    // Lists all objects in a specific bucket
    bucketPub.listObjects({
        Prefix: prefix
    }, function(err, data) {
        if (err) {
            resultsInfo.innerHTML = 'ERROR: ' + err;
        } else {
            setTimeout(createImages, 2000, data); // Not really needed here, just to avoid constant change of resultsInfo text
        }
    });
}

// If available, creates Images in HTML site
function createImages(data) {
    var objKeys = "";
    if(data.Contents.length <= 0) {
        resultsInfo.innerHTML = 'No pictures available.';
    }else{
        if(data.Contents.length > prevPicLength) {
            results.innerHTML = '';
            data.Contents.forEach(function(obj) {
                var url = 'http://'+bucketNamePub+'.s3-website.'+awsRegion+'.amazonaws.com/'+obj.Key;
                results.innerHTML += '<a href="'+url+'" target="_blank"><img height="200px" src="'+url+'"></a>';
            });
            resultsInfo.innerHTML = 'Pictures loaded.';
        }else{
            resultsInfo.innerHTML = 'No new pictures found.';
        }
    }
    prevPicLength = data.Contents.length;
    setTimeout(listObjs, 3000); // Not really needed here, just to avoid constant change of resultsInfo text
}

listObjs(); // Call the function once