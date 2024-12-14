import json
import boto3
from datetime import datetime, timedelta
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "ExchangeRatesTable"

# Custom encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super(DecimalEncoder, self).default(obj)

def get_current_rates(event, context):
    table = dynamodb.Table(TABLE_NAME)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    response = table.get_item(Key={"date": today})
    if "Item" not in response:
        return {"statusCode": 404, "body": "No data available for today"}

    # Serialize rates with DecimalEncoder
    return {
        "statusCode": 200,
        "body": json.dumps(response["Item"]["rates"], cls=DecimalEncoder)
    }

def get_rate_differences(event, context):
    table = dynamodb.Table(TABLE_NAME)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Fetch today's and yesterday's rates
    today_response = table.get_item(Key={"date": today})
    yesterday_response = table.get_item(Key={"date": yesterday})

    if "Item" not in today_response or "Item" not in yesterday_response:
        return {"statusCode": 404, "body": "Insufficient data"}

    today_rates = today_response["Item"]["rates"]
    yesterday_rates = yesterday_response["Item"]["rates"]

    # Calculate differences
    differences = {
        currency: float(today_rates[currency]) - float(yesterday_rates.get(currency, Decimal(0)))
        for currency in today_rates
    }

    # Serialize differences with DecimalEncoder
    return {
        "statusCode": 200,
        "body": json.dumps(differences, cls=DecimalEncoder)
    }
