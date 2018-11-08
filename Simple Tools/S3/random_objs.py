import boto3, botocore
import uuid
import argparse
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

s3 = boto3.resource('s3')

# Parse Arguments
parser = argparse.ArgumentParser(description='This script creates a number of S3 objects, optionally with versions included')
parser.add_argument('--objects', nargs=1, default=0, type=int, help='Number of S3 objects to create', metavar='x')
parser.add_argument('--versions', nargs=1, default=0, type=int, help='Number of S3 versions to create', metavar='x')
parser.add_argument('--bucket', nargs=1, type=str, help='Name of the S3 bucket', metavar='my-cool-bucket')
args = parser.parse_args()

# --------------------
# - Helper Functions -
# --------------------

# Checks if S3 Bucket exists
def bucket_exists(bucket):
  try:
    s3.meta.client.head_bucket(Bucket=bucket) # try a HEAD operation at the bucket
    return True
  except botocore.exceptions.ClientError as e: # search errors for 404
    error_code = int(e.response['Error']['Code'])
    if error_code == 403:
      return True
    elif error_code == 404:
      return False
  except botocore.exceptions.ParamValidationError as e: # seach for errors
    print (e)
    exit()
  except:
    print ("Unknown error while checking if Bucket exists")
    exit()
  
# Create an S3 Bucket
def create_bucket(bucket):
  print "Creating Bucket..."

  myBucket = s3.Bucket(bucket)
  if bucket_exists(bucket) == False:
    try:
      myBucket.create(ACL='private',CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})
      print "Successfully created bucket: "+bucket
      return myBucket
    except:
      print ("Unknown error while trying to create Bucket")
      exit()
  else:
    print "Bucket already exists"
    return myBucket


# Create a Number of Random Objects
def create_objects(bucket, number):
  for i in range(number):
    objectName = str(i+1)+'-Object'
    object = s3.Object(bucket.name, objectName)
    currentDate = datetime.datetime.now()
    objectContent = 'Date: '+str(currentDate)+'\nObject number: '+str(i)
    object.put(ACL='private', Body=objectContent, ContentType='text/plain')
  print ("Created {0} objects in Bucket: {1}".format(i+1, bucket.name))

# Enable Versioning and create Versions
def create_versions(bucket, number):
  global numObjects
  # Activate Versioning
  bucket_versioning = bucket.Versioning()
  bucket_versioning.enable()
  print ("Enabled Versioning on Bucket: "+bucket.name)

  numObj = numObjects[0]
  # Create Random Versions
  if number > numObj:
    n = number/numObj
  else:
    n = 1

  for v in range(n):
    for o in range(numObj):
      objectName = str(o+1)+'-Object'
      object = s3.Object(bucket.name, objectName)
      currentDate = datetime.datetime.now()
      objectContent = 'Date: '+str(currentDate)+'\nObject number: '+str(o+1)+'\nVersion number: '+str(v+1)
      object.put(ACL='private', Body=objectContent, ContentType='text/plain')

# --------
# - Main -
# --------

bucket = args.bucket
numObjects = args.objects
numVersions = args.versions
if bucket == None:
  bucketName = 'deleteme-'+str(uuid.uuid4())
  print "Using a random Bucket name: "+bucketName
else:
  bucketName = bucket[0]
  print "Using the given Bucket name: "+bucketName

s3Bucket = create_bucket(bucketName)

if numObjects > 0:
  create_objects(s3Bucket, numObjects[0])
else:
  print "Number of objects is: {0}, so no objects will be created"

if numVersions > 0:
  create_versions(s3Bucket, numVersions[0])
else:
  print "Number of versions is: {0}, so no versions will be created and Versioning may not be enabled"

print (bcolors.OKBLUE+bcolors.BOLD+"Created Bucket: "+bcolors.ENDC+"{0} with {1} Objects and {2} Versions".format(bucketName, numObjects, numVersions))

