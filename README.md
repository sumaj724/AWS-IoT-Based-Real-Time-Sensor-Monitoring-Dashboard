# AWS IoT Based Real-Time Sensor Monitoring Dashboard

An IoT project that detects objects using an IR sensor and Arduino Uno, sends the data securely to **AWS IoT Core** over MQTT, stores it in **DynamoDB**, and shows the live status on a **Flask web dashboard**.

## Architecture

```
IR Sensor → Arduino Uno → (USB Serial) → Python Publisher
        → (MQTT over TLS) → AWS IoT Core → IoT Rule → DynamoDB
        → Flask Dashboard (browser)
```

## How It Works

1. The **IR sensor** outputs a digital signal when an object is near.
2. The **Arduino Uno** reads the sensor every second and prints `Object Detected` or `No Object` on the serial port.
3. `publisher.py` reads the serial data and publishes it to the topic `sensor/ir` on AWS IoT Core using MQTT over TLS (mutual certificate authentication).
4. An **AWS IoT Rule** stores each message in the **DynamoDB** table `IRSensorData`.
5. `dashboard.py` (Flask) reads the latest record and displays the status and last-updated time. The page auto-refreshes every 2 seconds.

## Tech Stack

| Layer | Technology |
|---|---|
| Hardware | Arduino Uno, IR sensor |
| Firmware | Arduino C++ |
| Messaging | MQTT, AWS IoT Core |
| Storage | AWS DynamoDB |
| Backend | Python, Flask, boto3 |
| Frontend | HTML, CSS |

## Project Structure

```
├── ir_sensor.ino          # Arduino code (reads IR sensor)
├── publisher.py           # Reads serial data and publishes to AWS IoT Core
├── dashboard.py           # Flask app that reads DynamoDB
├── templates/
│   └── index.html         # Dashboard page
└── certificates/          # NOT included - add your own AWS IoT certificates
```

## Hardware Connections

| IR Sensor | Arduino Uno |
|---|---|
| VCC | 5V |
| GND | GND |
| OUT | Digital Pin 2 |

## Setup

### 1. Prerequisites
- Python 3.8+
- Arduino IDE
- An AWS account with IoT Core and DynamoDB access
- AWS CLI configured (`aws configure`, region `ap-south-1`)

### 2. Install dependencies
```bash
pip install flask boto3 pyserial awsiotsdk
```

### 3. AWS setup
1. Create an IoT **Thing** and download its certificate, private key and `AmazonRootCA1.pem`.
2. Attach a policy allowing `iot:Connect` and `iot:Publish` on topic `sensor/ir`.
3. Create a DynamoDB table named `IRSensorData` with partition key `ts` (Number).
4. Create an **IoT Rule** on topic `sensor/ir` that writes messages to `IRSensorData`.
5. Put your certificates in a `certificates/` folder and update the `ENDPOINT` in `publisher.py`.

### 4. Upload the Arduino code
Open `ir_sensor.ino` in the Arduino IDE and upload it to the Uno.

### 5. Run the publisher
Update `COM_PORT` in `publisher.py` to match your Arduino port, then run:
```bash
python publisher.py
```

### 6. Run the dashboard
```bash
python dashboard.py
```
Open **http://127.0.0.1:5000** in your browser.

## Output

The dashboard shows:
- 🟢 **Object Detected** or 🔴 **No Object**
- The time of the last update

## Security Note

Certificates, private keys and AWS credentials are **not** stored in this repository. Never commit them.

## Future Improvements
- Show history charts of sensor readings
- Add email/SMS alerts using AWS SNS
- Support more sensors
- Deploy the dashboard on AWS EC2

## Author

**Suma J** — [GitHub](https://github.com/sumaj724)
