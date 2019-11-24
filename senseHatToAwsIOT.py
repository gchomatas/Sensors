#!/usr/bin/python3 -u

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import json

from sense_hat import SenseHat
import os
import time
from SensorReadings import SensorReadings
from IOTArgParse import IOTArgParse

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


args = IOTArgParse()
args.parse_args()

print(args.topic, args.port, args.host, args.clientId)

# Configure logging
logging.basicConfig(filename='/var/log/senseHatToAwsIOT.log', level=logging.INFO)
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if args.useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(args.clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(args.host, args.port)
    myAWSIoTMQTTClient.configureCredentials(args.rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(args.clientId)
    myAWSIoTMQTTClient.configureEndpoint(args.host, args.port)
    myAWSIoTMQTTClient.configureCredentials(args.rootCAPath, args.privateKeyPath, args.certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(20)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
print("CONNECTED")

#if args.mode == 'both' or args.mode == 'subscribe':
#    myAWSIoTMQTTClient.subscribe(args.topic, 1, customCallback)
#time.sleep(2)
#print("SUBSCRIBED TO TOPIC")

# Publish to the same topic in a loop forever
sense_hat = SenseHat()

while True:
    if args.mode == 'both' or args.mode == 'publish':
        message = {}
        message['timestamp'] = int(time.time())
        message['sensor'] = SensorReadings(sense_hat).getAsMap()
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(args.topic, messageJson, 1)

        logging.info('Published topic %s: %s\n' % (args.topic, messageJson))

    time.sleep(60)

