"""
In this code, is developed the library in order to have a communication channel 
between the broker and the subscriber
"""







"""
How to subscribe?

The only function needed to subscribe to a topic is the "subscribe" function. It recieves the messages from an online broker.
The funtion writes in a dict variable


######

PARAMETERS:

topic: is the topic that the client wants to subscribe. This topic has to be separated by slashes ( "/" ) and has to be
betwenn 2 and 10 arguments ("toAsset/deviceID/something/something_else")

information: the information is the message or the body that is going to be recieved. It has to be a dict and in this dict
there has to be a "lastMessage" parameter where the message is going to be written on. And everytime the message is recived, it changes
the parameter inside the dictionary. If there is no key-value pair with the name "lastMessage", one is created. 

clientID: Client ID is only a way to diferenciate the people that are accessing the information

username: Yet to be implemented

password: Yet to be implemented



WARNING AND ADVICES:

This function stop the process, wating for messages. If you want to continuasy recieve messages without stoping the main
process, you can create a thread and run in a different process. The dictionary, if pass down to the fucntion, is going to be change 
even in the main process. 



EXAMPLES:

from mqtt_SSOP import clientSubscriber
from time import sleep
import threading



if __name__ == '__main__':

    try:
        
        
        message = {
            "lastMessage" : "Not modified",
            "id" : id,
        }

        subThread = threading.Thread(target=lambda : clientSubscriber.subscribe("toAsset/123",message,"something"))
        subThread.start()

        while(1):
            sleep(5)
            print(message)
    

    except KeyboardInterrupt:
        subThread.join()
        print("Processed interrupted! Exiting... ")



######


"""








"""
Errors:
1-> To much arguments
2-> Message to big
3-> Couldn't decode the topic
2->
2->
2->
"""
import random
from paho.mqtt import client as mqtt_client
import json
from .gCentralComponentDB import newPayload

#Messges must be shoreter than 10000 carachters
MAX_LEN_MESSAGE = 10000
#The topic given cannot be longer than 10 arguments
MAX_N_OF_ARGUMENTS = 10

#Password and username to be implemanted later 
USERNAME = 'selssopcloud2'       #Escolher username!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PASSWORD = 'jp4dg'     #Escolher password!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CLOUD_TOPIC = 'ssop/SSOPCloud'

#Online broker information
broker = 'mqtt-broker.smartenergylab.pt'
port = 1883

#Connection to the online broker made available by spider


#First the client needs to connect to the broker
def connect_mqtt(clientID) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(clientID)
    client.username_pw_set(USERNAME,PASSWORD)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#After the client set up, it can send messages freely
def recieveMessage(client: mqtt_client, topic):
    
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        try:

            payload = msg.payload.decode()
            payload = payload.replace("\'","\"")
   
        except Exception as e:
            print( "\n\n" + str(e))
            return -8

        try:
            print(type(payload))
            payload = json.loads(payload)
            print(payload)

        except Exception as e:
            print(payload)
            print( "\n\n" + str(e))
            return -8


        try:
            identification = dict(payload['credentials'])
            data = dict(payload['data'])
        except Exception as e:
            print("Erro -4", e)
            return -4

        try: 
            if isinstance(identification, dict):
                print("To be implemented")
                pass
            
            id = newPayload(msg.topic, "Cloud", "inverterData", data)
            
            if id < 1:
                return -6
        except Exception as e:
            print("Erro -5", e)            
            print(e)
            return -5
        
    client.subscribe(topic)
    client.on_message = on_message





#Function of subscription by function 
def subscribe(topic, clientID,username=USERNAME, password=PASSWORD):
    # generate client ID with pub prefix randomly
    print("THREAD started")
    client = connect_mqtt(clientID)
    recieveMessage(client, topic)
    client.loop_start()
    
    while 1:

        try:
            something = input() 
            print(something)
        except KeyboardInterrupt:
            client.loop_stop()
            return 0
        except:
            print("something went wrong!")
            return -1000


    
