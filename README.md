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

## Event model
```
[
  {
    "reason": "sick",
    "hours": "8",
    "user_name": "Mr User",
    "user_id": "user101",
    "event_date": "2019-03-21"
  }
]
```

## RESTful resources

Resources exposed through the api

Expects `Content-Type: appplication/json`

##### Tables
```
GET    /table-names                   # list dynamo tables
```

##### User context
```
GET    /users                         # list users
GET    /users/<user_id>               # get user
GET    /users/<user_id>/events        # list all user events
DELETE /users/<user_id>/events        # delete all user events
GET    /users/<user_id>/locks         # list all user locks
DELETE /users/<user_id>/locks         # delete all user locks
DELETE /users/<user_id>/locks/<date>  # delete user lock by date
GET    /users/<user_id>/events/<date> # get user event by date
DELETE /users/<user_id>/events/<date> # delete user event by date
```

##### Event context
```
GET    /events                 # list events
POST   /events                 # create event
GET    /events/dates/<date>    # get all events by date
DELETE /events/dates/<date>    # delete all events by date
```

##### Lock context
```
GET    /locks                  # list locks
POST   /locks                  # create lock
GET    /locks/dates/<date>     # list all locks by date
DELETE /locks/dates/<date>     # delete all locks by date
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
