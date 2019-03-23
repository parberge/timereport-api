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
To deploy to dev, open A pull request and it will automtically deploy

### PRODUCTION
to deploy to prod, push/merge to master.

### Manually
__note__: This requires that you have setup the credentials for AWS

### DEV
`chalice deploy --stage dev`
### PROD
`chalice deploy --stage prod`