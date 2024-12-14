# Currency Exchange Tracking Application

This project implements a currency exchange tracking application designed to run in the AWS Lambda environment. It fetches daily exchange rates from the European Central Bank (ECB), stores them in a DynamoDB database, and provides a REST API to retrieve the current exchange rates and compare them to the previous day’s rates.

## Architecture Overview
The application uses the following AWS services:
- **AWS Lambda**: Executes the code for fetching rates and handling API requests.
- **AWS DynamoDB**: Stores exchange rate data.
- **AWS API Gateway**: Exposes the REST API to the public.
- **AWS CloudFormation**: Manages infrastructure as code.


## Directory Structure
```
exchange-tracker/
├── lambdas/
│   ├── fetch_rates.py       # Lambda function to fetch and store rates
│   ├── api_handler.py       # Lambda function to serve API requests
├── templates/
│   └── cloudformation.yaml  # CloudFormation template for AWS resources
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
```

## Setup Instructions

### 1. Install Dependencies
Run the following command to install the required Python dependencies:
```bash
pip install -r requirements.txt -t lambdas/
```

### 2. Package Lambda Functions
Package the Lambda functions into zip files for deployment:
```bash
zip -r fetch_rates.zip lambdas/fetch_rates.py
zip -r api_handler.zip lambdas/api_handler.py
```

### 3. Upload to S3
Upload the packaged Lambda functions to an S3 bucket:
```bash
aws s3 cp fetch_rates.zip s3://your-deployment-bucket/
aws s3 cp api_handler.zip s3://your-deployment-bucket/
```

### 4. Deploy CloudFormation Stack
Deploy the application using the CloudFormation template:
```bash
aws cloudformation deploy \
  --template-file templates/cloudformation.yaml \
  --stack-name ExchangeTracker \
  --capabilities CAPABILITY_IAM
```

### 5. Configure API Gateway
After the stack is deployed, note the API Gateway URL from the CloudFormation outputs. Configure the endpoints:
- `/rates`: To fetch current rates.
- `/rates/difference`: To fetch rate differences.

## Usage

### Fetching Current Rates
Use the `/rates` endpoint to retrieve the latest exchange rates:
```bash
curl -X GET https://<API-Gateway-URL>/rates
```
Response:
```json
{
  "USD": 1.12,
  "GBP": 0.85,
  "JPY": 133.45
}
```

### Fetching Rate Differences
Use the `/rates/difference` endpoint to compare rates with the previous day:
```bash
curl -X GET https://<API-Gateway-URL>/rates/difference
```
Response:
```json
{
  "USD": 0.01,
  "GBP": -0.02,
  "JPY": 0.12
}
```

## Testing

### Local Testing
- Mock the ECB API response for testing the `fetch_rates` function.
- Use LocalStack to simulate AWS services locally.


## Deployment Details
- **Infrastructure**: Defined in `cloudformation.yaml`.
- **Endpoints**:
  - `/rates`: Provides current exchange rates.
  - `/rates/difference`: Provides the rate differences from the previous day.



aws lambda update-function-code \                                   
  --function-name ExchangeTracker-FetchRatesFunction-cGIUugYDyKNK \
  --s3-bucket samaritan-lambda-deployment-artifact \
  --s3-key fetch_rates.zip


aws lambda update-function-code \                                 
  --function-name ExchangeTracker-APIHandlerFunction-aNcMPjJJmgh5 \
  --s3-bucket samaritan-lambda-deployment-artifact \
  --s3-key api_handler.zip





aws lambda add-permission \
  --function-name ExchangeTracker-FetchRatesFunction-cGIUugYDyKNK \
  --statement-id AllowApiGatewayInvoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn arn:aws:execute-api:us-east-1:986939144885:7mhodq0ric/*/GET/rates
