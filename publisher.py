import json
import serial
from awscrt import mqtt
from awsiot import mqtt_connection_builder

# ==========================
# Configuration
# ==========================
ENDPOINT = "a2lwlqbwp5rltx-ats.iot.ap-south-1.amazonaws.com"

CLIENT_ID = "ArduinoPublisher"

TOPIC = "sensor/ir"

COM_PORT = "COM3"

BAUD_RATE = 9600

PATH_TO_CERT = "certificates/device.pem.crt"
PATH_TO_KEY = "certificates/private.pem.key"
PATH_TO_ROOT = "certificates/AmazonRootCA1.pem"

# ==========================
# Connect Serial
# ==========================
ser = serial.Serial(COM_PORT, BAUD_RATE)

# ==========================
# Connect AWS IoT
# ==========================
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print("Connecting to AWS IoT Core...")
mqtt_connection.connect().result()
print("Connected successfully!")

# ==========================
# Read Arduino & Publish
# ==========================
while True:
    line = ser.readline().decode().strip()

    message = {
        "status": line
    }

    mqtt_connection.publish(
        topic=TOPIC,
        payload=json.dumps(message),
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    print("Published:", message)