#### timereport_backend

##### Requirements

###### development
- Docker (to run amazon/dynamodb-local)
- chalice local

###### production
- aws credentials for dynamodb access
- aws credentials for travis-ci
- edit .chalice/config.json env variables

##### Instructions

- make run

```
Will pull and run amazon/dynamodb-local from docker on port 8000
Make sure to run chalice as well.

#
# In Production:
#
Point os.environ['DB_URL'] to your production amazonaws database. 
#
DB_URL = http://dynamodb.eu-north-1.amazonaws.com
#
Set aws credentials as os.environ:
#
AWS_ACCESS_KEY = my_access_key_id
AWS_SECRET_ACCESS_KEY = my_secret_access_key
#
#
or configure ~/.aws/credentials file with content:
#
[default]
aws_access_key_id = myAccessKey
aws_secret_access_key = mySecretAccessKey
#
#


Chalice will create data in backend (dynamodb) as well as fetch data from it.

```
