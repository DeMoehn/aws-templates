# S3 Tools

Here are some Tools to work with S3

## Cleanup S3

This cleans up S3 buckets and deletes all the included objects and versions by default!

Use:

- --includes 'test' to Delete ALL buckets that include a given string. Works
                        with regex.
- or:
- --buckets Bucket1 Bucket2 ... [Bucket1 Bucket2 ... ...] Only deletes a specific buckets
- or:
- --help to get more information

## Random Objects

This script creates/uses an S3 Bucket and creates objects and versions

Use:

- --objects x for the Number of S3 objects to create
- --versions x for the Number of S3 versions to create (if this is > objects, mupltiple versions of one object will be created)
- --bucket my-cool-bucket to Name a specific S3 bucket (existent or not)