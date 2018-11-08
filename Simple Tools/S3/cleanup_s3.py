import boto3
import sys
import argparse
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

client = boto3.client('s3') # AWS S3 client
paginator = client.get_paginator('list_object_versions') # Use the Paginator to page trough all versions, use 'list_object_versions' instead of '#list_objects_v2' to get all versions of all objects

objCount = 0
versCount = 0

# Parse Arguments
parser = argparse.ArgumentParser(description='This script deletes S3 Buckets, as well as the objects and versions. By default it deletes all buckets that include "deleteme')
g = parser.add_mutually_exclusive_group()
g.add_argument('--includes', action='store', type=str, help='Delete ALL buckets that include a given string. Works with regex.', metavar="'test'")
g.add_argument('--buckets', nargs='+', action='store', type=str, help='Only deletes a specific buckets', metavar='Bucket1 Bucket2 ...')
args = parser.parse_args()

# --------------------
# - Helper Functions -
# --------------------

def query_yes_no(question, default="yes"):
  valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
  if default is None:
    prompt = " [y/n] "
  elif default == "yes":
    prompt = " [Y/n] "
  elif default == "no":
    prompt = " [y/N] "
  else:
    raise ValueError("invalid default answer: '%s'" % default)

  while True:
    sys.stdout.write(question + prompt)
    choice = raw_input().lower()
    if default is not None and choice == '':
      return valid[default]
    elif choice in valid:
      return valid[choice]
    else:
      sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

def getKeys(objArr):
  global objCount, versCount

  objKeys = []
  for obj in objArr:
    if obj['IsLatest']:
      objCount += 1
    else:
      versCount += 1

    my_obj = {'Key': obj['Key'], 'VersionId': obj['VersionId']}
    objKeys.append(my_obj)
  return objKeys

def deleteBuckets(buckets):
  global objCount, versCount
  objCount = 0
  versCount = 0

  for bucket in buckets:
    response_iterator = paginator.paginate(Bucket=bucket)

    for page in response_iterator: # go trough all pages
      if 'Versions' in page and page['Versions'] is not None:
        objects = getKeys(page['Versions'])
        client.delete_objects(Bucket=bucket,Delete={'Objects': objects,'Quiet': False},)

      if 'DeleteMarkers' in page and page['DeleteMarkers'] is not None:
        delMarkers = getKeys(page['DeleteMarkers'])
        client.delete_objects(Bucket=bucket,Delete={'Objects': delMarkers,'Quiet': False},)

    print (bcolors.OKBLUE+bcolors.BOLD+"Emptied Bucket: "+bcolors.ENDC+"{0} with {1} objects and {2} versions".format(bucket, objCount, versCount))
    
    client.delete_bucket(Bucket=bucket)
    print (bcolors.OKGREEN+bcolors.BOLD+"Deleted Bucket: " +bcolors.ENDC+bucket)

# --------
# - Main -
# --------

# Function that searches for RegEx Matches in all Buckets
def deleteAllBuckets(searchString, sBuckets=[], doSearch=True):
  deleteMeBucketFound = False
  bucketNum = 0
  buckets = []
  usingsearchString = False

  if searchString != "":
    usingsearchString = True

  rxString = searchString

  all_buckets = client.list_buckets()

  for bucket in all_buckets['Buckets']:
    if usingsearchString:
      searchObj = re.search(rxString, bucket['Name'])
    else:
      searchObj = bucket['Name'] in sBuckets

    if searchObj:
      bucketNum += 1
      print (bcolors.OKBLUE+bcolors.BOLD+"Bucket found: "+bcolors.ENDC+bucket['Name'])
      buckets.append(bucket['Name'])
      deleteMeBucketFound = True

  if deleteMeBucketFound:
    question = "A total of {0} Buckets found. Do you really want to delete those S3 Buckets, all it's objects and versions permanently?".format(bucketNum)
    if query_yes_no(question, default="no"):
      print bcolors.BOLD+bcolors.FAIL+"Deleting all Buckets now, no return!"+bcolors.ENDC
      deleteBuckets(buckets)
    else:
      print (bcolors.OKGREEN+bcolors.BOLD+"Fine, I won't do anything."+bcolors.ENDC)
  else:
    if usingsearchString:
      print ("No Buckets found that include '{0}' in their name.".format(searchString))
    else:
      print ("No Buckets with the name(s) '{0}' found.".format(", ".join(sBuckets)))
      

# Code
if args.includes != None:
  deleteAllBuckets(args.includes)

if args.buckets != None:
  deleteAllBuckets("", args.buckets)