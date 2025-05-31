### Usage
[Serverless Framework](https://github.com/serverless/serverless)
```
npm install
npm run login
npm run dev
npm run prod
npm run remove
```

### Add Logs to Kibana

Update the [AWS Lambda Cloudwatch filebeat](https://github.com/hrforceai/env/blob/main/ops/files/elk/filebeat-aws-cloudwatch.yml.j2) to include new log group for new lambda function
