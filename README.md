### Docs

- [ServerLess](https://github.com/serverless/serverless)
- [AWS Chalice](https://github.com/aws/chalice)

### Init
```
nvm use 20
npm i serverless -g
npm install serverless-wsgi
```
### Login Serverless
```
serverless login # Ask to access the dgeinc organization
```
### Usage
```
serverless # Create app
```
### Update serverless.yml for region and env
```
provider:
  name: aws
  runtime: python3.8
  region: ${opt:region, 'ap-southeast-1'}  # Default region is ap-southeast-1 if not specified
  stage: ${opt:stage, 'dev'}  # Default stage is dev if not specified
```
### Update serverless.yml for AWS Lambda without API Gateway
```
functions:
  myLambdaFunction:
    handler: handler.myHandler
    # No events specified, so no API Gateway will be created
```

### Deploy and remove
```
serverless deploy --stage prod
serverless remove
```