from flask import Flask, render_template
import boto3
from datetime import datetime

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-south-1'
)

table = dynamodb.Table('IRSensorData')


@app.route("/")
def home():

    response = table.scan()

    items = response.get("Items", [])

    if len(items) == 0:
        return "No Data Available"

    # Sort by latest timestamp
    latest = sorted(items, key=lambda x: int(x["ts"]), reverse=True)[0]

    # Convert timestamp to readable format
    timestamp = int(latest["ts"]) / 1000

    latest["time"] = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %I:%M:%S %p")

    return render_template("index.html", data=latest)


if __name__ == "__main__":
    app.run(debug=True)