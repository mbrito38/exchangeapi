import json
import requests
import boto3
from datetime import datetime
from decimal import Decimal  # Import Decimal for precise numeric values

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "ExchangeRatesTable"

def fetch_and_store(event, context):
    # Fetch rates from ECB
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch exchange rates")
    
    # Parse XML (simplified for clarity)
    from xml.etree import ElementTree as ET
    tree = ET.fromstring(response.content)
    namespaces = {'gesmes': 'http://www.gesmes.org/xml/2002-08-01',
                  '': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    rates = {}
    for cube in tree.findall(".//Cube[@currency]", namespaces):
        currency = cube.attrib['currency']
        rate = Decimal(cube.attrib['rate'])  # Convert float to Decimal
        rates[currency] = rate

    # Store rates in DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(
        Item={
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "rates": rates
        }
    )
    return {"statusCode": 200, "body": "Exchange rates fetched and stored"}

