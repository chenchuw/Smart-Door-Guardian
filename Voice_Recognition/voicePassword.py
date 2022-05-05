import json
import subprocess
import glob
import os
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# def voiceRecognition_start():
# 	global p1
# 	rpistr_voice = "./voice2text.sh"
# 	p1 = subprocess.Popen(rpistr_voice, shell=True, preexec_fn=os.setsid)

def publish_host():
    # Publish one Message
    myMQTTClient.publish(
        topic="$aws/things/k64f/shadow/update/accepted",
        QoS=1,
        payload="Host, open the door")

    print("Published message to the topic!")

def publish_unknown():
    # Publish one Message
    myMQTTClient.publish(
        topic="$aws/things/k64f/shadow/update/accepted",
        QoS=1,
        payload="Unknown person!")

    print("Published message to the topic!")



if __name__ == '__main__':
	myMQTTClient = AWSIoTMQTTClient("Ccw_Mac_ID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
	myMQTTClient.configureEndpoint("a2vv0cnk6n1beh-ats.iot.us-east-1.amazonaws.com", 8883)

	myMQTTClient.configureCredentials("./Certificates/root-ca.pem", "./Certificates/private.pem.key", "./Certificates/certificate.pem.crt")

	myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
	myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
	myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
	myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
	myMQTTClient.connect()
	print ('Initialized Connection between current device and AWS IoT Core...')

	# Read converted text from user
	with open("converted.json") as f:
		data = f.readlines()[1]
		
	data_json = json.loads(data)
	convText = (data_json['result'][0]['alternative'][0]['transcript'])

	print("\n" + convText)

	password = "networking the physical world"

	if convText == password:
		print("Password matched! Door open..")
		publish_host()
	else:
		print("Wrong password..")
		publish_unknown()
