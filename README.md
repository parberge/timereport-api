# timereport-api
An API for timereport

## Architecture
* AWS API Gateway
* AWS lambda
* AWS dynamodb

## Setup

- aws credentials for dynamodb access
- aws credentials for travis-ci
- edit .chalice/config.json env variables

## RESTful resources

Resources exposed through the api

Expects `Content-Type: appplication/json`

###### Tables
```
GET    /table-names
```

###### Events
```
GET    /events
POST   /events
GET    /events/users
GET    /events/users/<name>
GET    /events/users/<name>/<date>
DELETE /events/users/<name>/<date>
GET    /events/<date>
```

###### Locks
```
GET    /locks
GET    /locks/dates
GET    /locks/users
DELETE /locks/users/<user>/<date>
DELETE /locks/dates/<date>
```

## Local development

### prerequisite
- Docker (to run amazon/dynamodb-local)
- packages in requirements.txt

To start a local dynamodb and chalice:
```
make run
```
Now you should be able to try the API on http://localhost:8010

To stop and cleanup:
```
make clean
```

## Deployment
Deployment to dev and prod is done automatically

### DEV
Deploy to dev will happen when a push/merge even happens on master branch

### PRODUCTION
Deploy to production will happen if a tag is created on the master branch

### Manually
__note__: This requires that you have setup the credentials for AWS

### DEV
`chalice deploy --stage dev`
### PROD
`chalice deploy --stage prod`

### Run unit tests
#### prerequisite
Install the packages (use pipenv)
__IMPORTANT!__ : Make sure you have started your local development environment
Run pytest:
`pytest -v tests`
